import pytest

from app.entities.claim_intake_bundle import ClaimIntakeBundle


@pytest.mark.feature("death_claim_intake_triage")
class TestDeathClaimIntakeWorkshopSpec:
    """
    Workshop contract for death-claim intake + next-step orchestration.

    This test is meant to be discussed with stakeholders before committing
    to a vertical slice or framework-specific architecture.
    """

    @pytest.mark.asyncio
    async def test_triage_representative_claim_cases(
        self,
        triage_workflow,
        fake_policy_lookup,
        fake_document_store,
        fake_review_queue,
        fake_pii_guardrail,
        fake_evaluation_recorder,
    ):
        # Case A: complete intake
        complete_case = ClaimIntakeBundle.fake_complete()
        complete_result = await triage_workflow.assess(complete_case)

        assert complete_result.disposition == "proceed"
        assert complete_result.confidence_band == "High"
        assert complete_result.case_summary
        assert complete_result.routing_decision
        assert not complete_result.escalation_reasons
        assert not complete_result.hitl_review_task

        # Case B: missing information
        missing_info_case = ClaimIntakeBundle.fake_missing_information()
        missing_result = await triage_workflow.assess(missing_info_case)

        assert missing_result.disposition == "request_more_information"
        assert missing_result.confidence_band == "Medium"
        assert missing_result.requirements_checklist
        assert missing_result.follow_up_message
        assert missing_result.reviewability_flags
        assert missing_result.escalation_reasons == []
        assert "empathetic" in missing_result.follow_up_message_quality_markers

        # Case C: ambiguous / HITL
        ambiguous_case = ClaimIntakeBundle.fake_ambiguous()
        ambiguous_result = await triage_workflow.assess(ambiguous_case)

        assert ambiguous_result.disposition == "escalate_to_human_review"
        assert ambiguous_result.confidence_band == "Low"
        assert ambiguous_result.hitl_review_task
        assert ambiguous_result.escalation_reasons
        assert ambiguous_result.escalation_rationale

        # Governance / compliance assertion
        assert fake_pii_guardrail.external_model_input_contains_no_raw_pii()
        assert fake_pii_guardrail.used_stable_safe_tokens()

        # Scope boundary assertion
        assert "adjudication" not in str(complete_result.routing_decision).lower()
        assert "benefit determination" not in str(ambiguous_result.escalation_rationale).lower()

        # Evaluation / observability assertion
        # Evaluation / observability assertion
        assert fake_evaluation_recorder.has_recorded_case("complete")
        assert fake_evaluation_recorder.has_recorded_case("missing_information")
        assert fake_evaluation_recorder.has_recorded_case("ambiguous")
