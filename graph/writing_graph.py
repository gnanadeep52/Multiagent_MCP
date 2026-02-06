# graph/writing_graph.py
from langgraph.graph import StateGraph, START, END
from graph.state import GraphState
from agents.note_taker_agent import note_taker_agent
from agents.doc_writer_agent import doc_writer_agent

async def outline_node(state: GraphState) -> GraphState:
    """Create outline"""
    await note_taker_agent(state["question"], "outline.txt")
    state["outline"] = ["Introduction", "Key Findings", "Conclusion"]
    return state

async def write_node(state: GraphState) -> GraphState:
    """Write final document"""
    await doc_writer_agent(state["question"], state["outline"], "answer.txt")
    state["final_answer"] = "Document written to answer.txt"
    return state

# Build writing graph
writing_builder = StateGraph(GraphState)
writing_builder.add_node("outline", outline_node)
writing_builder.add_node("write", write_node)

writing_builder.add_edge(START, "outline")
writing_builder.add_edge("outline", "write")
writing_builder.add_edge("write", END)

writing_graph = writing_builder.compile()





