# client/client.py
import asyncio
import sys
from pathlib import Path
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self):
        self.session = None
        self.exit_stack = AsyncExitStack()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()

    async def connect(self, server_path: str):
        """Connect to MCP server"""
        path = Path(server_path).resolve()
        
        if not path.exists():
            raise FileNotFoundError(f"Server not found: {path}")
        
        params = StdioServerParameters(command="python", args=[str(path)])
        read, write = await self.exit_stack.enter_async_context(stdio_client(params))
        self.session = await self.exit_stack.enter_async_context(ClientSession(read, write))
        # await self.session.initialize()

    async def call_tool(self, name: str, args: dict):
        """Call a tool and return result text"""
        result = await self.session.call_tool(name, args)
        return result.content[0].text

    async def chat(self):
        """Simple chat loop"""
        tools = await self.session.list_tools()
        print(f"✓ Connected! Tools: {[t.name for t in tools.tools]}\n")
        print("Type 'quit' to exit\n")
        
        while True:
            query = input("You: ").strip()
            if query.lower() in ("quit", "exit", "q"):
                break
            if not query:
                continue
            
            if "search" in query.lower():
                result = await self.call_tool("tavily_search", {"query": query})
                print(f"Result: {result[:500]}...\n")
            else:
                print("Try asking to search for something!\n")

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client/client.py mcp_server/server.py")
        sys.exit(1)
    
    client = MCPClient()
    try:
        await client.connect(sys.argv[1])
        await client.chat()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())




