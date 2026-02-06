

# graph/research_graph.py
from langgraph.graph import StateGraph, START, END
from graph.state import GraphState
from agents.search_agent import search_agent
from agents.web_scraper_agent import web_scraper_agent

async def search_node(state: GraphState) -> GraphState:
    """Search the web"""
    results = await search_agent(state["question"])
    state["search_results"] = results
    return state

async def scrape_node(state: GraphState) -> GraphState:
    """Scrape URLs from search results"""
    if state["search_results"]:
        content = await web_scraper_agent(state["search_results"])
        state["scraped_content"] = content
    return state

# Build research graph
research_builder = StateGraph(GraphState)
research_builder.add_node("search", search_node)
research_builder.add_node("scrape", scrape_node)

research_builder.add_edge(START, "search")
research_builder.add_edge("search", "scrape")
research_builder.add_edge("scrape", END)

research_graph = research_builder.compile()












