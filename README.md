# Dominion Smart Home Systems — Home Assistant Resources

**Community-built Home Assistant resources from Dominion Smart Home Systems, a Dominion Technology Consulting project.**

This repository is a growing collection of reusable Home Assistant resources developed from real-world smart-home projects. The goal is to make useful automations, scripts, dashboards, ESPHome configurations, device resources, templates, utilities, and related projects easy to discover, understand, and reuse.

> **Not affiliated with or endorsed by Nabu Casa or the Home Assistant project.** Home Assistant is an open-source home automation platform.

## Available Resources

### Blueprints

#### Export Device & Entity States

A reusable **script blueprint** that exports detailed Home Assistant state information for one or more devices and/or individual entities into a copyable persistent notification.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Ffhugh501%2FHome-Assistant-Resources%2Fmain%2Fblueprints%2Fscript%2Ffhugh501%2Fexport_device_entity_states.yaml)

**Features include:**

- Select multiple devices and standalone entities in one run
- Automatically suppress duplicate entities
- Export entity IDs, friendly names, domains, states, and availability
- Export selectable options and supported HVAC, fan, preset, swing, effect, source, and sound modes
- Export event type, unit of measurement, device class, and state class
- Export all currently exposed entity attributes
- Produce a persistent notification formatted for easy copy/paste
- No custom integration required

[View full documentation](blueprints/script/fhugh501/README.md) · [View blueprint YAML](blueprints/script/fhugh501/export_device_entity_states.yaml)

## Repository Scope

As the project grows, this repository is intended to include resources in areas such as:

- Automation blueprints
- Script blueprints
- Home Assistant dashboards
- ESPHome projects and device configurations
- Jinja templates and helpers
- Custom integrations and utilities
- Data converters and export tools
- Device setup guides
- Hardware and 3D-printable smart-home projects
- Documentation and examples

## Installing Blueprints

Blueprints can be installed using the **Import Blueprint** button shown with each supported blueprint.

You can also import manually in Home Assistant:

1. Go to **Settings → Automations & scenes → Blueprints**.
2. Select **Import Blueprint**.
3. Paste the GitHub or raw YAML URL for the blueprint.
4. Select **Preview** and then **Import**.
5. Create an automation or script from the imported blueprint, depending on its type.

## Project Philosophy

Resources in this repository are intended to be understandable, reusable, and practical. Wherever possible, projects should:

- Use native Home Assistant functionality before requiring custom dependencies
- Avoid hard-coded entity IDs when selectors or configuration inputs can be used instead
- Include clear installation and usage documentation
- Be designed for reuse outside the original installation
- Clearly identify external integrations or hardware requirements

## Issues and Contributions

Bug reports, feature suggestions, compatibility notes, and improvements are welcome through GitHub issues and pull requests as the repository expands.

## Branding

**Dominion Smart Home Systems**  
A **Dominion Technology Consulting** project

## License

Licensing information will be provided for resources in this repository. Until an explicit license is added, the presence of source code in this public repository should not be interpreted as granting rights beyond those provided by GitHub's terms of service.
