# Sample PDF document for testing
# Place this in data/pdfs/ directory

You can add your own PDF files to the data/pdfs/ directory.

The RAG system will:
1. Load all PDF files from this directory
2. Split them into chunks
3. Create embeddings
4. Store them in ChromaDB
5. Enable semantic search during queries

Supported formats:
- PDF files (.pdf)

To add documents:
1. Place PDF files in data/pdfs/
2. Run: python -m rag.initialization
3. The vector store will be rebuilt
