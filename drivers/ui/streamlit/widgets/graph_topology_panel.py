import streamlit as st
from langgraph.graph.state import CompiledStateGraph

from app.infrastructure.telemetry.logger import get_logger, log_exception

logger = get_logger(__name__).bind(widget="graph_topology_panel", surface="streamlit")


def render_graph_topology_panel(graph: CompiledStateGraph):
    st.subheader("Implementation Map: Graph Topology")
    st.markdown("This is a lightweight static map of the active nodes and conditional edges in the execution graph.")

    log = logger.bind(operation="render_graph_topology")
    log.info("started")
    try:
        png_data = graph.get_graph().draw_mermaid_png()
        st.image(png_data, caption="LangGraph Topology")
        log.info("completed")
    except Exception as e:
        log_exception(log, "failed", e)
        st.error(f"Failed to render graph topology: {e}")
