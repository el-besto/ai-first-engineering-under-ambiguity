# Minimal Makefile for local repo workflows

PRE_COMMIT ?= uv tool run --from pre-commit pre-commit
TOOLS_DIR := tools

BLUE := \033[0;34m
GREEN := \033[0;32m
NC := \033[0m

##@ Help

.PHONY: help
help: ## Display available targets
	@awk 'BEGIN {FS = ":.*##"; printf "\n$(BLUE)Usage:$(NC)\n  make $(GREEN)<target>$(NC)\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  $(GREEN)%-18s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Local Runtime / Scaffolds

.PHONY: install api kill-api ui kill-ui compile-dspy generate-guardrail-key tilt tilt-down kill-tilt prepare-rancher-desktop up down
install: ## Bootstrap and install the virtual environment dependencies
	uv sync

api: ## Boot the thin FastAPI ingress shell
	uv run uvicorn drivers.api.main:app --reload --port 8000

kill-api: ## Forcibly kill any stray FastAPI processes occupying ports
	pkill -f uvicorn || true

ui: ## Boot the thin Streamlit workbench shell
	PYTHONPATH=. uv run streamlit run drivers/ui/streamlit/streamlit_app.py

kill-ui: ## Forcibly kill any stray Streamlit processes occupying ports
	pkill -f streamlit || true

generate-guardrail-key: ## Generate a random 32-byte hex key for the Vaultless Guardrail and save to .env
	uv run python -m drivers.cli.main infra generate-guardrail-key

config-tilt: ## Configure the local .env API Base targets for Tilt/Docker execution
	uv run python -m drivers.cli.main infra set-config --tilt

config-local: ## Configure the local .env API Base targets for Host/Mac native execution
	uv run python -m drivers.cli.main infra set-config --local

tilt: ## Start Tilt for local infrastructure deployment
	tilt up

tilt-down: ## Tear down Tilt infrastructure deployment
	tilt down

kill-tilt: ## Forcibly kill any stray Tilt processes occupying ports
	pkill -f tilt || true

up: ## Start the minimal docker-compose services manually
	docker compose -f deploy/local/compose.yaml up -d

down: ## Stop the minimal docker-compose services and remove volumes
	docker compose -f deploy/local/compose.yaml down -v

compile-dspy: ## Compile the DSPy PII Guardrail locally against Ollama
	uv run python scripts/compile_dspy_guardrail.py

prepare-rancher-desktop: ## Re-point Docker CLI plugins to Rancher Desktop binaries
	bash tools/prepare-rancher-desktop.sh

##@ LangSmith Studio

.PHONY: install studio studio-debug kill-studio
studio: ## Start the LangGraph development loop locally
	uv run langgraph dev

studio-debug: ## Start LangGraph development loop with a debugger port open
	PYDEVD_DISABLE_FILE_VALIDATION=1 uv run python -Xfrozen_modules=off -m langgraph_cli dev --debug-port 5678

kill-studio: ## Forcibly kill any stray LangGraph Studio processes occupying ports
	pkill -f langgraph || true

##@ Cleanup

.PHONY: clean eject
clean: ## Remove all temporary directories, python caches, and build outputs
	@echo "$(BLUE)Cleaning temporary directories and caches...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf out/
	rm -rf .uv_cache/
	@echo "$(GREEN)Clean complete.$(NC)"

eject: clean ## Completely remove all local resources, environments, and sensitive info
	@echo "$(BLUE)Ejecting all local project state...$(NC)"
	-docker compose -f deploy/local/compose.yaml down -v 2>/dev/null || true
	-tilt down 2>/dev/null || true
	rm -f .env
	rm -rf .langgraph_api/
	rm -rf .venv/
	@echo "$(GREEN)Ejection complete. The repository is now clean.$(NC)"

##@ Formatting

.PHONY: format-md format-md-all format-py format-py-all format
format-md: ## Format modified markdown files
	@echo "$(BLUE)Formatting modified markdown files...$(NC)"
	@node $(TOOLS_DIR)/format-markdown.cjs
	@echo "$(GREEN)Markdown formatting complete.$(NC)"

format-md-all: ## Format all markdown files in the repo
	@echo "$(BLUE)Formatting all markdown files...$(NC)"
	@node $(TOOLS_DIR)/format-markdown.cjs --all
	@echo "$(GREEN)Markdown formatting complete.$(NC)"

format-py: ## Run Ruff linter and formatter on modified python files
	@echo "$(BLUE)Formatting modified python files...$(NC)"
	@uv run ruff check --fix
	@uv run ruff format
	@echo "$(GREEN)Python formatting complete.$(NC)"

format-py-all: ## Run Ruff linter and formatter on all python files
	@echo "$(BLUE)Formatting all python files...$(NC)"
	@uv run ruff check --fix .
	@uv run ruff format .
	@echo "$(GREEN)Python formatting complete.$(NC)"

format: format-md format-py ## Format all modified markdown and python files

##@ Testing

.PHONY: test test-live test-live-dspy
test: ## Execute the current test suite via pytest
	uv run pytest -m "not live" tests/ -v

test-live: ## Execute the live E2E test suite via pytest against OpenAI API
	uv run pytest -m live tests/ -v

test-live-dspy: ## Execute the live E2E DSPy test suite against Ollama and OpenAI API
	@echo "$(BLUE)Ensure Ollama is running locally with llama3.1:8b (e.g., in a separate terminal or via Tilt)$(NC)"
	uv run pytest -m "live and dspy" tests/ -v

##@ Checks & Validation

.PHONY: hooks-install pre-commit pre-commit-all check typecheck validate
hooks-install: ## Install pre-commit and commit-msg hooks locally
	@$(PRE_COMMIT) install --install-hooks --hook-type pre-commit --hook-type commit-msg

pre-commit: ## Run pre-commit hooks on staged files
	@$(PRE_COMMIT) run

pre-commit-all: ## Run pre-commit hooks on all tracked files
	@$(PRE_COMMIT) run --all-files

check: pre-commit-all ## Run the current repo-wide checks

typecheck: ## Run static type checker
	@echo "$(BLUE)Running typecheck...$(NC)"
	@uv run pyright

validate: format-md-all format-py-all typecheck test ## Run all formatters, linters, typecheckers, and tests
