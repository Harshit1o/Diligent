# Quick Start Guide

## 🎯 Quick Start (Local Testing)

1. **Install Ollama**
   ```bash
   # Download from: https://ollama.com/download
   ollama pull llama3.1
   ```

2. **Install Dependencies**
   ```bash
   cd my_agent
   pip install -r ../requirements.txt
   ```

3. **Add PDFs** (Optional - agent works without RAG)
   - Place PDF files in `data/pdfs/`
   - Run: `python -m rag.initialization`

4. **Run Agent**
   ```bash
   adk web
   ```
   Open http://localhost:8000

---

## ☁️ EC2 Deployment (Production)

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete instructions.

**Quick EC2 Setup:**
```bash
# 1. SSH into EC2
ssh -i key.pem ubuntu@<EC2_IP>

# 2. Run deployment script
./deploy_ec2.sh

# 3. Upload agent code
# (from local machine)
scp -r my_agent ubuntu@<EC2_IP>:/home/ubuntu/adk-agent/

# 4. Build vector store (if using PDFs)
python -m rag.initialization

# 5. Start agent
adk web --host 0.0.0.0 --port 8000
```

Access at: `http://<EC2_PUBLIC_IP>:8000`

---

## 📁 Project Structure

```
my_agent/
├── agent.py              # Main ADK agent with RAG
├── rag/
│   ├── initialization.py # Build vector store from PDFs
│   └── retrieval_tool.py # RAG retrieval tool
├── data/
│   └── pdfs/            # Place your PDF files here
├── vectorstore/         # ChromaDB storage (auto-created)
├── deploy_ec2.sh        # EC2 deployment script
└── adk-agent.service    # Systemd service file
```

---

## 🔑 Key Features

✅ Self-hosted LLM (Llama 3.1 via Ollama)  
✅ RAG with ChromaDB vector database  
✅ PDF document ingestion  
✅ Semantic search & retrieval  
✅ Web UI interface  
✅ EC2 deployment ready  
✅ Auto-restart service  

---

## 📚 Documentation

- [Complete Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Medium Article](https://medium.com/@alirezakzt.cs/building-an-adk-agent-enhanced-with-rag-chromadb-langchain-and-llama-3-1-0f3c33f1f043)
- [Google ADK Docs](https://github.com/google/adk)
