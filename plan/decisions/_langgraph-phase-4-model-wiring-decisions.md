<!-- AGENT INSTRUCTION: You MUST read `templates/decision/decision-document-template.README.md` before using this template to create a new decision record. Do not alter the structure of this document. -->
# Phase 4 Live Model Wiring: Decisions Needed

> **Template Version:** 1.0 (2025-10-13)
>
> **Usage Instructions:** See `templates/decision/decision-document-template.README.md` for how to use this template and how it fits into the repo's decision-record workflow.
>
> **Related Template:** Use this document when a cross-cutting repo or implementation decision needs explicit options, rationale, and status tracking.

---

**Status:** ✅ 2 of 2 Resolved | 0 Awaiting Discussion

This document captures the key architectural decisions for the LangGraph Phase 4 live model wiring, specifically addressing how to support both the immediate OpenAI requirement and the future DSPy/local SLM stretch goal.

---

## Decision 1: Model Abstraction Layer & Adapter Strategy ⚠️ CRITICAL

**Agent Analysis:**

- The current plan (`langgraph-phase-4-live-model-wiring.md`) calls for an `openai_adapter.py`.
- However, our stretch goal requires routing PII extraction specifically to a local SLM via DSPy (using models like Ollama or LM Studio).
- If we build an OpenAI-specific adapter now, we will be forced to build an `ollama_adapter.py` later and implement custom factory logic to inject different adapters into different nodes of the graph.
- We need to decide whether to map our internal `ModelAdapter` protocol to a specific provider driver (OpenAI) or a generic abstraction layer.

**Context:**
The core graph expects a `ModelAdapter` with a `generate(prompt: str) -> str` signature. We need a live implementation of this adapter.

**Decision Required:**
Which library should power the live model adapter, and should we build one generic adapter or multiple provider-specific adapters?

- [x] **Option A: Single Generic Adapter via `langchain-core` (`init_chat_model`)**
  - Build a single `live_chat_model_adapter.py`. It uses `langchain.chat_models.init_chat_model(model=..., api_key=...)` under the hood.
  - ✅ Pro: No new dependencies (we already have LangChain installed for LangGraph).
  - ✅ Pro: First-class Native LangGraph Support. LangGraph relies heavily on native provider packages (`langchain-openai`, `langchain-anthropic`) to handle complex structured outputs and tool binding perfectly. `init_chat_model` yields these native classes.
  - ✅ Pro: DSPy explicitly supports native local SLM pipelines without needing LiteLLM formatting.
  - ❌ Con: If we want to use a provider that doesn't have a dedicated `langchain-{provider}` package, we might have to install it later.

- [ ] **Option B: Single Generic Adapter via `LiteLLM`**
  - Build a single `live_litellm_adapter.py`. It uses `litellm.completion()` to route to 100+ providers using the OpenAI API format.
  - ✅ Pro: Maximum flexibility. Supports local SLMs (Ollama/vLLM) and Anthropic/OpenAI out-of-the-box using standard connection strings without provider-specific LangChain packages.
  - ✅ Pro: DSPy has integrated LiteLLM support out of the box (`dspy.LM`), meaning we get guaranteed format consistency.
  - ❌ Con: Added Complexity/Security. To use this in LangGraph, we must use `ChatLiteLLM`. This places **two** abstraction layers between LangGraph and the provider (`LangGraph` -> `ChatLiteLLM` -> `LiteLLM` -> `Provider`). LangGraph tool execution and structured generation often breaks across generic wrappers when providers implement advanced tool binding differently. Inheriting bugs from LiteLLM's mapping logic is a real risk.
  - ❌ Con: Introduces a new dependency (`litellm`) to the project.

- [ ] **Option C: Multiple Provider-Specific Adapters (Current Plan)**
  - Build `openai_adapter.py` now. When the stretch goal arrives, build `ollama_adapter.py` or `dspy_adapter.py`.
  - ✅ Pro: Explicit, highly contained adapter code with zero magic routing.
  - ❌ Con: Requires duplicating adapter logic, extending `dependencies.py` with custom factory routing, and tightly coupling edge files to specific provider SDKs.

**Agent Recommendation:** Option A or Option B.

**Reasoning:**
Given the stretch goal explicitly calls for a local SLM, Options A and B drastically simplify the Dependency Injection layer, allowing `dependencies.py` to remain provider-agnostic. Option A is the lowest friction since LangChain is already heavily embedded in the project.

**User Decision:** ✅ **Option A: Single Generic Adapter via `langchain-core`**

**Rationale:**
We will use LangChain since it provides one fewer abstraction layer (avoiding `ChatLiteLLM`), does not add an additional dependency (`litellm`), and DSPy has integrated support for LangChain out-of-the-box.

**Impact:** CRITICAL - Determines the edge-layer architecture and how dependencies are injected throughout the LangGraph workflow.

**Status:** ✅ RESOLVED

---

## Decision 2: Environment Variable Strategy & Topology

**Agent Analysis:**

- We need to define exactly what environment variables are expected, how they are loaded securely, and where they are used.

**Context:**
Currently, our `pydantic-settings` uses `app/config.py` to load standard variables.

**Decision Required:**
How should we structure and name the environment variables to support multiple models (main vs. guardrail) and how will they be injected?

- [x] **Option A: Explicit Custom Domain Variables (Recommended)**
  - **Expected Vars:** Let's prefix with `LLM_` to keep them grouped based on usage domain.
    - `LLM_MAIN_MODEL` (e.g., `"gpt-4o"`)
    - `LLM_MAIN_API_KEY`
    - `LLM_GUARDRAIL_MODEL` (e.g., `"ollama/llama3"`)
    - `LLM_GUARDRAIL_API_BASE` (e.g., `"http://localhost:11434"`)
    - `LLM_GUARDRAIL_API_KEY` (e.g., `"local-dev"`)
  - **Where Used:** Loaded securely via `pydantic-settings` (`Field(repr=False)` for keys) in `APIConfig`/`UIConfig`.
  - **How Used:** Passed explicitly to the constructor of the generic adapter via DI container setup in `dependencies.py`.
  - ✅ Pro: Total decoupling and routing isolation. If we want to use OpenAI for both the main model AND the guardrail, but track costs under two different OpenAI API keys, explicit assignment guarantees 100% control of which key goes to which node.
  - ❌ Con: We lose "zero-config magic." If a developer writes a standalone scratchpad script, `LangChain`/`OpenAI` SDKs won't automatically read `LLM_MAIN_API_KEY`. They'd have to map it manually or export canonical names (e.g., `OPENAI_API_KEY=...`).

- [ ] **Option B: Standard Provider-Specific Auto-Read Variables (Legacy)**
  - **Expected Vars:**
    - `OPENAI_API_KEY`
    - `ANTHROPIC_API_KEY`
    - `OPENAI_MODEL_NAME` // Or passed directly via config
  - **Where Used:** Injected implicitly by the provider SDKs by reading `os.environ`.
  - **How Used:** The adapter classes themselves just initialize without passing keys, relying on LangChain's auto-read.
  - ✅ Pro: Zero-config magic. Standard scratchpad scripts "just work."
  - ❌ Con: Implicit Behavior & Conflicts. If the entire application shares one `OPENAI_API_KEY`, but you want to route the PII guardrail through a secondary provider (or different OpenAI Org), implicit reads make this extremely difficult. It tightly couples app routing to the host environment.

**Agent Recommendation:** Option A.

**Reasoning:**
Generic routing variables decouple the infrastructure from the code. A developer running the PoC locally should be able to swap `MAIN_MODEL_NAME` to an Anthropic or local model purely via `.env` without modifying Python code.

**User Decision:** ✅ **Option A: Explicit Custom Domain Variables (Recommended)**

**Rationale:**
Explicit mapping is preferred to ensure complete routing isolation. For one-off scripts, developers can be responsible for setting the appropriate environment variables manually.

*New Deferred Risk Added:* By using explicit API keys in `.env` configurations, we must ensure these are eventually migrated to a proper secrets manager (like ExternalSecrets, 1Password, or Azure Key Vault) so that execution environments load them dynamically instead of storing them on disk.

**Impact:** HIGH - Defines the `.env` contract for all developers deploying the system.

**Status:** ✅ RESOLVED

---

## Next Steps

**Completed:**

- ✅ Analyzed the DSPy/local SLM stretch goal requirements against the current Phase 4 plan.
- ✅ Drafted architectural options for model abstraction and environment configuration.

**Awaiting Input (0 decisions):**

- None

**After Decisions Resolved:**

1. ✅ Update `plan/implementation/langgraph-phase-4-live-model-wiring.md` to reflect the chosen strategy.
2. Proceed to Execution phase for Phase 4.

**Status:** 2 of 2 decisions resolved | 0 awaiting collaborative review
