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

##@ Checks

.PHONY: hooks-install pre-commit pre-commit-all check
hooks-install: ## Install pre-commit and commit-msg hooks locally
	@$(PRE_COMMIT) install --install-hooks --hook-type pre-commit --hook-type commit-msg

pre-commit: ## Run pre-commit hooks on staged files
	@$(PRE_COMMIT) run

pre-commit-all: ## Run pre-commit hooks on all tracked files
	@$(PRE_COMMIT) run --all-files

check: pre-commit-all ## Run the current repo-wide checks

##@ Markdown

.PHONY: format-md format-md-all
format-md: ## Format modified markdown files
	@echo "$(BLUE)Formatting modified markdown files...$(NC)"
	@node $(TOOLS_DIR)/format-markdown.cjs
	@echo "$(GREEN)Markdown formatting complete.$(NC)"

format-md-all: ## Format all markdown files in the repo
	@echo "$(BLUE)Formatting all markdown files...$(NC)"
	@node $(TOOLS_DIR)/format-markdown.cjs --all
	@echo "$(GREEN)Markdown formatting complete.$(NC)"

##@ Python Formatting

.PHONY: format-py format-py-all format
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

##@ Local Runtime / Scaffolds

.PHONY: install dev debug api ui test tilt up
install: ## Bootstrap and install the virtual environment dependencies
	uv sync

dev: ## Start the LangGraph development loop locally
	uv run langgraph dev

debug: ## Start LangGraph development loop with a debugger port open
	PYDEVD_DISABLE_FILE_VALIDATION=1 uv run python -Xfrozen_modules=off -m langgraph_cli dev --debug-port 5678

api: ## Boot the thin FastAPI ingress shell
	uv run uvicorn drivers.api.main:app --reload --port 8000

ui: ## Boot the thin Streamlit workbench shell
	uv run streamlit run drivers/ui/streamlit/app.py

test: ## Execute the current test suite via pytest
	uv run pytest tests/ -v

tilt: ## Start Tilt for local infrastructure deployment
	tilt up

tilt-down: ## Tear down Tilt infrastructure deployment
	tilt down

prepare-rancher-desktop: ## Re-point Docker CLI plugins to Rancher Desktop binaries
	bash tools/prepare-rancher-desktop.sh

up: ## Start the minimal docker-compose services manually
	docker compose -f deploy/local/compose.yaml up -d
