from langgraph.graph import StateGraph, START, END

from app.graph.state import GraphState

from app.nodes.complaint_analysis_node import (
    complaint_analysis_node,
)
from app.nodes.investigation_node import (
    investigation_node,
)
from app.nodes.response_generator_node import (
    response_generator_node,
)


def build_graph():
    """
    Build and compile the LangGraph workflow.
    """

    workflow = StateGraph(GraphState)

    # ======================================================
    # Nodes
    # ======================================================

    workflow.add_node(
        "complaint_analysis_node",
        complaint_analysis_node,
    )

    workflow.add_node(
        "investigation_node",
        investigation_node,
    )

    workflow.add_node(
        "response_generator_node",
        response_generator_node,
    )

    # ======================================================
    # Edges
    # ======================================================

    workflow.add_edge(
        START,
        "complaint_analysis_node",
    )

    workflow.add_edge(
        "complaint_analysis_node",
        "investigation_node",
    )

    workflow.add_edge(
        "investigation_node",
        "response_generator_node",
    )

    workflow.add_edge(
        "response_generator_node",
        END,
    )

    # ======================================================
    # Compile Graph
    # ======================================================

    graph = workflow.compile()

    return graph


graph = build_graph()