# Dominion Smart Home Systems — Home Assistant Resources

**Community-built Home Assistant resources from Dominion Smart Home Systems, a Dominion Technology Consulting project.**

This repository is a growing collection of reusable Home Assistant resources developed from real-world smart-home projects. The goal is to make useful automations, scripts, dashboards, ESPHome configurations, device resources, templates, utilities, and related projects easy to discover, understand, and reuse.

> **Not affiliated with or endorsed by Nabu Casa or the Home Assistant project.** Home Assistant is an open-source home automation platform.

## Available Resources

### Dashboards

#### TRMNL 800×480 E-Ink Home Status Dashboard

A fixed-size **Home Assistant dashboard template** designed for an 800×480 TRMNL e-ink display and screenshot-based delivery through TRMNL HA.

**Highlights include:**

- Action-focused Notification Center with larger alert icons
- Prominent smoke, CO, and security alarm handling
- Door, vehicle, laundry, and plant-moisture notifications
- Current weather and local 60-minute rain probability
- Static OSM/RainViewer radar optimized for e-ink capture
- Compact security, indoor climate, and outdoor AQI panels
- Kiosk Mode support for a clean header-free screenshot
- Fixed 800×480 layout with refresh date/time footer
- Reusable `replace_*` entity placeholders instead of installation-specific entity IDs

[View full documentation](dashboards/trmnl-eink-home-status/README.md) · [View dashboard template YAML](dashboards/trmnl-eink-home-status/dashboard-template.yaml)

> Dashboard templates are not native Home Assistant automation/script blueprints, so this resource is installed by copying the YAML into a dedicated dashboard and replacing the documented entity placeholders.

### Hardware & 3D Printing

#### TRMNL 7.5" OG DIY Kit Wall Mount

A community-designed two-part 3D-printable wall mount for the **TRMNL 7.5" OG DIY Kit**. The design uses four M3 screws and is a useful starting point for remixes, including adding recessed magnets for refrigerator mounting.

[View and download on Printables](https://www.printables.com/model/1385847-trmnl-diy-kit-wall-mount)

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

Unless otherwise noted, the resources and source code published in this repository are licensed under the **MIT License**.

Copyright (c) 2026 Dominion Technology Consulting.

See [LICENSE](LICENSE) for the full license text.

This license applies to material published in this public repository. Separate Dominion Smart Home Systems products, premium resources, services, or private repositories may be offered under different terms.
