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
