# Developer Mode Light Controller

Control a light and observe how its reported values change during a requested
transition. Version **1.1.0-rc.1** adds visible blueprint settings, refresh requests,
a timestamped sample log, and a comparison of requested versus reported timing.
No custom integration or helpers are required.

## Install or update

[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Ffhugh501%2FHome-Assistant-Resources%2Fmain%2Fblueprints%2Fscript%2Ffhugh501%2Fdeveloper_mode_light_controller.yaml)

Paste this URL into **Import a blueprint**, or use the button:

```text
https://raw.githubusercontent.com/fhugh501/Home-Assistant-Resources/main/blueprints/script/fhugh501/developer_mode_light_controller.yaml
```

For an existing installation, re-import the blueprint from its source to update
it. Open the script made from it and configure the settings below. Save the
script before running it. The blueprint and script action names are unchanged.
New settings have defaults so existing runtime calls remain usable.

1. Select **Light to test**.
2. Choose on, off, toggle, or status.
3. Enable **Set brightness** and choose a target, if testing brightness.
4. Choose **Color setting**: keep, RGB, or color temperature.
5. Set the requested transition time, sample interval, and extra observation time.
6. Leave **Request light refresh before every sample** enabled for active refresh
   requests. Start with a two-second interval.
7. Save, run the script, and open Home Assistant's notification panel.

You can also call the script from **Developer Tools → Actions** and override these
settings with its runtime fields. The light selection can be left blank in the
blueprint only if a runtime `light_entity` will be supplied. A plain run with no
selected light stops with an explanatory notification.

## What the test does

- Requests an initial refresh, records baseline values, then starts its clock
  immediately **before** sending the light command.
- Sends one native light action with the requested transition. It does not
  simulate a fade by sending many brightness commands.
- Samples immediately after dispatch and approximately every configured interval.
  When refresh is enabled, each sample is preceded by
  `homeassistant.update_entity`. Slow action/refresh calls increase sample spacing;
  recorded elapsed times include that latency.
- Continues for the requested transition plus extra observation time (default
  five seconds), even when the target is reported early.
- Updates one notification with current values, HA timestamps, first target-match
  time, intermediate-sample count, and the most recent 12 sample rows.
- Leaves a final summary with separate sections for the initial transition and
  any optional timed shutoff. Each phase retains up to 120 samples in the returned
  response; total counts and first-match timing cover the complete phase.

For a useful brightness test, begin at a substantially different brightness
from the requested target. An already-matching baseline cannot establish fade
behavior. Observe the physical light alongside the log.

**Important measurement limit:** Home Assistant may publish the target immediately
while the light is still fading. Some integrations ignore forced refreshes,
return cached values, or suppress intermediate transition reports. Neither
`last_updated` nor `last_reported` proves the device was queried or physically
reached a setting. The tool reports **observations**, not a physical pass/fail.

## Example

Replace `light.example_headboard` and, if necessary, the script action name:

```yaml
action: script.developer_mode_light_controller
data:
  light_entity: light.example_headboard
  command: turn_on
  transition: 30
  brightness_pct: 80
  rgb_color: [0, 86, 214]
  status_interval: 2
  settle_time: 5
  poll: true
```

A notification might show brightness values at 0, 2, 4, … seconds and first
matching values near 30 seconds. If it reports 80% immediately, the assessment
says the physical transition is unverified; it does not treat that as a pass.

### Assessments

| Observation | Interpretation |
| --- | --- |
| Target matched before dispatch | Already at target; timing inconclusive. |
| Target reported immediately | Optimistic feedback or fast response; physical timing unverified. |
| Intermediate values with target time near request | HA reports are compatible with the request; confirm physical behavior separately. |
| Target reported earlier/later | Inspect sample times, polling latency, and the physical light. |
| No intermediate values | Feedback is insufficient to establish physical fade timing. |
| Target never reported, or final values do not match | Target not observed within the window, or not sustained. |
| Unavailable samples | Timing inconclusive; inspect connectivity and trace. |

A target match requires the requested on/off state and all explicitly selected
settings. Brightness tolerance is two percentage points; temperature tolerance is
100 K. RGB is normalized to a maximum channel of 255 before comparing, with a
12/255 channel tolerance, because HA often separates brightness from RGB color
and converts RGB to a device's native color space. This is an approximate color
comparison, not a colorimetric measurement. Effect, when provided, must match
exactly. Off targets use the off state, since brightness/color attributes may be
missing or retained when off. Only requested color/effect channels participate.

Timing compatibility allows the larger of one sample interval or two seconds
around the request. First-match time is the first **sample** that matched, not an
exact device completion timestamp. The report also records the last nonmatching
sample before it. A coarse interval may miss the whole transition.

## Controls and runtime overrides

| Runtime field | Configured fallback / behavior |
| --- | --- |
| `light_entity` | Light to test; required either here or in blueprint settings. |
| `command` | Configured command; on, off, toggle, or status. |
| `brightness_pct` | Configured brightness if Set brightness is enabled; optional 0–100. Zero requests off. |
| `rgb_color` | Configured RGB if selected; three integers 0–255. |
| `color_temp_kelvin` | Configured temperature if selected; 1000–40000 K within actual device limits. |
| `effect` | Configured exact effect name, or empty to omit. |
| `transition` | Configured transition; default 30, range 0–3600 seconds. |
| `status_interval` | Configured interval; default 2, range 1–60 seconds. |
| `settle_time` | Configured extra observation time; default 5, range 0–300 seconds. |
| `poll` | Configured refresh option; default true. False samples HA state without refresh requests. |
| `duration` | Optional on duration after the initial observation; default 0 disables timed shutoff. Range 0–86400 seconds. |

A runtime RGB override supersedes a configured temperature, and vice versa.
Supplying both runtime color formats is rejected. Brightness/color/effect are
only sent for a resolved turn-on action. Toggle resolves from the current
reported state; other controllers can race with it. Device capabilities and
native action errors still apply. The report includes whether the integration
advertises transition support; that flag does not prove support for every duration.

`duration` waits after the initial transition and extra observation time, then
sends off with the same transition and observes that too. Initial-test results
are retained separately. Zero brightness or an initial off action never schedules
another shutoff. No prior state is restored. Other controllers can change the
light during a test; their changes are included in the observations, and any
scheduled shutoff still occurs.

One test runs per script instance (`mode: single`). Additional runs are rejected
while it is active. Stop the script with `script.turn_off` to cancel sampling and
a pending timed shutoff; this does not cancel a fade already sent to the device.

### Status only

```yaml
action: script.developer_mode_light_controller
data:
  light_entity: light.example_headboard
  command: status
  poll: true
```

Requests refreshes and returns a snapshot without sending a light command.
Unknown/unavailable states are allowed for status. Changing commands reject them
after the initial refresh. Polling and light-action failures stop the script and
remain visible in its trace; a preparing/starting/running notification without a
finished report indicates an interrupted or failed run.

### Response data

Call the script action directly with `response_variable` in another script or
automation to receive the final result. `script.turn_on` starts it in the
background without returning the response.

The response contains `entity_id`, `state`, `available`, `advertised_transition`,
`refresh_requested`, `reports`, and `physical_timing_verified` (always false).
Each phase report includes baseline/final snapshots, first-match and preceding
nonmatch times, intermediate/unavailable counts, sample and refresh-request
counts, a bounded `samples` list, `samples_truncated`, and an `assessment`.
Samples include elapsed time, observed timestamp, state, brightness, RGB, xy,
color temperature, color mode, effect, HA update/report timestamps, and whether
requested values match. Counts describe observed samples, not independent device
responses. The notification and script trace contain entity IDs and settings.

## Validation

Install `tests/requirements.txt`, then run from the repository root:

```sh
python3 -m unittest discover -s tests -p test_light_control.py -v
```

Tests execute the actual YAML templates and control flow against simulated light
feedback and a clock. They cover gradual fades, early/late/immediate target
reports, stale feedback, active polling and disabling polling, polling/command
latency and failures, off/toggle, timed shutoff, unavailable lights, bounded
history, visible input defaults, runtime overrides, and approximate RGB matching.
These tests do not run the HA script engine or real hardware. Sampling and
comparison templates have additionally been evaluated read-only in the user's
live HA template engine; no light command was sent for that validation. Full
script/schema/frontend and physical fade testing remain pending. Declared
minimum HA version 2024.8.0 has not been live-tested.

References: Home Assistant [light features and color conversion](https://contributors.home-assistant.io/core/entities/light/),
[refresh requests and limitations](https://www.home-assistant.io/actions/homeassistant.update_entity/),
and [script fields/responses](https://www.home-assistant.io/docs/script/).
