"""
RAG-Enhanced ADK Agent with Ollama (Llama 3.1) and ChromaDB
Based on: https://medium.com/@alirezakzt.cs/building-an-adk-agent-enhanced-with-rag-chromadb-langchain-and-llama-3-1-0f3c33f1f043
"""
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

# Import RAG retrieval tool
try:
    from rag.retrieval_tool import create_rag_retrieval_tool
    
    # Create RAG retrieval tool
    print("🔧 Initializing RAG retrieval tool...")
    retrieve_docs = create_rag_retrieval_tool(
        name="retrieve_documents",
        description="Retrieve relevant information from the knowledge base documents to answer user questions accurately.",
        similarity_top_k=6
    )
    rag_tools = [retrieve_docs]
    print("✅ RAG tool ready!")
    
except FileNotFoundError as e:
    print(f"⚠️  Vector store not found: {e}")
    print("ℹ️  Agent will run without RAG capabilities.")
    print("   To enable RAG, run: python -m rag.initialization")
    rag_tools = []
except Exception as e:
    print(f"⚠️  Could not load RAG tool: {e}")
    print("ℹ️  Agent will run without RAG capabilities.")
    rag_tools = []


# Agent instruction
agent_instruction = """You are an intelligent AI assistant with access to a knowledge base.

When answering questions:
1. Use the retrieve_documents tool to search for relevant information in the knowledge base
2. Base your answers on the retrieved documents when available
3. If information is not in the knowledge base, use your general knowledge but clearly state this
4. Be concise, accurate, and helpful
5. Cite information from the documents when possible

Always prioritize accuracy over speculation."""


# Create the RAG Agent with Ollama (Llama 3.1)
root_agent = Agent(
    model=LiteLlm(model="ollama_chat/llama3.1"),  # Using Llama 3.1 via Ollama
    name='rag_agent',
    description='An intelligent assistant with document retrieval capabilities.',
    instruction=agent_instruction,
    tools=rag_tools,
)
