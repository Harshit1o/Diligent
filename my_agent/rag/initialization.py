"""
RAG Initialization - Build and load ChromaDB vector store
Based on: https://medium.com/@alirezakzt.cs/building-an-adk-agent-enhanced-with-rag-chromadb-langchain-and-llama-3-1-0f3c33f1f043
"""
import os
import glob
from pathlib import Path
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader, UnstructuredPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from chromadb.config import Settings as ChromaSettings


# Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
PERSIST_DIRECTORY = "./vectorstore"
PDF_DIRECTORY = "./data/pdfs"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def load_pdf_documents(pdf_dir: str = PDF_DIRECTORY) -> List:
    """
    Load PDF documents from a directory using LangChain loaders.
    
    Args:
        pdf_dir: Directory containing PDF files
        
    Returns:
        List of loaded documents
    """
    pdf_paths = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    
    if not pdf_paths:
        print(f"⚠️  No PDF files found in {pdf_dir}")
        return []
    
    documents = []
    print(f"📄 Loading {len(pdf_paths)} PDF files...")
    
    for path in pdf_paths:
        try:
            print(f"  Loading: {os.path.basename(path)}")
            loader = PyMuPDFLoader(path)
            docs = loader.load()
            documents.extend(docs)
        except Exception as e:
            print(f"  ⚠️  PyMuPDF failed, trying UnstructuredPDFLoader: {e}")
            try:
                loader = UnstructuredPDFLoader(path)
                docs = loader.load()
                documents.extend(docs)
            except Exception as e2:
                print(f"  ❌ Failed to load {os.path.basename(path)}: {e2}")
    
    print(f"✅ Loaded {len(documents)} document chunks")
    return documents


def build_vectorstore(documents: List, persist_dir: str = PERSIST_DIRECTORY) -> Chroma:
    """
    Build a ChromaDB vector store from documents.
    
    Args:
        documents: List of documents to process
        persist_dir: Directory to persist the vector store
        
    Returns:
        ChromaDB vector store
    """
    if not documents:
        raise ValueError("No documents provided to build vectorstore")
    
    print(f"✂️  Splitting documents into chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", "\u200c", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} text chunks")
    
    print(f"🔢 Loading embedding model: {EMBEDDING_MODEL}")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    print(f"💾 Building ChromaDB vector store...")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    
    print(f"✅ Vector store created and persisted to {persist_dir}")
    return vectordb


def get_vectorstore(persist_dir: str = PERSIST_DIRECTORY) -> Chroma:
    """
    Load a persisted ChromaDB vector store if it exists.
    
    Args:
        persist_dir: Directory where vector store is persisted
        
    Returns:
        ChromaDB vector store
        
    Raises:
        FileNotFoundError: If no vector store exists
    """
    settings = ChromaSettings(
        anonymized_telemetry=False,
        persist_directory=persist_dir,
    )
    
    embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    db_path = Path(persist_dir)
    
    if db_path.exists() and any(db_path.iterdir()):
        print(f"✅ Loading existing vector store from {persist_dir}")
        return Chroma(
            persist_directory=persist_dir,
            embedding_function=embedder,
            client_settings=settings,
        )
    else:
        raise FileNotFoundError(
            f"No vectorstore found in {persist_dir!r}. "
            "Please run the build script first to create the vector store."
        )


if __name__ == "__main__":
    """Build the vector store from PDFs"""
    print("=" * 60)
    print("🚀 Building RAG Vector Store")
    print("=" * 60)
    
    # Load PDFs
    docs = load_pdf_documents()
    
    if not docs:
        print("\n❌ No documents loaded. Please add PDF files to ./data/pdfs/")
        exit(1)
    
    # Build vector store
    try:
        vectordb = build_vectorstore(docs)
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Vector store is ready.")
        print("=" * 60)
        print(f"📊 Total documents: {len(docs)}")
        print(f"💾 Stored in: {PERSIST_DIRECTORY}")
        print("\nYou can now run your ADK agent with RAG capabilities!")
    except Exception as e:
        print(f"\n❌ Error building vector store: {e}")
        exit(1)
