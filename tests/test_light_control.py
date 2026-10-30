"""Execute the blueprint's templates and control flow with a simulated light/clock.

Offline contract tests; these do not replace Home Assistant schema or hardware tests.
"""
import copy
import datetime
from pathlib import Path
import unittest

import yaml
from jinja2.nativetypes import NativeEnvironment
from jinja2.sandbox import SandboxedEnvironment
from jinja2 import StrictUndefined

BLUEPRINT = Path(__file__).resolve().parents[1] / 'blueprints/script/fhugh501/developer_mode_light_controller.yaml'


class Environment(SandboxedEnvironment, NativeEnvironment):
    pass


class Stopped(Exception):
    def __init__(self, result=None, error=False):
        self.result = result
        self.error = error


class LightHarness:
    def __init__(self, state='off', fail_action=False, unavailable_after=None):
        self.doc = yaml.safe_load(BLUEPRINT.read_text())
        self.state = state
        self.attrs = {'brightness': 64, 'rgb_color': [255, 255, 255],
                      'supported_color_modes': ['rgb', 'color_temp']}
        self.seconds = 0
        self.notifications = []
        self.calls = []
        self.fail_action = fail_action
        self.unavailable_after = unavailable_after
        self.env = Environment(undefined=StrictUndefined)
        self.env.globals.update(
            states=lambda entity: self.state if entity == 'light.test' else 'unknown',
            state_attr=lambda entity, attr: self.attrs.get(attr),
            now=lambda: datetime.datetime(2026, 10, 30, tzinfo=datetime.timezone.utc)
                + datetime.timedelta(seconds=self.seconds),
            as_timestamp=lambda dt: dt.timestamp(),
        )

    def render(self, value, context):
        if isinstance(value, str):
            return self.env.from_string(value).render(context)
        if isinstance(value, dict):
            return {key: self.render(item, context) for key, item in value.items()}
        if isinstance(value, list):
            return [self.render(item, context) for item in value]
        return value

    def conditions(self, conditions, context):
        return all(self.render(item['value_template'], context) for item in conditions)

    def sequence(self, steps, context):
        for step in steps:
            if 'variables' in step:
                for key, value in step['variables'].items():
                    context[key] = self.render(value, context)
            elif 'if' in step:
                if self.conditions(step['if'], context):
                    self.sequence(step['then'], context)
            elif 'repeat' in step:
                count = 0
                while self.conditions(step['repeat']['while'], context):
                    self.sequence(step['repeat']['sequence'], context)
                    count += 1
                    if count > 1000:
                        raise AssertionError('Unbounded polling loop')
            elif 'delay' in step:
                self.seconds += self.render(step['delay']['seconds'], context)
                if self.unavailable_after is not None and self.seconds >= self.unavailable_after:
                    self.state = 'unavailable'
            elif 'stop' in step:
                raise Stopped(context.get(step.get('response_variable')), step.get('error', False))
            elif 'action' in step:
                action = self.render(step['action'], context)
                data = self.render(step.get('data', {}), context)
                if action == 'persistent_notification.create':
                    self.notifications.append(copy.deepcopy(data))
                else:
                    if self.fail_action:
                        raise RuntimeError('Simulated integration error')
                    self.calls.append((action, self.render(step['target'], context), data))
                    self.state = 'on' if action == 'light.turn_on' else 'off'
                    if 'brightness_pct' in data:
                        self.attrs['brightness'] = round(data['brightness_pct'] * 255 / 100)
                        if data['brightness_pct'] == 0:
                            self.state = 'off'
                    for key in ['rgb_color', 'color_temp_kelvin', 'effect']:
                        if key in data:
                            self.attrs[key] = data[key]
            else:
                raise AssertionError(f'Unhandled step: {step}')

    def run(self, **fields):
        context = {'this': {'entity_id': 'script.developer_mode_light_controller'}, **fields}
        try:
            self.sequence(self.doc['sequence'], context)
        except Stopped as stopped:
            if stopped.error:
                raise ValueError(self.notifications[-1]['message'])
            return stopped.result
        raise AssertionError('No response')


class LightControlTests(unittest.TestCase):
    def test_requested_example_and_refresh(self):
        h = LightHarness()
        result = h.run(light_entity='light.test', transition=30,
                       brightness_pct=80, rgb_color=[0, 86, 214])
        self.assertEqual(h.calls, [('light.turn_on', {'entity_id': 'light.test'},
            {'transition': 30, 'brightness_pct': 80, 'rgb_color': [0, 86, 214]})])
        self.assertEqual(h.seconds, 32)
        self.assertGreater(len(h.notifications), 10)
        self.assertEqual(len({n['notification_id'] for n in h.notifications}), 1)
        self.assertIn('Reported RGB: [0, 86, 214]', h.notifications[-1]['message'])
        self.assertEqual(result['state'], 'on')
        self.assertAlmostEqual(result['brightness_pct'], 80, delta=0.3)

    def test_yaml_omitted_fields_have_runtime_defaults(self):
        h = LightHarness()
        h.run(light_entity='light.test')
        self.assertEqual(h.calls[0][2], {'transition': 0})
        self.assertEqual(h.seconds, 2)

    def test_off_does_not_send_on_only_attributes(self):
        h = LightHarness('on')
        h.run(light_entity='light.test', command='turn_off', rgb_color=[1, 2, 3],
              brightness_pct=50, effect='rainbow', duration=10)
        self.assertEqual(h.calls, [('light.turn_off', {'entity_id': 'light.test'}, {'transition': 0})])
        self.assertEqual(h.seconds, 2)

    def test_toggle_both_directions(self):
        for before, action in [('on', 'light.turn_off'), ('off', 'light.turn_on')]:
            with self.subTest(before=before):
                h = LightHarness(before)
                h.run(light_entity='light.test', command='toggle')
                self.assertEqual(h.calls[0][0], action)

    def test_timed_shutoff_and_non_divisible_interval(self):
        h = LightHarness()
        result = h.run(light_entity='light.test', transition=3, duration=5, status_interval=3)
        self.assertEqual([c[0] for c in h.calls], ['light.turn_on', 'light.turn_off'])
        self.assertEqual(h.seconds, 15)  # 3+2 monitoring, 5 hold, 3+2 off monitoring
        self.assertEqual(result['state'], 'off')
        self.assertTrue(any('Waiting for timed shutoff' in n['message'] for n in h.notifications))

    def test_status_is_read_only_even_when_unavailable(self):
        h = LightHarness('unavailable')
        result = h.run(light_entity='light.test', command='status')
        self.assertFalse(h.calls)
        self.assertEqual(h.seconds, 0)
        self.assertFalse(result['available'])

    def test_invalid_requests_never_send_light_actions(self):
        for fields in [{}, {'light_entity': 'switch.test'}, {'light_entity': ['light.test']},
                       {'command': 'invalid'}, {'transition': -1}, {'transition': 'bad'},
                       {'duration': 86401}, {'status_interval': 0}, {'brightness_pct': 101},
                       {'brightness_pct': True}, {'rgb_color': [0, 1]},
                       {'rgb_color': [0, 1, 256]}, {'rgb_color': [0, 1, 2.5]},
                       {'rgb_color': 'red'}, {'color_temp_kelvin': 999},
                       {'rgb_color': [0, 1, 2], 'color_temp_kelvin': 3000}, {'effect': []}]:
            with self.subTest(fields=fields):
                h = LightHarness()
                args = {'light_entity': 'light.test', **fields} if fields else {}
                with self.assertRaises(ValueError):
                    h.run(**args)
                self.assertFalse(h.calls)

    def test_unavailable_prevents_toggle_or_on(self):
        for state in ['unknown', 'unavailable']:
            h = LightHarness(state)
            with self.assertRaises(ValueError):
                h.run(light_entity='light.test', command='toggle')
            self.assertFalse(h.calls)

    def test_temperature_effect_and_zero_brightness(self):
        h = LightHarness()
        h.run(light_entity='light.test', color_temp_kelvin=3000, effect='steady')
        self.assertEqual(h.calls[0][2], {'transition': 0, 'color_temp_kelvin': 3000, 'effect': 'steady'})
        h = LightHarness()
        h.run(light_entity='light.test', brightness_pct=0, duration=10)
        self.assertEqual(len(h.calls), 1)
        self.assertEqual(h.seconds, 2)

    def test_status_rereads_state_and_does_not_claim_success(self):
        h = LightHarness(unavailable_after=2)
        result = h.run(light_entity='light.test', transition=4)
        self.assertEqual(result['state'], 'unavailable')
        self.assertIn('Reported state: unavailable', h.notifications[-1]['message'])
        self.assertNotIn('success', h.notifications[-1]['message'].lower())

    def test_action_error_does_not_produce_final_report(self):
        h = LightHarness(fail_action=True)
        with self.assertRaises(RuntimeError):
            h.run(light_entity='light.test')
        self.assertIn('Sending request', h.notifications[-1]['message'])
        self.assertFalse(any('Final report' in n['message'] for n in h.notifications))


if __name__ == '__main__':
    unittest.main()
