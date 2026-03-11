import uuid

import streamlit as st

from app.infrastructure.telemetry.logger import bind_context, configure_logging, get_logger
from drivers.ui.config import UIConfig


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
st.write("This is a thin shell for the Streamlit UI, tracking the future graph-owned behavior.")
