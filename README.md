# Bestow PoC

Death claim triage Proof of Concept application.

## Configuration

This project manages environment variables using `pydantic-settings` via configuration classes (`app/config.py`).

A foundational set of default environment variables are documented and exposed in `.env.example`. To set up your local environment:

```bash
cp .env.example .env
```

### Core Variables

| Variable      | Description                                         | Default       | Options                                         |
|---------------|-----------------------------------------------------|---------------|-------------------------------------------------|
| `ENVIRONMENT` | Dictates application logging formats and behaviors. | `development` | `development`, `staging`, `production`          |
| `LOG_LEVEL`   | Controls verbosity of the structured logger.        | `INFO`        | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `LOG_FORMAT`  | Forces the output format of the structured logger.  | `auto`        | `auto`, `console`, `json`                       |

When writing new features, please add their associated environment variables to the specific config models (e.g. `APIConfig` or `UIConfig`) and update `.env.example` and this README accordingly.
