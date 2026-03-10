from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    status: str


def dummy_node(state: State) -> State:
    return {"status": "pending_implementation"}


builder = StateGraph(State)
builder.add_node("dummy", dummy_node)
builder.add_edge(START, "dummy")
builder.add_edge("dummy", END)

graph = builder.compile()
