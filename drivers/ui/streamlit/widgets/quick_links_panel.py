import streamlit as st


def render_quick_links_panel():
    """Renders quick links in the sidebar."""
    st.sidebar.divider()

    st.sidebar.markdown("### 🔗 Quick Links")

    links = {
        "FastAPI Swagger Docs": "http://localhost:8000/docs",
        "Tilt Dashboard": "http://localhost:10350",
        "LangGraph Studio": "https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024",
    }

    for name, url in links.items():
        st.sidebar.markdown(f"- [{name}]({url})")
