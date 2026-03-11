import typing

import streamlit as st

from app.entities.claim_intake_bundle import ClaimIntakeBundle
from app.infrastructure.telemetry.logger import get_logger, log_exception
from app.interface_adapters.orchestrators.triage_graph_state import (
    TriageGraphState,
)
from drivers.ui.config import UIConfig
from drivers.ui.streamlit.dependencies import get_triage_graph
from drivers.ui.streamlit.widgets.bundle_viewer import render_bundle_viewer
from drivers.ui.streamlit.widgets.disposition_panel import render_disposition_panel
from drivers.ui.streamlit.widgets.token_audit_panel import render_token_audit_panel

logger = get_logger(__name__).bind(page="triage_workbench", surface="streamlit")


@st.cache_resource
def get_config() -> UIConfig:
    return UIConfig()


config = get_config()

st.set_page_config(page_title="Triage Workbench", layout="wide")
st.title("Death Claim Triage Workbench")

st.markdown("Select a canonical claim scenario to test the triage workflow:")

col1, col2, col3 = st.columns(3)

bundle_to_run = None

with col1:
    if st.button("Run: Complete Claim", use_container_width=True):
        bundle_to_run = ClaimIntakeBundle.fake_complete()
with col2:
    if st.button("Run: Missing Info", use_container_width=True):
        bundle_to_run = ClaimIntakeBundle.fake_missing_information()
with col3:
    if st.button("Run: Ambiguous Scenario", use_container_width=True):
        bundle_to_run = ClaimIntakeBundle.fake_ambiguous()

if bundle_to_run:
    st.divider()
    log = logger.bind(operation="run_triage_workbench", case_id=bundle_to_run.case_id)

    # Left column: Bundle, Right column: Disposition & Audit
    left_col, right_col = st.columns([1, 1.5])

    with left_col:
        render_bundle_viewer(bundle_to_run)

    with right_col:
        with st.spinner("Processing through LangGraph Triage Workflow..."):
            log.info("started")
            try:
                graph = get_triage_graph(config)
                initial_state = {"claim_bundle": bundle_to_run}
                # Execute the graph.
                result = typing.cast(TriageGraphState, graph.invoke(initial_state))
                log.info(
                    "completed",
                    selected_disposition=result.get("disposition", "unknown"),
                    confidence_band=result.get("confidence_band", "unknown"),
                )
            except Exception as e:
                log_exception(log, "failed", e)
                raise

        st.success("Triage Workflow Completed!")

        tab1, tab2 = st.tabs(["Disposition", "Security Audit"])

        with tab1:
            render_disposition_panel(result)

        with tab2:
            render_token_audit_panel(result)
