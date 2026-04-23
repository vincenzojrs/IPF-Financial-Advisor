from langgraph.graph import END, START, StateGraph
from src.agent.utils.nodes import (municipality_node, province_node, rag_node, router_node, zone_and_uses_node, human_input_node, extract_parameters, calculate)
from src.agent.utils.state import AgentState

def routing_logic(state):
    return "rag" if state["route"] == "rag" else "mutuo"

graph = StateGraph(AgentState)
graph.add_node("router_node", router_node)

graph.add_node("human_input_node", human_input_node)
graph.add_node("province_node", province_node)
graph.add_node("municipality_node", municipality_node)
graph.add_node("zone_and_uses_node", zone_and_uses_node)
graph.add_node("extract_parameters", extract_parameters)
graph.add_node("calculate", calculate)

graph.add_node("rag_node", rag_node)

graph.add_edge(START, "router_node")
graph.add_conditional_edges(
    "router_node", routing_logic, {"rag": "rag_node", "mutuo": "human_input_node"}
)

graph.add_edge("rag_node", END)

graph.add_edge("human_input_node", "province_node")
graph.add_edge("province_node", "municipality_node")
graph.add_edge("municipality_node", "zone_and_uses_node")
graph.add_edge("zone_and_uses_node", "extract_parameters")
graph.add_edge("extract_parameters", "calculate")
graph.add_edge("calculate", END)

compiled = graph.compile()