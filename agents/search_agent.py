# agents/search_agent.py
from agents.llm import llm
from client.client_sse import MCPClient

async def search_agent(question: str) -> str:
    """
    Uses LLM to decide what to search,
    then calls Tavily via MCP.
    """
    search_query = llm.invoke(
        f"Convert this question into a concise search query: {question}"
    ).content.strip()

    async with MCPClient() as client:
        # await client.connect("mcp_server/server_http.py")
        result = await client.call_tool("tavily_search", {"query": search_query, "max_results": 3})
        return result














