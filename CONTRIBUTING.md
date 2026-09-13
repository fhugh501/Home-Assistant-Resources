# Contributing to Dominion Smart Home Systems — Home Assistant Resources

Thank you for helping improve this repository.

This is a **Dominion-curated** Home Assistant resource collection. Community bug reports, compatibility updates, documentation improvements, feature suggestions, and pull requests that improve existing Dominion Smart Home Systems resources are welcome.

The repository is not intended to become a general collection of unrelated third-party Home Assistant projects. New resource ideas are welcome as feature requests, but inclusion is at the maintainer's discretion.

## Ways to Contribute

You can help by:

- Reporting a reproducible bug
- Suggesting an improvement or new feature
- Fixing an issue in an existing resource
- Improving documentation or installation instructions
- Reporting compatibility changes with Home Assistant or a documented dependency
- Improving portability by replacing installation-specific values with reusable inputs or placeholders

Before submitting an entirely new resource, open a feature request first so the idea can be reviewed for fit with the repository.

## Before You Submit a Pull Request

Please make sure that:

- The change has been tested in Home Assistant when applicable.
- No passwords, API keys, access tokens, webhook URLs, private URLs, or other secrets are included.
- Personal information has been removed or replaced with clear placeholders.
- Installation-specific entity IDs, device IDs, addresses, coordinates, usernames, or similar values are not hard-coded unless they are clearly marked examples and necessary to explain the resource.
- Required custom integrations, cards, add-ons, hardware, firmware, or other dependencies are documented.
- Documentation is updated when behavior, configuration, requirements, or installation steps change.
- Any third-party code, images, or other material you include is compatible with this repository's license and is properly attributed when required.
- You have the right to contribute the submitted material.

## Repository Organization

Use the existing structure whenever possible.

### Blueprints

Home Assistant blueprints should be organized by domain and author/maintainer namespace:

```text
blueprints/
├── automation/
│   └── fhugh501/
└── script/
    └── fhugh501/
```

Each substantial blueprint should include clear documentation describing what it does, requirements, configuration, and installation.

### Dashboards

Dashboard resources should use a dedicated project folder:

```text
dashboards/
└── project-name/
    ├── README.md
    └── dashboard-template.yaml
```

Use reusable placeholders rather than publishing entity IDs from a private Home Assistant installation.

### Future Resource Types

As resources are added, additional top-level directories may include:

```text
esphome/
devices/
custom-integrations/
converters/
templates/
hardware/
3d-models/
docs/
```

New top-level categories should be added only when there is an actual resource to place in them.

## Documentation Expectations

A substantial resource should document, as applicable:

- Purpose and use case
- Requirements
- Home Assistant version tested
- Required integrations or custom components
- Required hardware
- Installation steps
- Configuration steps
- Example use
- Known limitations
- Screenshots or example output when they materially help users

## Pull Request Guidelines

Keep pull requests focused on one logical change whenever practical.

A good pull request should explain:

1. What changed
2. Why the change is useful or necessary
3. How it was tested
4. Any Home Assistant, integration, hardware, or dependency versions that matter

Please do not mix unrelated formatting changes, new features, and bug fixes into the same pull request unless they are inseparable.

## Security and Privacy

Do not publish sensitive security information, credentials, access tokens, precise private location data, or exploit details in a public issue or pull request.

See [SECURITY.md](SECURITY.md) for security-reporting guidance.

## Licensing of Contributions

Unless explicitly stated otherwise for a particular resource, this repository is licensed under the [MIT License](LICENSE).

By submitting a contribution, you represent that you have the right to submit it and agree that the submitted contribution may be distributed under the repository's MIT License.

## Project Ownership and Curation

**Dominion Smart Home Systems** is a Dominion Technology Consulting project. Repository maintainers may decline or modify contributions that do not fit the project's scope, quality standards, security expectations, or long-term direction.

Constructive contributions and community feedback are appreciated.