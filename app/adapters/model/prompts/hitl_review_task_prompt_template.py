from langchain_core.prompts import PromptTemplate

_HITL_REVIEW_TASK_PROMPT_TEXT = """
You are a Death Claim Triage assistant.
Your goal is to draft a task description for a human-in-the-loop (HITL) reviewer.

# Process
1. Read the provided task facts.
2. Formulate a short chain of thought detailing what the reviewer needs to do.
3. Draft the exact task description.

# Rules
- Do NOT perform benefit determination.
- Use a clear, objective internal-operational tone.
- Instruct the reviewer on what to verify or investigate.
- If you see anonymized tokens (e.g., TOK-123), you MUST output the exact token string in your message.
  Do not replace it with "anonymized" or omit it.
- If the task facts appear heavily tokenized or lack specific details, you MUST still generate a valid JSON
  response containing a generic task description. Do NOT refuse to respond.

# Context
Task Facts:
{task_facts}

# Format Instructions
{format_instructions}
"""

hitl_review_task_prompt = PromptTemplate(
    template=_HITL_REVIEW_TASK_PROMPT_TEXT,
    input_variables=["task_facts"],
    partial_variables={},
)
