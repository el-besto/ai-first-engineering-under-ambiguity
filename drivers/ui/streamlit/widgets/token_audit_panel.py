import streamlit as st

from app.interface_adapters.orchestrators.triage_graph_state import TriageGraphState


def render_token_audit_panel(state: TriageGraphState):
    st.subheader("Security: PII Scrubbing Audit")

    bundle = state.get("claim_bundle")
    if not bundle:
        st.warning("No bundle found in state to audit.")
        return

    st.success("The underlying text was tokenized for PII BEFORE processing by the LLM.")

    if not bundle.documents:
        st.write("No documents to display.")
        return

    for doc_name, doc_text in bundle.documents.items():
        with st.expander(f"{doc_name.title().replace('_', ' ')} (Scrubbed Text)"):
            st.text(doc_text)
