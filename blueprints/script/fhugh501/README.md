# Export Device & Entity States

A reusable **Home Assistant script blueprint** that exports detailed state information for one or more devices and/or individual entities into a copyable persistent notification.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Ffhugh501%2FHome-Assistant-Resources%2Fmain%2Fblueprints%2Fscript%2Ffhugh501%2Fexport_device_entity_states.yaml)

### Manual import URL

```text
https://raw.githubusercontent.com/fhugh501/Home-Assistant-Resources/main/blueprints/script/fhugh501/export_device_entity_states.yaml
```

## What It Does

This blueprint creates a script that can inspect selected Home Assistant devices and individual entities and place a detailed export into a persistent notification.

It is useful when you need a clean, copyable inventory of entity states and attributes for troubleshooting, documentation, configuration work, or sharing device details.

## Features

- Select multiple devices at once
- Select multiple standalone entities at once
- Use devices, entities, or both in the same run
- Automatically suppress duplicate entities when an entity is selected directly and also belongs to a selected device
- Export:
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
  - All current attributes
- Output is placed in a Home Assistant persistent notification inside a code block for easy copying
- No custom integration required

## Requirements

- Home Assistant with blueprint support
- No custom components required

## Installation

### One-click import

Use the **Import Blueprint** button above. Your configured My Home Assistant instance should open the blueprint import dialog with the YAML URL pre-filled.

### Manual import

1. Copy the manual import URL above.
2. In Home Assistant, go to **Settings → Automations & scenes → Blueprints**.
3. Select **Import Blueprint**.
4. Paste the URL.
5. Select **Preview**.
6. Select **Import**.

Because this is a **script blueprint**, create a new script from the imported blueprint after installation.

## Usage

1. Create a script from **Export Device & Entity States**.
2. Select one or more devices, individual entities, or both.
3. Save the script.
4. Run it.
5. Open the resulting Home Assistant persistent notification.
6. Copy the exported information from the code block.

### Duplicate handling

If an entity is selected individually and is also associated with one of the selected devices, it is exported only once.

## Output

For selected devices, the export includes the device name, device ID, enabled entity count, total registered entity count, and details for enabled entities.

For each exported entity, the blueprint reports the information currently exposed by Home Assistant, including its state, supported option lists where available, classification information, and all current attributes.

## Clipboard Note

Home Assistant persistent notifications cannot automatically write to the browser or device clipboard. The export is therefore rendered in a code block for easy manual copying from the frontend.

A true one-click clipboard action would require frontend or custom-card functionality and would reduce the portability of this native blueprint.

## Blueprint File

[`export_device_entity_states.yaml`](export_device_entity_states.yaml)

## Author

**fhugh501**  
Dominion Smart Home Systems  
A Dominion Technology Consulting project

## Support

If you encounter a bug or have a feature request, open an issue in the [Home Assistant Resources repository](https://github.com/fhugh501/Home-Assistant-Resources/issues).
