import streamlit as st

from app.entities.claim_intake_bundle import ClaimIntakeBundle


def render_bundle_viewer(bundle: ClaimIntakeBundle):
    st.subheader("Original Intake Bundle")
    st.caption("Raw data before processing.")

    st.write(f"**Case ID:** {bundle.case_id}")

    if not bundle.documents:
        st.write("No documents found.")
        return

    for doc_name, doc_text in bundle.documents.items():
        with st.expander(f"{doc_name.title().replace('_', ' ')} Text", expanded=True):
            st.text(doc_text)
