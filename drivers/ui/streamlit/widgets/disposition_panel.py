import streamlit as st

from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState


def render_disposition_panel(state: TriageGraphState):
    st.subheader("Automated Triage Disposition")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Disposition", state.get("disposition", "N/A"))
    with col2:
        st.metric("Confidence Band", state.get("confidence_band", "N/A"))

    routing = state.get("routing_decision")
    if routing:
        st.info(f"**Routing Target:** {routing.target_queue}\n\n**Rationale:** {routing.rationale}")

    summary = state.get("case_summary")
    if summary:
        with st.expander("Case Summary", expanded=True):
            st.write(summary.summary_text)

    hitl_task = state.get("hitl_review_task")
    if hitl_task:
        with st.expander("HITL Review Task", expanded=True):
            st.warning(hitl_task)

    checklist = state.get("requirements_checklist")
    if checklist:
        with st.expander("Requirements Checklist"):
            st.markdown(checklist)

    follow_up = state.get("follow_up_message")
    if follow_up:
        with st.expander("Follow-up Message"):
            st.write(follow_up)
            if state.get("follow_up_message_quality_markers"):
                st.caption(f"Quality Markers: {', '.join(state.get('follow_up_message_quality_markers', []))}")

    escalation_reasons = state.get("escalation_reasons")
    if escalation_reasons:
        with st.expander("Escalation Reasons", expanded=True):
            for reason in escalation_reasons:
                st.write(f"- {reason}")
            if state.get("escalation_rationale"):
                st.write(f"**Rationale:** {state.get('escalation_rationale')}")
