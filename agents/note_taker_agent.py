# agents/note_taker_agent.py
from agents.llm import llm
from client.client_sse import MCPClient

async def note_taker_agent(topic: str, outline_file: str = "outline.txt") -> str:
    """
    Uses LLM to create an outline,
    then saves it using MCP.
    """
    outline_text = llm.invoke(
        f"Create a 5-point outline for: {topic}"
    ).content

    points = [
        line.strip("- ").strip()
        for line in outline_text.splitlines()
        if line.strip()
    ]

    async with MCPClient() as client:
        await client.call_tool("create_outline", {
            "points": points,
            "file_name": outline_file
        })

    
    return {
        "outline_points": points,
        "outline_file": outline_file
    }







