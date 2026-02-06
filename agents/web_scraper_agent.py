# agents/web_scraper_agent.py
from agents.llm import llm
from client.client_sse import MCPClient

async def web_scraper_agent(search_results: str) -> str:
    """
    Uses LLM to extract URLs from search results,
    
    then scrapes them via MCP.
    """
    urls_text = llm.invoke(
        f"Extract up to 3 URLs from these search results (one per line):\n{search_results}"
    ).content

    urls = [u.strip() for u in urls_text.splitlines() if u.strip().startswith("http")]
    
    if not urls:
        return "No URLs found"

    async with MCPClient() as client:
        # await client.connect("mcp_server/server_http.py")
        result = await client.call_tool("scrape_webpages", {"urls": urls})
        return result



