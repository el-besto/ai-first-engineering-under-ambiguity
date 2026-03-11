import dataclasses
import typing
import uuid

import streamlit as st

from app.entities.claim_intake_bundle import ClaimIntakeBundle
from app.infrastructure.telemetry.logger import bind_context, configure_logging, get_logger
from app.interface_adapters.orchestrators.triage_graph_state import (
    TriageGraphState,
    map_state_to_triage_result,
)
from drivers.ui.config import UIConfig
from drivers.ui.streamlit.dependencies import get_triage_graph


@st.cache_resource
def get_config() -> UIConfig:
    return UIConfig()


config = get_config()

# Initialize logging
configure_logging(
    environment=config.environment,
    log_level=config.log_level,
    log_format=config.log_format,
)
logger = get_logger(__name__)

st.set_page_config(page_title="Death Claim Triage Workbench", layout="wide")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    logger.info("new_ui_session_started", session_id=st.session_state.session_id)

bind_context(session_id=st.session_state.session_id)

st.title("Death Claim Triage")
st.write("Submit a canonical test case to trace the LangGraph orchestrator.")

graph = get_triage_graph(config)

policy_number = st.text_input(
    "Enter Policy Number (e.g. CASE_A_COMPLETE, CASE_B_MISSING, CASE_C_AMBIGUOUS)"
)
if st.button("Run Triage"):
    policy_str = policy_number.upper()
    if "MISSING" in policy_str:
        bundle = ClaimIntakeBundle.fake_missing_information()
    elif "AMBIGUOUS" in policy_str:
        bundle = ClaimIntakeBundle.fake_ambiguous()
    else:
        bundle = ClaimIntakeBundle.fake_complete()

    with st.spinner("Processing triage graph..."):
        initial_state = {"claim_bundle": bundle}
        result_state = typing.cast(TriageGraphState, graph.invoke(initial_state))
        # map back
        result = map_state_to_triage_result(result_state)

        st.success(f"Triage Complete: {result.disposition}")
        with st.expander("Triage Result JSON", expanded=True):
            # Using dataclasses.asdict correctly since TriageResult contains nested dataclasses
            # that Streamlit sometimes struggles to serialize automatically.
            st.json(
                {
                    "disposition": result.disposition,
                    "confidence_band": result.confidence_band,
                    "case_summary": (
                        dataclasses.asdict(result.case_summary) if result.case_summary else None
                    ),
                    "routing_decision": (
                        dataclasses.asdict(result.routing_decision)
                        if result.routing_decision
                        else None
                    ),
                    "requirements_checklist": result.requirements_checklist,
                    "follow_up_message": result.follow_up_message,
                    "hitl_review_task": result.hitl_review_task,
                    "reviewability_flags": result.reviewability_flags,
                    "escalation_reasons": result.escalation_reasons,
                    "escalation_rationale": result.escalation_rationale,
                }
            )
