# Bestow PoC

Death claim triage Proof of Concept application.

## Quickstart & Local Dev Guide

This guide covers how to set up the repository for local development, focusing on the optimal path for MacOS engineers using Apple Silicon Metal acceleration.

### Prerequisites

1. **Python Development Environment:**
    * Install `uv` (the fast Python package installer and resolver).
2. **Container Runtimes:**
    * **Docker Desktop** or **OrbStack** (OrbStack is highly recommended for performance).
    * **Tilt** (for local Kubernetes development loop): `brew install tilt`
3. **Local LLM Guardrail (Ollama):**
    * The PII Tokenizer Guardrail uses a local Small Language Model (SLM) for deterministic tokenization.
    * To leverage Apple's Metal GPU and avoid sluggish behavior in K8s CPU containers, **you must run Ollama natively on your Mac.**
    * Install the Ollama Desktop App or run: `brew install --cask ollama`
    * Once installed, **pull the designated guardrail model:**

        ```bash
        ollama pull llama3.1:8b
        ```

### 1. Initial Setup

> [!NOTE]
> **Tilt Automation:** If you intend to run the application via Kubernetes with Tilt (Path A), the `tilt up` command will automatically bootstrap your virtual environment, create your `.env` file, generate a new guardrail hex key, and pull the required Ollama model. The only manual step required is adding your `LLM_MAIN_API_KEY` to the `.env` file!

If you are not using Tilt or need to manually bootstrap the project for other local workflows, follow these steps:

Bootstrap your virtual environment and resolve dependencies:

```bash
make install
```

Generate your local `.env` file by copying the template:

```bash
cp .env.example .env
```

Review your `.env` file to ensure the configuration maps correctly to your setup.

* The `LLM_GUARDRAIL_API_BASE` should be set to `http://host.docker.internal:11434` for local Mac development so the containers can route out to your natively running Ollama instance. (Tip: You can use `make config-tilt` and `make config-local` to quickly toggle these local networking targets.)
* Set your `LLM_MAIN_API_KEY` to an active OpenAI key.
* Generate a secure hex key for the `LLM_GUARDRAIL_SECRET_KEY`:

    ```bash
    make generate-guardrail-key
    ```

    This will automatically write the secure key to your `.env` file.

### 2. Booting the Application Infrastructure

You have two paths for running the application locally:

#### Path A: Kubernetes with Tilt (Recommended)

This path identically mirrors the cloud deployment architecture using a local cluster and live-reloads code on save.

```bash
make tilt
```

Press `Spacebar` to open the Tilt dashboard in your browser. From there, you can view the logs for the `api` and `ui` pods.

#### Path B: Docker Compose (Minimalist)

If you do not want to run a local Kubernetes cluster, you can spin up the raw containers:

```bash
make up
```

### 3. Local Development Workflows

* **View the UI:** Open [http://localhost:8501](http://localhost:8501)
* **Run the Test Suite:** `uv run pytest`
* **Linting and Formatting:** `make format-py-all` and `make format-md-all`

### 4. Environment Cleanup

When you need to completely teardown the project's infrastructure or reset your environment, use the provided cleanup targets:

* **`make down`**: Stops the minimal Docker Compose services and removes volumes.
* **`make clean`**: Removes all temporary python cache directories (`__pycache__`, `.pytest_cache`, `.ruff_cache`, `.uv_cache`) and build outputs (`out/`).
* **`make eject`**: Completely removes all local resources. It runs `clean`, removes your local virtual environment (`.venv`) and `.env` file, and gracefully shuts down running Docker or Tilt infrastructure.

## Configuration

This project manages environment variables using `pydantic-settings` via configuration classes (`app/config.py`).

A foundational set of default environment variables are documented and exposed in `.env.example`.

### Core Variables

| Variable      | Description                                         | Default       | Options                                         |
|---------------|-----------------------------------------------------|---------------|-------------------------------------------------|
| `ENVIRONMENT` | Dictates application logging formats and behaviors. | `development` | `development`, `staging`, `production`          |
| `LOG_LEVEL`   | Controls verbosity of the structured logger.        | `INFO`        | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `LOG_FORMAT`  | Forces the output format of the structured logger.  | `auto`        | `auto`, `console`, `json`                       |

When writing new features, please add their associated environment variables to the specific config models (e.g. `APIConfig` or `UIConfig`) and update `.env.example` and this README accordingly.

## Notes on Cloud Deployment

The in-cluster deployment of Ollama (`deploy/local/k8s/ollama.yaml`) is currently deferred in the `Tiltfile` to strictly enforce routing LLM requests to the Mac Host for development performance. When deploying to AWS/Azure Staging environments, the cloud infrastructure manifests will provision the in-cluster Ollama service, and your CI/CD pipeline will inject the cluster-internal DNS routing (`http://ollama:11434`) dynamically.
