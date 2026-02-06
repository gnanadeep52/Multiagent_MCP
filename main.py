# main.py - Run the system
import asyncio
from graph.supervisor import supervisor_graph
from graph.state import GraphState

async def main():
    question = input("Ask a question: ").strip()
    
    initial_state: GraphState = {
        "question": question,
        "search_results": "",
        "scraped_content": "",
        "outline": [],
        "final_answer": "",
    }
    
    print("\n🔍 Running research and writing pipeline...\n")
    
    result = await supervisor_graph.ainvoke(initial_state)
    
    print("\n" + "="*60)
    print("RESEARCH COMPLETE")
    print("="*60)
    print(f"\nSearch Results: {result['search_results'][:200]}...")
    print(f"\nOutline: {result['outline']}")
    print(f"\n{result['final_answer']}")
    print("\n✓ Check temp/ folder for outline.txt and answer.txt")

if __name__ == "__main__":
    asyncio.run(main())




# # main.py
# import asyncio
# from graph.supervisor import run_supervisor

# if __name__ == "__main__":
#     question = input("Ask a question: ")
#     result = asyncio.run(run_supervisor(question))

#     print("\n=== FINAL ANSWER ===\n")
#     print(result["final_answer"])
