import streamlit as st

from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState


def render_token_audit_panel(state: TriageGraphState):
    st.subheader("Security: PII Scrubbing Audit")

    bundle = state.get("claim_bundle")
    if not bundle:
        st.warning("No bundle found in state to audit.")
        return

    raw_facts = state.get("document_facts")
    tokenized_facts = state.get("tokenized_document_facts")

    if not raw_facts or not tokenized_facts:
        st.info("Waiting for facts to be extracted and tokenized...")
        return

    st.success(
        "The extracted facts were tokenized for PII BEFORE being sent to the LLM. "
        "The tokenized facts represent the payload safely passed to the generative models."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Original Facts")
        st.json(raw_facts)

    with col2:
        st.markdown("##### Tokenized Facts (Model Payload)")
        st.json(tokenized_facts)
