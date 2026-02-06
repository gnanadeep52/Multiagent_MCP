# graph/supervisor.py
from langgraph.graph import StateGraph, START, END
from graph.state import GraphState
from graph.research_graph import research_graph
from graph.writing_graph import writing_graph

async def research_team_node(state: GraphState) -> GraphState:
    """Run research team"""
    result = await research_graph.ainvoke(state)
    return result

async def writing_team_node(state: GraphState) -> GraphState:
    """Run writing team"""
    result = await writing_graph.ainvoke(state)
    return result

# Build main supervisor graph
supervisor_builder = StateGraph(GraphState)
supervisor_builder.add_node("research_team", research_team_node)
supervisor_builder.add_node("writing_team", writing_team_node)

supervisor_builder.add_edge(START, "research_team")
supervisor_builder.add_edge("research_team", "writing_team")
supervisor_builder.add_edge("writing_team", END)

supervisor_graph = supervisor_builder.compile()






