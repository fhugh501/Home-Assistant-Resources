# Developer Mode Light Controller

A native Home Assistant script blueprint for one light at a time. Its runtime
fields provide a light picker, on/off/toggle/status selector, brightness slider,
RGB color picker, color temperature, effect, transition time, optional timed
shutoff, and notification refresh interval. No custom integration is required.

Version: **1.0.0-rc.1**. Offline contract tests are included. Home Assistant schema,
frontend, and physical-device testing remain pending. Minimum declared version:
Home Assistant 2024.8.0; this minimum has not been tested on a live installation.

## Install

[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Ffhugh501%2FHome-Assistant-Resources%2Fmain%2Fblueprints%2Fscript%2Ffhugh501%2Fdeveloper_mode_light_controller.yaml)

Use the button above, or paste this public URL into **Import a blueprint**:

```text
https://raw.githubusercontent.com/fhugh501/Home-Assistant-Resources/main/blueprints/script/fhugh501/developer_mode_light_controller.yaml
```

Select **Preview**, then **Import**, and create a script named **Developer Mode
Light Controller**. Its fields are available when calling the script in
**Developer Tools → Actions**.

### Manual installation

1. Copy [the blueprint](../developer_mode_light_controller.yaml) to
   `/config/blueprints/script/fhugh501/developer_mode_light_controller.yaml` in Home Assistant.
2. Reload blueprints (or restart Home Assistant), then open **Settings → Automations
   & scenes → Blueprints** and create a script from **Developer Mode Light Controller**.
3. Name the script **Developer Mode Light Controller**. Find its action name in
   **Developer Tools → Actions**; the examples below assume
   `script.developer_mode_light_controller`. Substitute your actual action name if different.
4. Select the action in Developer Tools. Its fields appear in the action form.
   Select the light, enable the optional fields you want, and run it. Open the
   Home Assistant notification panel to watch the status refresh.

Alternatively, after copying the blueprint, add this entry to `scripts.yaml`
(if your configuration uses `script: !include scripts.yaml`), then reload scripts:

```yaml
developer_mode_light_controller:
  alias: Developer Mode Light Controller
  use_blueprint:
    path: fhugh501/developer_mode_light_controller.yaml
    input: {}
```

This is a script blueprint. Do not paste the complete blueprint into Developer
Tools → Actions; call the script created from it.

## Example headboard light

```yaml
action: script.developer_mode_light_controller
data:
  light_entity: light.example_headboard
  command: turn_on
  transition: 30
  brightness_pct: 80
  rgb_color: [0, 86, 214]
  status_interval: 2
```

Replace `light.example_headboard` with your own light entity. This sends a blue
RGB color at 80% brightness with a 30-second transition. It then refreshes one persistent
notification approximately every two seconds for the requested 30-second transition
plus a two-second reporting grace period. The report includes state, brightness,
RGB, color temperature, effect, color mode, and the elapsed/remaining observation
timer. The final report stays visible until dismissed or replaced by the next run.

Some integrations publish the requested target immediately or update attributes
infrequently. Reported values and the observation timer **do not prove physical
fade progress or that the requested values were reached**. The tool reads Home
Assistant's current state; it does not force device polling.

## Controls

| Field | Behavior |
| --- | --- |
| `light_entity` | Required single `light.*` entity. |
| `command` | `turn_on` (default), `turn_off`, `toggle`, or read-only `status`. |
| `brightness_pct` | Optional 0–100. Omit to leave brightness to the device/integration. Zero requests off. |
| `rgb_color` | Optional `[red, green, blue]`, each an integer 0–255. |
| `color_temp_kelvin` | Optional 1000–40000 K, within the device's actual supported range. Cannot be combined with RGB. |
| `effect` | Optional exact effect name from the entity's `effect_list`. Empty string is omitted. |
| `transition` | 0–3600 seconds; default 0. Applies to both the initial action and timed shutoff. |
| `duration` | 0–86400 seconds; default 0 means no timed shutoff. Starts **after** the initial transition observation plus two-second grace period. |
| `status_interval` | 1–60 seconds; default 2. Approximate notification refresh interval, not device polling frequency. |

Brightness, color, temperature, and effect are only sent when the resolved action
is `turn_on`. Toggle reads the starting state and resolves to `turn_on` or
`turn_off`; it is not atomic with other controllers. A duration applies only when
the resolved action is `turn_on` and brightness is not zero. At its end, the script
turns the light off and observes that transition too. It does not restore the
previous state. For example, `transition: 30` with `duration: 60` sends off about
92 seconds after the initial action returns, then monitors for another 32 seconds.

Only one run per script instance is allowed at a time. Additional calls while
monitoring or waiting for shutoff are rejected with a warning. Create separate
script instances for independent lights. Other automations and manual controls
can still change the light during a run; a scheduled shutoff will still occur.
To cancel monitoring and a pending shutoff, stop the script with `script.turn_off`.
Stopping the script does not cancel a transition already sent to the light, and
the last notification remains visible.

### Read status without changing the light

```yaml
action: script.developer_mode_light_controller
data:
  light_entity: light.example_headboard
  command: status
```

Returns a snapshot and updates the notification, including when the light is
unknown/unavailable. This is a single snapshot, not continuous monitoring.

### Color temperature and timed shutoff

```yaml
action: script.developer_mode_light_controller
data:
  light_entity: light.example_headboard
  command: turn_on
  brightness_pct: 40
  color_temp_kelvin: 3000
  transition: 5
  duration: 600
```

### Use the final snapshot in another script or automation

```yaml
- action: script.developer_mode_light_controller
  data:
    light_entity: light.example_headboard
    command: status
  response_variable: light_status
- action: persistent_notification.create
  data:
    title: Headboard status
    message: "State: {{ light_status.state }}; brightness: {{ light_status.brightness_pct }}%"
```

Call the script action directly to wait for its final response. `script.turn_on`
starts it in the background and does not return that response. Responses contain
`entity_id`, `state`, `available`, `brightness_pct` (or null), `rgb_color`,
`color_temp_kelvin`, `color_mode`, `effect`, `supported_color_modes`, `effect_list`,
and `observed_at`. Availability means Home Assistant reports `on` or `off`;
it does not certify connectivity or physical output.

## Errors and device support

Invalid input is rejected before any light action is sent, with a notification
and a script error. Missing/unknown/unavailable lights are rejected for changing
commands. Unsupported capabilities, out-of-device-range temperatures, and service
errors follow Home Assistant's native error handling: inspect the script trace.
If an action raises an error, monitoring stops without a final snapshot; the last
notification tells you to check the trace. Successful action dispatch and the end
of the observation window are not a success check against requested values.

Use a light's actual supported features and color modes. RGB, color temperature,
effects, and smooth transitions depend on the integration and hardware. RGB may be
converted to another supported color space. Effects may also override colors.

The notification includes your entity ID and light settings. It is local Home
Assistant UI output and remains until dismissed or replaced.

## Validation

Run `python3 -m unittest discover -s tests -p test_light_control.py -v` from the repository root with
`tests/requirements.txt` installed. The light-control tests execute the actual YAML
templates, conditionals, polling loops, and response path against a simulated
clock and light. They do not run the Home Assistant script engine.

Before relying on it, import into a test Home Assistant installation, confirm the
fields render in Developer Tools, run a short transition, check status against
Developer Tools → States, test off/toggle, then test a short timed shutoff.

Built using Home Assistant's documented [script fields and responses](https://www.home-assistant.io/docs/script/),
[selectors](https://www.home-assistant.io/docs/blueprint/selectors/), and
[light actions and reported attributes](https://www.home-assistant.io/integrations/light/).
