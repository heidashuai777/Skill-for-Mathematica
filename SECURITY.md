# Security

## Supported versions

Security updates apply to the latest release and the current `main` branch.

## Reporting a vulnerability

Do not report secrets in public issues.

For sensitive reports, contact the repository owner directly through GitHub. Include:

- the affected file or workflow,
- the risk and reproduction steps,
- whether any credential, notebook, or private source material was exposed.

## Secret handling

This repository must not contain:

- Wolfram account credentials,
- API keys or secured authentication keys,
- cookies or local auth tokens,
- private notebooks or proprietary package documentation,
- generated caches that include private user content.

Use environment variables, OS keychain storage, Wolfram secure credential mechanisms, or another local secret manager for live integrations.
