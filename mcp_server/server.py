# mcp_server/server.py
import os
import re
from typing import List, Dict
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv

load_dotenv()

# Initialize MCP server
mcp = FastMCP("Research Writing Tools Server")

# Tavily client
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Temp directory for file operations
TEMP_DIR = os.path.join(os.getcwd(), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

def safe_filename(name: str) -> str:
    if not name:
        return "document.txt"
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", name)

# Tools
@mcp.tool()
def tavily_search(query: str, max_results: int = 3) -> str:
    """Search the web using Tavily AI search engine.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 3)
    
    Returns:
        Search results as formatted string
    """
    if not os.getenv("TAVILY_API_KEY"):
        return "Error: Tavily API key missing"
    
    try:
        response = tavily.search(
            query=query,
            max_results=max_results,
            search_depth="advanced"
        )
        
        results = []
        if response.get("answer"):
            results.append(f"Answer: {response['answer']}\n")
        
        for r in response.get("results", []):
            results.append(f"Title: {r.get('title', '')}")
            results.append(f"URL: {r.get('url', '')}")
            results.append(f"Content: {r.get('content', '')[:500]}\n")
        
        return "\n".join(results) if results else "No results found"
    
    except Exception as e:
        return f"Search failed: {str(e)}"


@mcp.tool()
def scrape_webpages(urls: List[str]) -> str:
    """Fetch and extract text from webpages.
    
    Args:
        urls: List of webpage URLs to scrape
    
    Returns:
        Combined text content from all pages
    """
    if not urls:
        return "No URLs provided"
    
    try:
        loader = WebBaseLoader(urls)
        docs = loader.load()
        content = "\n\n".join(d.page_content for d in docs)
        return content[:100000]
    except Exception as e:
        return f"Scraping failed: {str(e)}"


@mcp.tool()
def create_outline(points: List[str], file_name: str = "outline.txt") -> str:
    """Create an outline file.
    
    Args:
        points: List of outline section points
        file_name: Outline filename (saved under temp/)
    
    Returns:
        Confirmation message
    """
    file_name = safe_filename(file_name)
    path = os.path.join(TEMP_DIR, file_name)
    
    try:
        with open(path, "w", encoding="utf-8") as f:
            for i, p in enumerate(points, 1):
                f.write(f"{i}. {p}\n")
        return f"Outline saved to {file_name}"
    except Exception as e:
        return f"Failed: {str(e)}"


@mcp.tool()
def write_document(file_name: str, content: str) -> str:
    """Write or overwrite a document.
    
    Args:
        file_name: Document filename (saved under temp/)
        content: Text content to write
    
    Returns:
        Confirmation message
    """
    file_name = safe_filename(file_name)
    path = os.path.join(TEMP_DIR, file_name)
    
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Document written to {file_name}"
    except Exception as e:
        return f"Failed: {str(e)}"


@mcp.tool()
def read_document(file_name: str) -> str:
    """Read a document from the temp directory.
    
    Args:
        file_name: Document filename
    
    Returns:
        Document contents or error message
    """
    file_name = safe_filename(file_name)
    path = os.path.join(TEMP_DIR, file_name)
    
    if not os.path.exists(path):
        return "Document not found"
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Failed: {str(e)}"


@mcp.tool()
def edit_document(file_name: str, inserts: Dict[int, str]) -> str:
    """Insert text at specific line numbers.
    
    Args:
        file_name: Document filename
        inserts: Mapping of line numbers to text inserts
    
    Returns:
        Confirmation message
    """
    file_name = safe_filename(file_name)
    path = os.path.join(TEMP_DIR, file_name)
    
    try:
        if not os.path.exists(path):
            open(path, "w").close()
        
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        for line_no, text in sorted(inserts.items()):
            if not text.endswith("\n"):
                text += "\n"
            idx = min(max(line_no - 1, 0), len(lines))
            lines.insert(idx, text)
        
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        
        return f"Document edited and saved to {file_name}"
    except Exception as e:
        return f"Failed: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")


