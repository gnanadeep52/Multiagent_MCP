# Deep Draft

It is an AI system that can research a topic and write a document about it automatically.

Instead of using one large prompt, the system is split into multiple small agents, each responsible for one task (research, outlining, writing).

The system automatically:

- Searches the web for up-to-date information  
- Reads important webpages  
- Creates a clean outline  
- Writes a full, structured document based on that outline  
- Shows you key summary points


## Use Case

You provide a question or topic.

The system will:

 - Search the web for relevant information

 - Read and extract content from webpages

 - Create a structured outline

 - Write a final document based on that outline

 
## What You See in the Streamlit Interface

When you run the app (`streamlit run app.py`) and type a question, this is what appears step by step in the chat:

1. Your question is shown (as a user message)

2. The assistant replies with:
   - **Outline**  
     A clean list of main points

3. After a short pause:
   - **Full Document**  
     The complete markdown-formatted explanation / report  
     (with headings, paragraphs, bullets — everything the LLM wrote)

4. After another short pause:
   - **Key Summary Points**  
     5–8 concise bullet points  
     (the most important takeaways from the document)

5. The chat input box appears again — you can ask follow-up questions or type `quit` / `exit` / `q` to stop

All generated content stays in the chat history until you close or clear it.



## High-Level Architecture

The system has three layers:

- Agents – Do the actual work (searching, scraping, writing)

- Graphs – Define the order in which agents run

- Tool Server (MCP) – Provides external capabilities like web search and file writing

## Internal Process

1. Supervisor starts the workflow

- The supervisor graph is the entry point.

- It controls the full flow 

2. Research process

     The research graph runs first.

   Step 1: Search

    - The system takes the user’s question

    - An LLM converts it into a concise search query

    - A search tool (Tavily) is called via the tool server

    - Search results are returned 

    Step 2: Scrape

    - URLs are extracted from the search results

    - The system fetches the webpages

    - The text content of those pages is collected

At the end of this phase, the system has:

Raw search results

Scraped webpage content

3. Writing process

    After research finishes, the writing graph runs.

    Step 1: Outline creation

    - An LLM generates a structured outline for the topic

    - The outline is saved to a file (outline.txt)

    Step 2: Document writing

    - Another LLM uses the topic and outline

    - A full document is written

    - The final output is saved to a file (answer.txt)


## How Agents Work

Each agent is a small, focused function:

1. Search agent

 - Decides what to search

 - Calls the web search tool

2. Web scraper agent

- Extracts URLs

- Reads webpage content

3. Note taker agent

- Generates an outline

- Saves it as a file

4. Document writer agent

- Writes the final explanation

- Saves it as a file

## How Graphs Work

Graphs define execution order, not logic.

- Each graph:

1. Has a shared state

2. Runs nodes one after another

3. Passes data forward

- There are three graphs:

1. Research graph – search → scrape

2. Writing graph – outline → write

3. Supervisor graph – research → writing


## How Tools Work (MCP Server)

The system does not directly access the web or filesystem.

Instead, it uses a tool server that exposes controlled tools.

- Available tools

  1. Web search tool

     Searches the web using Tavily

  2. Web scraping tool

     Fetches webpage content

  3. Create outline

     Writes outline text to a file

  4. Write document

     Writes full documents to a file

  5. Read / edit document

     Reads or modifies saved files

Agents call these tools through an MCP client.


 ## Outputs

All generated files are saved in a temporary directory:

outline.txt – generated outline

answer.txt – final document

These files represent the system’s final output.



# References

https://modelcontextprotocol.io/docs/develop/build-server

https://modelcontextprotocol.io/docs/develop/build-client