import streamlit as st

from app.config import BaseConfig


class UIConfig(BaseConfig):
    """
    UI-specific configuration class.
    Extends BaseConfig to include settings specific to the Streamlit application.
    """

    api_url: str = "http://127.0.0.1:8000"


@st.cache_resource
def get_config() -> UIConfig:
    """
    Returns a cached instance of UIConfig.
    """
    return UIConfig()
