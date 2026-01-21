"""
RAG Retrieval Tool for ADK Agent
Integrates ChromaDB with LlamaIndex for semantic retrieval
"""
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from google.adk.tools.retrieval import LlamaIndexRetrieval

from rag.initialization import get_vectorstore


def create_rag_retrieval_tool(
    name: str = "retrieve_documents",
    description: str = "Retrieve relevant information from the knowledge base to answer user questions.",
    similarity_top_k: int = 6
) -> LlamaIndexRetrieval:
    """
    Create a RAG retrieval tool using ChromaDB and LlamaIndex.
    
    Args:
        name: Name of the tool
        description: Description for the agent
        similarity_top_k: Number of similar documents to retrieve
        
    Returns:
        LlamaIndexRetrieval tool for ADK agent
    """
    print(f"🔧 Creating RAG retrieval tool...")
    
    # 1. Load the ChromaDB vectorstore
    db = get_vectorstore()
    collection = db._collection
    print(f"✅ Loaded ChromaDB collection: {collection.name}")
    
    # 2. Wrap it for LlamaIndex
    vector_store = ChromaVectorStore(chroma_collection=collection)
    
    # 3. Create an index over that store
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        storage_context=storage_context
    )
    
    # 4. Get a semantic retriever
    retriever = index.as_retriever(similarity_top_k=similarity_top_k)
    print(f"✅ Retriever configured (top_k={similarity_top_k})")
    
    # 5. Wrap it in the ADK Retrieval tool
    retrieve_docs = LlamaIndexRetrieval(
        name=name,
        description=description,
        retriever=retriever,
    )
    
    print(f"✅ RAG retrieval tool created: {name}")
    return retrieve_docs
