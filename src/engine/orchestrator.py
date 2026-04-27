from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from src.engine.utils.nodes import calculate, elaborate, human_input_node, rag_node, router_node, scraping_parameters
from src.engine.utils.state import AgentState


def routing_logic(state):
    return "rag" if state["route"] == "rag" else "mutuo"


graph = StateGraph(AgentState)
graph.add_node("router_node", router_node)

graph.add_node("rag_node", rag_node)

graph.add_node("human_input_node", human_input_node)
graph.add_node("scraping_parameters", scraping_parameters)
graph.add_node("calculate", calculate)

graph.add_node("elaborate", elaborate)

graph.add_edge(START, "router_node")
graph.add_conditional_edges(
    "router_node", routing_logic, {"rag": "rag_node", "mutuo": "human_input_node"}
)

graph.add_edge("rag_node", END)

graph.add_edge("human_input_node", "scraping_parameters")
graph.add_edge("scraping_parameters", "calculate")
graph.add_edge("calculate", "elaborate")
graph.add_edge("elaborate", END)

memory = InMemorySaver()

graph_runnable = graph.compile(checkpointer=memory)

print(graph_runnable.get_graph().draw_ascii())

def invoke_graph(prompt, config=None):
    return graph_runnable.invoke(prompt, config=config)
