# Blueprint Exchange Post Draft — DO NOT PUBLISH UNTIL LIVE TEST PASSES

## Suggested title

**Export Device & Entity States — Copyable device/entity diagnostics [Script Blueprint]**

## Suggested tags

`script` · `blueprint` · `yaml` · `notification`

---

# Export Device & Entity States

A reusable **Home Assistant script blueprint** that exports detailed device and entity state information into a copyable persistent notification.

I built this to make troubleshooting and documentation easier when you need to collect the Home Assistant information exposed by a device or entity without manually copying each state and attribute.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Ffhugh501%2FHome-Assistant-Resources%2Fmain%2Fblueprints%2Fscript%2Ffhugh501%2Fexport_device_entity_states.yaml)

## Features

- Select multiple devices
- Select multiple standalone entities
- Use devices and individual entities together
- Automatically suppress duplicate entities
- Reports device name, device ID, enabled entity count, and total registered entity count
- Exports entity ID, friendly name, domain, state, and availability
- Exports supported option/mode lists when exposed
- Exports unit, device class, state class, event type, and all current attributes
- Uses a native Home Assistant persistent notification
- No HACS or custom integration required

## Requirements

- Home Assistant **2024.8.0 or newer**
- No additional integrations are required beyond standard Home Assistant functionality

## How to use

1. Import the blueprint using the button above.
2. Create a new script from **Export Device & Entity States**.
3. Select one or more devices, individual entities, or both.
4. Save and run the script.
5. Open the generated persistent notification and copy the export from the code block.

## Duplicate handling

If an entity is selected individually and is also associated with one of the selected devices, it is exported only once.

## Privacy warning

The blueprint intentionally exports **all currently exposed attributes**. Depending on the integration, attributes can contain device identifiers, URLs, media information, location-related values, network information, or other installation-specific data.

**Review and redact the output before posting it publicly.**

## Source, documentation, and changelog

- Repository: https://github.com/fhugh501/Home-Assistant-Resources
- Blueprint documentation: https://github.com/fhugh501/Home-Assistant-Resources/tree/main/blueprints/script/fhugh501
- Blueprint source: https://github.com/fhugh501/Home-Assistant-Resources/blob/main/blueprints/script/fhugh501/export_device_entity_states.yaml

## Blueprint YAML

**Before publishing this forum post:** copy the complete current contents of `export_device_entity_states.yaml` from the repository and paste it into a `yaml` code block here. Home Assistant's Blueprint Exchange rules require the full blueprint configuration to be included in the forum topic.

```yaml
# PASTE THE COMPLETE CURRENT BLUEPRINT YAML HERE IMMEDIATELY BEFORE PUBLISHING.
```

## Release checklist before posting

- [ ] Import badge opens the correct blueprint import preview in a real Home Assistant instance
- [ ] Blueprint imports without warnings/errors
- [ ] Script can be created from the imported blueprint
- [ ] Device-only selection tested
- [ ] Entity-only selection tested
- [ ] Mixed device + entity selection tested
- [ ] Duplicate suppression tested
- [ ] Persistent notification renders correctly
- [ ] Output can be copied from the Markdown code block
- [ ] Screenshot captured with sensitive values redacted
- [ ] Full current YAML pasted into this post draft

---

**Project:** Dominion Smart Home Systems  
A Dominion Technology Consulting project  
License: MIT
