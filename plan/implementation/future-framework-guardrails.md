# FUTURE: Framework-Level Guardrails Implementation Plan

This document outlines the strategy for adding framework-level guardrails (e.g., NeMo Guardrails, LlamaGuard) inside the `LiveChatModelAdapter`.

## Goal

Implement universal conversational and safety guardrails that protect all LLM calls across the application universally, without needing to hardcode logic into every individual LangGraph node or Pydantic schema.

## Why Framework-Level?

While Pydantic schemas are great for *data formatting* (e.g., "Must be an Enum") and LangGraph nodes are great for *business logic* (e.g., "Review this claim's facts"), framework-level guardrails protect the **LLM interaction itself**.

By placing this inside `LiveChatModelAdapter`, we ensure:

1. **Prompt Injection Protection:** Every inbound prompt is sanitized before hitting the core LLM.
2. **Off-Topic Detection:** The model refuses to engage in non-insurance, non-triage conversations.
3. **Universal Tone/Toxicity Checks:** All outgoing text is verified to be professional, safe, and non-toxic (e.g., preventing the LLM from generating harmful advice).
4. **Hallucination Checking:** Verifying the output strictly adheres to the input facts before returning.

---

## Recommended Packages

### Option A: NeMo Guardrails (Nvidia)

NeMo Guardrails is an open-source framework specifically designed to add programmable rails to conversational AI systems.

- **Pros:** Expressive domain-specific language (Colang) for defining strict conversational flows, off-topic detection, and fact-checking. Easily integrates with LangChain.
- **Cons:** Can be complex to set up initially with Colang files; adds slight overhead to deployment.

### Option B: LlamaGuard (Meta)

LlamaGuard is an LLM-based safeguard model designed to classify inputs and outputs for safety risks (violence, prompt injection, etc.).

- **Pros:** Excellent, state-of-the-art safety taxonomy. Very fast if deployed on a local vLLM instance or queried via Together AI / Groq.
- **Cons:** Primarily focused on safety/toxicity rather than business-logic off-topic routing (though can be fine-tuned).

---

## Proposed Changes

We will modify the `app/adapters/model/live_chat_model_adapter.py` to wrap the standard LangChain invocation in a guardrail layer.

### 1. Abstracting the Guardrail

Create a transparent layer inside the `LiveChatModelAdapter`'s `generate()` method that intercepts both the prompt and the response.

```python
# app/adapters/model/live_chat_model_adapter.py

from langchain_core.runnables import RunnableGuardrails # (or NeMo equivalent)
import structlog

logger = structlog.get_logger(__name__)

class LiveChatModelAdapter(ModelAdapter):
    def __init__(self, llm: BaseChatModel, guardrails_app=None):
        self._llm = llm
        self._guardrails = guardrails_app # e.g., NeMo Guardrails RailsConfig

    async def generate(self, prompt: str) -> str:
        logger.info("Executing model call with universal guardrails", model=self._llm.model_name)

        # Scenario A: Using NeMo Guardrails
        if self._guardrails:
            # The guardrail app intercepts the prompt, evaluates it, calls the LLM,
            # evaluates the output, and returns the final string.
            response = await self._guardrails.generate_async(messages=[{{"role": "user", "content": prompt}}])

            # Extract content appropriately based on the guardrail's return structure
            final_text = response["content"]

            if "I cannot help you with that" in final_text:
                 logger.warning("Guardrail triggered: Input or Output flagged.")
                 raise GuardrailViolationException("The request or response violated safety protocols.")

            return final_text

        # Fallback to direct call
        result = await self._llm.ainvoke(prompt)
        return result.content
```

### 2. Handling Guardrail Violations

When a guardrail triggers (e.g., detects prompt injection), we should **fail closed**.

- Modify `generate_artifacts_node.py` or the adapter itself to catch `GuardrailViolationException`.
- When caught, the application should cleanly escalate the claim to `human_review` with the rationale: `"System safety protocol triggered; human review required."`

---

## Best Practices

1. **Fail Closed:** If the guardrail service goes down or times out, the model call should fail rather than bypassing the guardrail. Security must take precedence.
2. **Latency Awareness:** LLM-in-the-middle guardrails (like LlamaGuard or SelfCheckGPT for hallucinations) double the latency of a single generation step. Use fast, specialized models (e.g., Llama-Guard-3-8B hosted on Groq or vLLM) for the guardrail layer, leaving the heavy lifting to the main LLM.
3. **Observability:** Tag the LangSmith run explicitly when a guardrail triggers. Use `structlog` to log the reason the guardrail failed (e.g., `guardrail_reason="prompt_injection"`). This is critical for auditing and evaluating system attacks.
4. **Do Not Overlap:** Let the Guardrail handle *safety and scope* (prompt injection, toxicity), let the LangGraph node handle *business logic* (fraud detection, complexity), and let Pydantic handle *data shapes* (Enums, lists). Do not use NeMo to validate JSON shapes, and do not use Pydantic to check for prompt injection.
