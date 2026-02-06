
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

class MCPClient:
    """
    HTTP/SSE client for MCP server.
    Connects automatically on entering the context.
    """
    def __init__(self, url: str = "http://localhost:8000/sse"):
        self.url = url
        self.session: ClientSession | None = None
        self._sse_cm = None

    async def __aenter__(self):
        # Start SSE connection
        self._sse_cm = sse_client(self.url)
        read, write = await self._sse_cm.__aenter__()

        # Create and enter session
        self.session = ClientSession(read, write)
        await self.session.__aenter__()

        # Try to initialize 
        try:
            await asyncio.wait_for(self.session.initialize(), timeout=12.0)
        except asyncio.TimeoutError:
            print("Warning: initialize() timed out – continuing anyway")
        except Exception as e:
            print(f"Initialize failed: {e!r}")

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Cleanup – ignore most errors (common with SSE)
        if self.session:
            try:
                await self.session.__aexit__(exc_type, exc_val, exc_tb)
            except Exception:
                pass
            self.session = None

        if self._sse_cm:
            try:
                await self._sse_cm.__aexit__(exc_type, exc_val, exc_tb)
            except Exception:
                pass
            self._sse_cm = None

    async def call_tool(self, name: str, arguments: dict) -> str:
        if self.session is None:
            raise RuntimeError("Client not connected. Use: async with MCPClient() as client:")

        result = await self.session.call_tool(name, arguments)

        # Extract text result (most common case)
        if hasattr(result, 'content') and result.content:
            for block in result.content:
                if hasattr(block, 'text') and block.text:
                    return block.text
        return str(result)

    async def list_tools(self):
        if self.session is None:
            raise RuntimeError("Client not connected")
        return await self.session.list_tools()