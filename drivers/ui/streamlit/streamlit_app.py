import uuid

import streamlit as st

from app.infrastructure.telemetry.logger import bind_context, clear_context, configure_logging, get_logger
from drivers.ui.config import get_config

config = get_config()

# Initialize logging
configure_logging(
    environment=config.environment,
    log_level=config.log_level,
    log_format=config.log_format,
)
logger = get_logger(__name__).bind(driver="StreamlitApp", surface="streamlit")

st.set_page_config(page_title="Death Claim Triage", layout="wide")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    logger.bind(operation="streamlit_session").info("started", session_id=st.session_state.session_id)

clear_context()
bind_context(session_id=st.session_state.session_id, surface="streamlit")

st.title("Death Claim Triage")
st.markdown(
    """
    Welcome to the Death Claim Triage portal.

    Please select the **Triage Workbench** from the sidebar to begin processing canonical test cases
    through the LangGraph orchestrator.
    """
)
