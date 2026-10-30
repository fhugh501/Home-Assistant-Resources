"""Contract tests executing the public YAML; not the HA script engine or hardware."""
import copy
from collections import ChainMap
import datetime
from pathlib import Path
from types import SimpleNamespace
import unittest

import yaml
from jinja2 import StrictUndefined
from jinja2.nativetypes import NativeEnvironment
from jinja2.sandbox import SandboxedEnvironment

BLUEPRINT = Path(__file__).resolve().parents[1] / 'blueprints/script/fhugh501/developer_mode_light_controller.yaml'

class Input(str): pass
class Loader(yaml.SafeLoader): pass
Loader.add_constructor('!input', lambda loader, node: Input(loader.construct_scalar(node)))
class Environment(SandboxedEnvironment, NativeEnvironment): pass
class Stopped(Exception):
    def __init__(self, result=None, error=False):
        self.result, self.error = result, error

class Context(ChainMap):
    """Approximate HA's nonparallel child scopes: update existing outer names."""
    def __setitem__(self, key, value):
        for scope in self.maps:
            if key in scope:
                scope[key] = value
                return
        self.maps[0][key] = value

class StateAccess:
    def __init__(self, harness): self.h = harness
    def __call__(self, entity): return self.h.state if entity == 'light.test' else 'unknown'
    def __getitem__(self, entity):
        if entity != 'light.test': return StrictUndefined(name=entity)
        return SimpleNamespace(last_updated=self.h.at(self.h.changed), last_reported=self.h.at(self.h.reported))

class LightHarness:
    def __init__(self, state='off', mode='instant', fail_action=False, unavailable_after=None,
                 fail_poll=False, poll_latency=0, command_latency=0):
        self.doc = yaml.load(BLUEPRINT.read_text(), Loader=Loader)
        self.state, self.mode = state, mode
        self.attrs = {'brightness': 64, 'rgb_color': [255,255,255], 'supported_features':44}
        self.seconds = self.changed = self.reported = 0
        self.notifications, self.calls, self.polls = [], [], []
        self.fail_action, self.fail_poll = fail_action, fail_poll
        self.unavailable_after, self.poll_latency = unavailable_after, poll_latency
        self.command_latency, self.pending = command_latency, None
        self.max_render = 0
        self.env = Environment(undefined=StrictUndefined)
        self.env.globals.update(states=StateAccess(self),state_attr=lambda e,a:self.attrs.get(a),
            now=lambda:self.at(self.seconds), as_timestamp=lambda dt:dt.timestamp())

    def at(self, seconds):
        return datetime.datetime(2026,10,30,tzinfo=datetime.timezone.utc)+datetime.timedelta(seconds=seconds)

    def render(self, value, context):
        if isinstance(value, Input): return context['inputs'][str(value)]
        if isinstance(value, str):
            rendered = self.env.from_string(value).render(context)
            self.max_render = max(self.max_render, len(str(rendered)))
            if self.max_render > 262144: raise AssertionError('Oversized template result')
            return rendered
        if isinstance(value, dict):return {k:self.render(v,context) for k,v in value.items()}
        if isinstance(value, list):return [self.render(v,context) for v in value]
        return value

    def conditions(self, items, ctx):
        return all(self.render(i['value_template'],ctx) for i in items)

    def refresh(self):
        self.polls.append(self.seconds)
        if self.fail_poll: raise RuntimeError('Simulated poll failure')
        self.seconds += self.poll_latency
        before = self.state, copy.deepcopy(self.attrs)
        if self.pending and self.mode not in ['stale','instant']:
            p = self.pending
            fraction = min(1,(self.seconds-p['start']) / max(0.001,p['duration']))
            self.attrs['brightness'] = round(p['from']+(p['to']-p['from'])*fraction)
            self.state = 'off' if p['off'] and fraction >= 1 else 'on'
            for k in ['rgb_color','color_temp_kelvin','effect']:
                if k in p['data'] and fraction >= 1:self.attrs[k] = p['data'][k]
        if self.unavailable_after is not None and self.seconds >= self.unavailable_after:
            self.state = 'unavailable'
        if before != (self.state,self.attrs):self.changed = self.seconds
        if self.mode != 'stale':self.reported = self.seconds

    def sequence(self, steps, ctx):
        for step in steps:
            if 'variables' in step:
                for k,v in step['variables'].items():ctx[k] = self.render(v,ctx)
            elif 'if' in step:
                if self.conditions(step['if'],ctx):self.sequence(step['then'],ctx.new_child())
            elif 'repeat' in step:
                block = step['repeat']
                if 'for_each' in block:
                    for index,item in enumerate(self.render(block['for_each'],ctx),1):
                        child = ctx.new_child({'repeat':{'item':item,'index':index}})
                        self.sequence(block['sequence'],child)
                else:
                    for index in range(1,100001):
                        child = ctx.new_child({'repeat':{'index':index}})
                        self.sequence(block['sequence'],child)
                        if self.conditions(block['until'],ctx):break
                    else:raise AssertionError('Unbounded polling loop')
            elif 'delay' in step:self.seconds += self.render(step['delay']['seconds'],ctx)
            elif 'stop' in step:raise Stopped(ctx.get(step.get('response_variable')), step.get('error',False))
            elif 'action' in step:
                action = step['action']
                data = self.render(step.get('data',{}),ctx)
                if action == 'persistent_notification.create':self.notifications.append(copy.deepcopy(data))
                elif action == 'homeassistant.update_entity':self.refresh()
                elif action in ['light.turn_on','light.turn_off']:
                    if self.fail_action:raise RuntimeError('Simulated command failure')
                    self.calls.append((action,self.render(step['target'],ctx),data,self.seconds))
                    off = action == 'light.turn_off' or data.get('brightness_pct') == 0
                    initial = self.attrs.get('brightness',0) if self.state == 'on' else 0
                    target = 0 if off else round(data.get('brightness_pct',self.attrs.get('brightness',255)/255*100)*255/100)
                    duration = data.get('transition',0)
                    if self.mode == 'early':duration /= 3
                    if self.mode == 'late':duration *= 2
                    self.pending = dict(start=self.seconds,duration=duration,off=off,to=target,
                                        **{'from':initial},data=data)
                    self.seconds += self.command_latency
                    if self.mode == 'instant' or duration == 0:
                        self.state = 'off' if off else 'on'
                        self.attrs['brightness'] = target
                        for k in ['rgb_color','color_temp_kelvin','effect']:
                            if k in data:self.attrs[k] = data[k]
                        self.changed = self.reported = self.seconds
                else:raise AssertionError(f'Unexpected action: {action}')
            else:raise AssertionError(f'Unexpected step: {step}')

    def run(self, inputs=None, **fields):
        defaults = {k:v['default'] for k,v in self.doc['blueprint']['input'].items()}
        ctx = Context({'this':{'entity_id':'script.developer_mode_light_controller'},
               'inputs':{**defaults,**(inputs or {})},**fields})
        try:self.sequence(self.doc['sequence'],ctx)
        except Stopped as stop:
            if stop.error:raise ValueError(self.notifications[-1]['message'])
            return stop.result
        raise AssertionError('Missing response')

class LightControlTests(unittest.TestCase):
    def test_rgb_example_dispatches_once_and_polls(self):
        h = LightHarness()
        r = h.run(light_entity='light.test',transition=30,brightness_pct=80,rgb_color=[0,86,214])
        self.assertEqual(h.calls[0][:3],('light.turn_on',{'entity_id':'light.test'},
            {'transition':30,'brightness_pct':80,'rgb_color':[0,86,214]}))
        self.assertEqual(len(h.calls),1)
        self.assertGreater(len(h.polls),10)
        self.assertEqual(h.seconds,35)
        self.assertIn('immediately',r['reports'][0]['assessment'])
        self.assertFalse(r['physical_timing_verified'])
        self.assertEqual(len({n['notification_id'] for n in h.notifications}),1)

    def test_blueprint_controls_run_without_runtime_fields(self):
        h = LightHarness(mode='ramp')
        r = h.run(inputs={'selected_light':'light.test','set_brightness':True,
            'target_brightness':80,'transition_seconds':30})
        report = r['reports'][0]
        self.assertGreater(report['intermediate_samples'],3)
        self.assertAlmostEqual(report['first_target_at'],30,delta=2)
        self.assertIn('compatible',report['assessment'])
        self.assertIn('| elapsed s |',h.notifications[-1]['message'])

    def test_runtime_overrides_blueprint_color_and_numeric_settings(self):
        h = LightHarness()
        h.run(inputs={'selected_light':'light.test','color_setting':'color_temp'},
              rgb_color=[0,86,214],transition=4,status_interval=3,settle_time=1)
        self.assertNotIn('color_temp_kelvin',h.calls[0][2])
        self.assertEqual(h.calls[0][2]['rgb_color'],[0,86,214])
        self.assertEqual(h.seconds,5)

    def test_rgb_matching_normalizes_brightness_scale(self):
        h = LightHarness('on',mode='stale')
        h.attrs.update(brightness=204,rgb_color=[1,108,255])
        r = h.run(light_entity='light.test',brightness_pct=80,rgb_color=[0,86,214],transition=0)
        self.assertTrue(r['reports'][0]['samples'][0]['matches_target'])

    def test_early_late_stale_and_already_at_target(self):
        for mode, phrase in [('early','earlier'),('late','later'),('stale','not reported')]:
            with self.subTest(mode=mode):
                h = LightHarness(mode=mode)
                r = h.run(light_entity='light.test',brightness_pct=80,transition=10,settle_time=15)
                self.assertIn(phrase,r['reports'][0]['assessment'])
        h = LightHarness('on')
        h.attrs['brightness'] = 204
        r = h.run(light_entity='light.test',brightness_pct=80)
        self.assertIn('Already',r['reports'][0]['assessment'])

    def test_polling_can_be_disabled_and_does_not_become_device_read_claim(self):
        h = LightHarness()
        r = h.run(light_entity='light.test',poll=False,transition=2)
        self.assertFalse(h.polls)
        self.assertFalse(r['refresh_requested'])
        self.assertIn('cached',h.notifications[-1]['message'])

    def test_off_and_toggle_do_not_send_on_only_data(self):
        for state, command, action in [('on','turn_off','light.turn_off'),('on','toggle','light.turn_off'),('off','toggle','light.turn_on')]:
            with self.subTest(state=state,command=command):
                h = LightHarness(state)
                h.run(light_entity='light.test',command=command,brightness_pct=50,rgb_color=[1,2,3],transition=0)
                self.assertEqual(h.calls[0][0],action)
                if action.endswith('turn_off'):self.assertEqual(h.calls[0][2],{'transition':0})

    def test_off_fade_collects_intermediates(self):
        h = LightHarness('on',mode='ramp')
        r = h.run(light_entity='light.test',command='turn_off',transition=10)
        self.assertGreater(r['reports'][0]['intermediate_samples'],0)
        self.assertEqual(r['state'],'off')

    def test_status_is_read_only_and_unavailable_allowed(self):
        h = LightHarness('unavailable')
        r = h.run(light_entity='light.test',command='status')
        self.assertFalse(h.calls)
        self.assertFalse(r['available'])
        self.assertEqual(r['reports'][0]['sample_count'],1)

    def test_unavailable_prevents_commands_and_midtest_inconclusive(self):
        h = LightHarness('unavailable')
        with self.assertRaises(ValueError):h.run(light_entity='light.test')
        self.assertFalse(h.calls)
        h = LightHarness(unavailable_after=2)
        r = h.run(light_entity='light.test',transition=4)
        self.assertIn('Unavailable',r['reports'][0]['assessment'])

    def test_invalid_input_never_dispatches(self):
        invalid=[{'light_entity':''},{'light_entity':['light.test']},{'command':'bad'},
            {'brightness_pct':True},{'brightness_pct':101},{'transition':-1},{'status_interval':0},
            {'settle_time':301},{'duration':86401},{'poll':'yes'},
            {'rgb_color':[0,1]},{'rgb_color':[0,1,256]},{'rgb_color':[0,1,2.5]},
            {'rgb_color':'red'},{'rgb_color':[0,1,2],'color_temp_kelvin':3000},
            {'color_temp_kelvin':999},{'effect':[]}]
        for case in invalid:
            with self.subTest(case=case):
                h = LightHarness()
                with self.assertRaises(ValueError):h.run(**{'light_entity':'light.test',**case})
                self.assertFalse(h.calls)

    def test_timed_off_keeps_initial_report(self):
        h = LightHarness(mode='ramp')
        r = h.run(light_entity='light.test',brightness_pct=80,transition=4,settle_time=1,duration=5)
        self.assertEqual([c[0] for c in h.calls],['light.turn_on','light.turn_off'])
        self.assertEqual([p['phase'] for p in r['reports']],['Transition test','On duration','Timed shutoff test'])
        self.assertEqual(h.seconds,15)
        self.assertIn('Transition test',h.notifications[-1]['message'])
        self.assertEqual(r['state'],'off')

    def test_zero_brightness_does_not_schedule_shutoff(self):
        h = LightHarness()
        r = h.run(light_entity='light.test',brightness_pct=0,duration=10,transition=0)
        self.assertEqual(len(h.calls),1)
        self.assertEqual(r['state'],'off')

    def test_failures_do_not_produce_finished_notification(self):
        for flag in ['fail_poll','fail_action']:
            h = LightHarness(**{flag:True})
            with self.assertRaises(RuntimeError):h.run(light_entity='light.test')
            self.assertFalse(any(n['title'].endswith('finished') for n in h.notifications))

    def test_long_run_bounds_sample_history_but_preserves_counts(self):
        h = LightHarness(mode='ramp')
        r = h.run(light_entity='light.test',brightness_pct=80,transition=130,status_interval=1)
        p = r['reports'][0]
        self.assertGreater(p['sample_count'],120)
        self.assertEqual(len(p['samples']),120)
        self.assertTrue(p['samples_truncated'])
        self.assertGreater(p['intermediate_samples'],100)
        self.assertLess(max(len(n['message']) for n in h.notifications),15000)

    def test_clock_includes_command_and_refresh_latency(self):
        h = LightHarness(command_latency=3,poll_latency=0.2)
        r = h.run(light_entity='light.test',transition=5,settle_time=1)
        p = r['reports'][0]
        self.assertGreaterEqual(p['samples'][0]['elapsed'],3)
        self.assertGreaterEqual(p['final']['elapsed'],6)
        self.assertGreater(p['poll_requests'],1)

    def test_temperature_effect_and_support_flag(self):
        h = LightHarness()
        h.attrs['supported_features'] = 0
        r = h.run(light_entity='light.test',color_temp_kelvin=3000,effect='steady',transition=0)
        self.assertEqual(h.calls[0][2],{'transition':0,'color_temp_kelvin':3000,'effect':'steady'})
        self.assertFalse(r['advertised_transition'])

if __name__ == '__main__':unittest.main()
