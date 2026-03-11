from typing import Any

from app.adapters.model.parsers.case_summary_parser import case_summary_parser, map_to_case_summary
from app.adapters.model.parsers.checklist_parser import (
    checklist_parser,
    map_to_requirements_checklist_string,
)
from app.adapters.model.parsers.follow_up_message_parser import follow_up_message_parser
from app.adapters.model.parsers.hitl_review_task_parser import hitl_review_task_parser
from app.adapters.model.parsers.routing_rationale_parser import routing_rationale_parser
from app.adapters.model.prompts.case_summary_prompt_template import case_summary_prompt
from app.adapters.model.prompts.follow_up_message_prompt_template import follow_up_message_prompt
from app.adapters.model.prompts.hitl_review_task_prompt_template import hitl_review_task_prompt
from app.adapters.model.prompts.requirements_checklist_prompt_template import (
    requirements_checklist_prompt,
)
from app.adapters.model.prompts.routing_rationale_prompt_template import routing_rationale_prompt
from app.adapters.model.protocol import ModelAdapter
from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState
from app.use_cases.generate_escalation_rationale_uc import GenerateEscalationRationaleUseCase
from app.use_cases.generate_hitl_review_task_uc import GenerateHITLReviewTaskUseCase
from app.use_cases.generate_requirements_checklist_uc import GenerateRequirementsChecklistUseCase


def build_generate_artifacts_node(model: ModelAdapter):
    def generate_artifacts_node(state: TriageGraphState) -> dict[str, Any]:
        """
        Coordinates LLM artifact requests (Summary, FollowUp, Routing Checklist)
        using the injected ModelAdapter based on deterministic extraction,
        LangChain prompt templates, and Pydantic output parsers.
        """
        disposition = state.get("disposition", "unknown")
        document_facts = state.get("document_facts", {})
        updates: dict[str, Any] = {}

        # Always generate a summary
        summary_prompt_str = case_summary_prompt.format(
            document_facts=str(document_facts),
            format_instructions=case_summary_parser.get_format_instructions(),
        )
        summary_response = model.generate(summary_prompt_str)
        summary_parsed = case_summary_parser.parse(summary_response)
        updates["case_summary"] = map_to_case_summary(summary_parsed)

        if disposition == "request_more_information":
            # 1. Checklist
            checklist_facts = GenerateRequirementsChecklistUseCase().execute(document_facts)
            checklist_prompt_str = requirements_checklist_prompt.format(
                checklist_facts=str(checklist_facts),
                format_instructions=checklist_parser.get_format_instructions(),
            )
            checklist_response = model.generate(checklist_prompt_str)
            checklist_parsed = checklist_parser.parse(checklist_response)
            updates["requirements_checklist"] = map_to_requirements_checklist_string(checklist_parsed)

            # 2. Tone / FollowUp Message
            msg_prompt_str = follow_up_message_prompt.format(
                requirements_checklist=updates["requirements_checklist"],
                format_instructions=follow_up_message_parser.get_format_instructions(),
            )
            msg_response = model.generate(msg_prompt_str)
            msg_parsed = follow_up_message_parser.parse(msg_response)
            updates["follow_up_message"] = msg_parsed.message
            updates["follow_up_message_quality_markers"] = msg_parsed.quality_markers

        elif disposition == "escalate_to_human_review":
            # 1. HITL Task
            task_facts = GenerateHITLReviewTaskUseCase().execute(document_facts)
            task_prompt_str = hitl_review_task_prompt.format(
                task_facts=str(task_facts),
                format_instructions=hitl_review_task_parser.get_format_instructions(),
            )
            task_response = model.generate(task_prompt_str)
            task_parsed = hitl_review_task_parser.parse(task_response)
            updates["hitl_review_task"] = task_parsed.task_description

            # 2. Rationale
            rationale_uc = GenerateEscalationRationaleUseCase()
            reasons_facts, rationale_facts = rationale_uc.execute(document_facts)
            rationale_prompt_str = routing_rationale_prompt.format(
                rationale_facts=str(rationale_facts),
                format_instructions=routing_rationale_parser.get_format_instructions(),
            )
            rationale_response = model.generate(rationale_prompt_str)
            rationale_parsed = routing_rationale_parser.parse(rationale_response)
            updates["escalation_rationale"] = rationale_parsed.rationale
            updates["escalation_reasons"] = reasons_facts

        return updates

    return generate_artifacts_node
