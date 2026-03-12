import streamlit as st

from drivers.ui.config import get_config


def render_env_vars_panel():
    """Renders environment variables in the sidebar."""
    st.sidebar.divider()

    config = get_config()

    with st.sidebar.expander("🔧 Environment Variables", expanded=False):
        # Dictionary of config attributes to check.
        # Key: display name, Value: (config_attribute_name, is_sensitive)
        vars_to_show = {
            "ENVIRONMENT": ("environment", False),
            "LOG_LEVEL": ("log_level", False),
            "LLM_MAIN_MODEL": ("llm_main_model", False),
            "LLM_MAIN_API_KEY": ("llm_main_api_key", True),
            "LLM_GUARDRAIL_MODEL": ("llm_guardrail_model", False),
            "LLM_GUARDRAIL_API_BASE": ("llm_guardrail_api_base", False),
            "LLM_GUARDRAIL_API_KEY": ("llm_guardrail_api_key", True),
            "LLM_GUARDRAIL_SECRET_KEY": ("llm_guardrail_secret_key", True),
            "LANGSMITH_TRACING": ("langsmith_tracing", False),
            "LANGSMITH_API_KEY": ("langsmith_api_key", True),
            "LANGCHAIN_PROJECT": ("langchain_project", False),
        }

        for display_name, (attr_name, is_sensitive) in vars_to_show.items():
            val = getattr(config, attr_name, None)

            if not val or (isinstance(val, str) and val.strip() == ""):
                display_val = "MISSING"
            elif is_sensitive:
                val_str = str(val)
                if len(val_str) > 8:
                    display_val = f"{val_str[:3]}...{val_str[-3:]}"
                else:
                    display_val = "********"
            else:
                display_val = str(val)

            if display_val == "MISSING":
                st.markdown(
                    f"**{display_name}**<br><span style='color: #ff4b4b;'>{display_val}</span>", unsafe_allow_html=True
                )
            else:
                st.markdown(f"**{display_name}**<br><code>{display_val}</code>", unsafe_allow_html=True)
