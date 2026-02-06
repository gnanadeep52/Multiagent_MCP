
from agents.llm import llm
from client.client_sse import MCPClient

async def doc_writer_agent(topic: str, outline: list[str], doc_file: str = "answer.txt") -> dict:
    """
    Uses LLM to:
      1. Write a clear full document following the given outline
      2. Generate summary / key takeaway points from that document
    Saves the full document via MCP
    Returns a dictionary with final_content + summary_points + file name
    """
    # ── Step 1: Generate full document ───────────────────────────────
    outline_str = "\n".join(f"- {point}" for point in outline)

    document_prompt = f"""Write a clear, well-structured document on the topic '{topic}' 
following exactly this outline:

{outline_str}

Use markdown formatting:
- # for the main title
- ## for section headings
- Short paragraphs
- Bullet points when appropriate

Keep the tone professional, informative, and concise."""
    
    full_content = llm.invoke(document_prompt).content.strip()

    # ── Step 2: Generate summary / key takeaway points ───────────────
    summary_prompt = f"""Based on the following document, extract 5–8 concise bullet-point key takeaways.
Each bullet should start with "- ".
Do not add any extra text outside the bullets.

Document content:
{full_content}"""

    summary_response = llm.invoke(summary_prompt).content.strip()

    # Clean up summary points
    summary_points = []
    for line in summary_response.splitlines():
        line = line.strip()
        if line.startswith(('-', '•', '*')):
            clean_point = line.lstrip('-•* ').strip()
            if clean_point:
                summary_points.append(clean_point)

    # ── Step 3: Save the full document using MCP ─────────────────────
    async with MCPClient() as client:
        await client.call_tool("write_document", {
            "file_name": doc_file,
            "content": full_content  
        })

    
    return {
        "final_content": full_content,
        "final_summary_points": summary_points,
        "final_file": doc_file
    }