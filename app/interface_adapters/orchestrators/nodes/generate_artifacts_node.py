from typing import Any

from app.adapters.model.protocol import ModelAdapter
from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState
from app.use_cases.generate_escalation_rationale_uc import GenerateEscalationRationaleUseCase
from app.use_cases.generate_hitl_review_task_uc import GenerateHITLReviewTaskUseCase
from app.use_cases.generate_requirements_checklist_uc import GenerateRequirementsChecklistUseCase


def build_generate_artifacts_node(model: ModelAdapter):
    def generate_artifacts_node(state: TriageGraphState) -> dict[str, Any]:
        """
        Coordinates LLM artifact requests (Summary, FollowUp, Routing Checklist)
        using the injected ModelAdapter based on deterministic extraction.
        """
        disposition = state.get("disposition", "unknown")
        document_facts = state.get("document_facts", {})
        updates: dict[str, Any] = {}

        # Always generate a summary
        updates["case_summary"] = model.generate(f"Generate summary for facts: {document_facts}")

        if disposition == "request_more_information":
            # Use deterministic extraction to get the structural baseline
            checklist_facts = GenerateRequirementsChecklistUseCase().execute(document_facts)

            # 1. Checklist
            checklist_prompt = f"Format requirements checklist for: {checklist_facts}"
            updates["requirements_checklist"] = model.generate(checklist_prompt)

            # 2. Tone / FollowUp Message
            msg_prompt = (
                f"Generate empathetic follow-up message requesting: "
                f"{updates['requirements_checklist']}"
            )
            updates["follow_up_message"] = model.generate(msg_prompt)
            updates["follow_up_message_quality_markers"] = [
                "empathetic",
                "clear",
                "non-adjudicative",
            ]

        elif disposition == "escalate_to_human_review":
            # Generate Escalation elements using deterministic extraction as a base
            task_facts = GenerateHITLReviewTaskUseCase().execute(document_facts)

            rationale_uc = GenerateEscalationRationaleUseCase()
            reasons_facts, rationale_facts = rationale_uc.execute(document_facts)

            updates["hitl_review_task"] = model.generate(
                f"Format HITL review task for: {task_facts}"
            )
            updates["escalation_rationale"] = model.generate(
                f"Format rationale for: {rationale_facts}"
            )
            updates["escalation_reasons"] = reasons_facts

        return updates

    return generate_artifacts_node
