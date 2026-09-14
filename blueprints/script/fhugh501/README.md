# Export Device & Entity States

**Version 1.0.0** · **Home Assistant 2024.8.0+** · **Script blueprint**

A reusable Home Assistant script blueprint that exports detailed state information for one or more devices and/or individual entities into a copyable persistent notification.

It is designed for troubleshooting, documentation, configuration work, support requests, and quickly sharing the Home Assistant information exposed by a device or entity.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Ffhugh501%2FHome-Assistant-Resources%2Fmain%2Fblueprints%2Fscript%2Ffhugh501%2Fexport_device_entity_states.yaml)

### Manual import URL

```text
https://raw.githubusercontent.com/fhugh501/Home-Assistant-Resources/main/blueprints/script/fhugh501/export_device_entity_states.yaml
```

## What It Does

The blueprint creates a script that can inspect selected Home Assistant devices, individual entities, or both. It builds a text export and places the result in a Home Assistant persistent notification using Markdown code-block formatting for easy copying.

If an entity is selected individually and is also part of a selected device, the duplicate is automatically suppressed.

## Features

- Select multiple devices at once
- Select multiple standalone entities at once
- Use devices, entities, or both in the same run
- Automatically suppress duplicate entities
- Report the device name and Home Assistant device ID
- Report enabled entity count and total registered entity count for selected devices
- Export per-entity information including:
  - Friendly name
  - Entity ID
  - Domain
  - Current state
  - Availability
  - Available options
  - HVAC modes
  - Fan modes
  - Preset modes
  - Swing modes
  - Effects
  - Media sources
  - Sound modes
  - Common domain state references
  - Event type
  - Unit of measurement
  - Device class
  - State class
  - All currently exposed attributes
- Output to a native Home Assistant persistent notification
- No custom integration required

## Requirements

- **Home Assistant 2024.8.0 or newer**
- Blueprint support enabled through standard Home Assistant functionality
- No HACS or custom component required

The minimum version is declared in the blueprint itself. Version 2024.8.0 is used because the blueprint uses Home Assistant's modern `action:` YAML syntax. Other features used by the blueprint, including multiple entity/device selectors and `has_value()`, were introduced earlier.

## Installation

### One-click import

Use the **Import Blueprint** button above. Your configured My Home Assistant instance should open the blueprint import dialog with this blueprint URL pre-filled.

### Manual import

1. Copy the manual import URL above.
2. In Home Assistant, go to **Settings → Automations & scenes → Blueprints**.
3. Select **Import Blueprint**.
4. Paste the URL.
5. Select **Preview**.
6. Select **Import**.
7. Create a new **script** from the imported blueprint.

## Usage

1. Create a script from **Export Device & Entity States**.
2. Select one or more devices, individual entities, or both.
3. Save the script.
4. Run it.
5. Open the resulting Home Assistant persistent notification.
6. Copy the exported information from the code block.

## Understanding the Device Counts

For a selected device, `Total registered entities` comes from Home Assistant's device registry and can include hidden or disabled entities.

`Enabled entities` represents entities that are currently loaded into Home Assistant's state machine. Detailed entity output is generated for those loaded entities.

This distinction is intentional and can be useful when diagnosing why a device appears to have more registered entities than are currently usable.

## Example Output

The exact fields vary based on what each integration exposes. A typical section looks similar to this:

```text
DEVICE
==================================================
Name: Example Device
Device ID: 0123456789abcdef0123456789abcdef
Enabled entities: 2
Total registered entities: 3

ENTITIES
==================================================

Friendly name: Example Temperature
Entity ID: sensor.example_temperature
Domain: sensor
Current state: 72.4
Available: True

Unit: °F
Device class: temperature
State class: measurement

Attributes:
  friendly_name: Example Temperature
  unit_of_measurement: °F
  device_class: temperature
  state_class: measurement
```

This is an illustrative example, not output from a specific installation.

## Privacy & Sharing Warning

**Review the export before posting or sending it to anyone.**

The blueprint intentionally exports all currently exposed state attributes. Depending on the integration, those attributes can contain information you may not want to share publicly, including device identifiers, local URLs, media information, location-related data, network information, or other installation-specific values.

Redact anything sensitive before posting an export to GitHub, the Home Assistant Community forum, Reddit, Discord, or a support ticket.

## Persistent Notification Behavior

The blueprint uses the notification ID:

```text
device_entity_export
```

Running the script again updates the existing export notification rather than creating a growing stack of notifications. This is intentional.

## Clipboard Note

Home Assistant persistent notifications cannot automatically write to the browser or device clipboard. The export is rendered inside a Markdown code block so it can be selected and copied manually.

A true one-click clipboard button would require frontend/custom-card functionality and would reduce the portability of this native blueprint.

## Known Limitations

- The export only has detailed state information for entities currently loaded into Home Assistant.
- Disabled entities may be included in the total registered count but will not have a current state to export.
- Very large devices or large multi-device selections can produce lengthy notifications.
- Attribute values are reproduced as Home Assistant exposes them and are not automatically redacted.
- The fixed notification ID means each run replaces the previous export notification.

## Validation Status

Repository-side validation completed for **v1.0.0** on **2026-09-13**:

- ✅ Blueprint domain is `script`
- ✅ Blueprint inputs use supported device/entity selectors
- ✅ Blueprint inputs are exposed as script variables before use in templates
- ✅ `device_entities()`, `device_name()`, `states()`, `state_attr()`, and `has_value()` are supported Home Assistant template functions
- ✅ `persistent_notification.create` is a current Home Assistant action and supports Markdown messages
- ✅ Minimum Home Assistant version is declared
- ✅ My Home Assistant import URL targets the current repository blueprint file
- ⬜ Final live import/run test in a real Home Assistant instance
- ⬜ Release screenshot from the live Home Assistant UI

The final two checks require an actual Home Assistant instance and should be completed before posting the blueprint to the public Blueprint Exchange.

## Blueprint File

[`export_device_entity_states.yaml`](export_device_entity_states.yaml)

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md).

## Author

**Dominion Smart Home Systems**  
A **Dominion Technology Consulting** project  
GitHub: **fhugh501**

## License

MIT License. See the repository-level [`LICENSE`](../../../LICENSE) file.

## Support

If you encounter a bug or have a feature request, use the structured issue forms in the [Home Assistant Resources repository](https://github.com/fhugh501/Home-Assistant-Resources/issues).
