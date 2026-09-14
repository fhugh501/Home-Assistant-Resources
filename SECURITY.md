# Security Policy

Home automation can interact with security systems, locks, cameras, presence sensors, network services, and other devices that affect privacy or physical security. Please handle security reports carefully.

## Supported Code

Security fixes are focused on the current version of resources in the repository's default `main` branch. Older copied or modified versions may not receive separate fixes.

## Reporting a Security Issue

Please **do not publish sensitive vulnerability details in a public GitHub issue, discussion, or pull request**.

If GitHub's private vulnerability reporting option is available for this repository, use **Security → Report a vulnerability** to submit the report privately.

If private vulnerability reporting is not available, open a minimal public issue stating only that you have identified a potential security concern and need a private reporting channel. Do not include exploit instructions, credentials, private URLs, personal information, or details that would make the issue easier to abuse.

## What to Include in a Private Report

When possible, include:

- The affected resource and file path
- A concise description of the issue
- Home Assistant version and relevant integration/component versions
- Steps needed to reproduce the problem
- The potential security or privacy impact
- Any proposed mitigation or fix

Please redact unrelated personal information and credentials.

## Sensitive Information

Never include real:

- Passwords
- API keys or access tokens
- Long-lived Home Assistant access tokens
- Webhook URLs containing secrets
- Private certificates or encryption keys
- Wi-Fi credentials
- Cloud-service credentials
- Alarm codes
- Door-lock codes
- Private camera URLs
- Precise private location data unless absolutely necessary and shared through an appropriate private channel

Home Assistant device IDs and entity IDs are not normally authentication secrets, but they may reveal information about a private installation. Share only what is necessary.

## Safe Testing

Do not test a suspected vulnerability against systems you do not own or have explicit permission to test. Avoid testing methods that could cause unsafe device behavior, disable alarms, unlock doors, expose cameras, damage equipment, or disrupt another person's Home Assistant installation.

## Response Expectations

This is a community project maintained by Dominion Smart Home Systems and does not currently provide a guaranteed security-response SLA. Credible reports will be reviewed and prioritized based on potential impact.

## Scope

This policy applies to code and resources maintained in this repository. Security issues in Home Assistant itself, third-party integrations, custom cards, device firmware, cloud services, or other dependencies should also be reported to the appropriate upstream project or vendor when applicable.