import os
import uuid

import streamlit as st

from app.infrastructure.telemetry.logger import bind_context, configure_logging, get_logger

# Initialize logging
env = os.getenv("ENVIRONMENT", "development")
configure_logging(environment=env)
logger = get_logger(__name__)

st.set_page_config(page_title="Death Claim Triage Workbench", layout="wide")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    logger.info("new_ui_session_started", session_id=st.session_state.session_id)

bind_context(session_id=st.session_state.session_id)

st.title("Death Claim Triage")
st.write("This is a thin shell for the Streamlit UI, tracking the future graph-owned behavior.")
