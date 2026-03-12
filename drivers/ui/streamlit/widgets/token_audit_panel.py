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
    tokenized_docs = tokenized_facts.get("document_texts", {}) if tokenized_facts else {}

    if not raw_facts or not tokenized_facts:
        st.info("Waiting for facts to be extracted and tokenized...")
        return

    st.success(
        "The extracted facts and full document text were tokenized for PII BEFORE being sent to the LLM. "
        "The tokenized data represents the payload safely passed to the generative models."
    )

    if tokenized_docs:
        st.markdown("### Tokenized Document Text")
        for doc_name, doc_text in tokenized_docs.items():
            with st.expander(f"Tokenized {doc_name.title().replace('_', ' ')}", expanded=False):
                st.text(doc_text)

    st.markdown("### Facts (Metadata)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Original Facts")
        st.json(raw_facts)

    with col2:
        st.markdown("##### Tokenized Facts (Model Payload)")
        st.json(tokenized_facts)
