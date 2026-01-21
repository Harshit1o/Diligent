# AI Agent with RAG - Diligent Assessment

> **Assessment Project for Diligent**  
> Production-ready AI Agent with Retrieval-Augmented Generation (RAG) capabilities

---

## 🚀 Live Demo

**Access the deployed agent here:**  
🔗 **[http://13.233.173.132:8000](http://13.233.173.132:8000)**

---

## 📋 Project Overview

This project demonstrates a complete implementation of an intelligent AI agent using:

- **Google ADK (Agent Development Kit)** - Framework for building customizable AI agents
- **Ollama + Llama 3.1** - Self-hosted Large Language Model for privacy and control
- **ChromaDB** - Vector database for semantic search and document retrieval
- **LangChain** - Document processing and RAG implementation
- **FastAPI** - Web server with interactive UI
- **AWS EC2** - Cloud deployment for public access

---

## ✨ Key Features

### Core Capabilities
- ✅ **Self-Hosted LLM** - Llama 3.1 running via Ollama (no external API calls)
- ✅ **RAG (Retrieval-Augmented Generation)** - Answer questions based on uploaded documents
- ✅ **Vector Search** - Semantic search using ChromaDB embeddings
- ✅ **PDF Processing** - Automatic document ingestion and chunking
- ✅ **Web Interface** - User-friendly chat UI accessible from any browser
- ✅ **Cloud Deployed** - Production-ready deployment on AWS EC2
- ✅ **Auto-Restart** - Systemd service ensures 24/7 uptime

### Technical Highlights
- Document chunking with RecursiveCharacterTextSplitter
- HuggingFace embeddings (sentence-transformers/all-MiniLM-L6-v2)
- LlamaIndex integration for advanced retrieval
- Persistent vector store with ChromaDB
- Scalable architecture ready for production use

---

## 🏗️ Architecture

```
User Browser
    ↓
EC2 Instance (AWS)
    ↓
ADK Web Server (Port 8000)
    ↓
┌─────────────┬──────────────┐
│   Agent     │  Retrieval   │
│   (ADK)     │   (RAG)      │
└─────────────┴──────────────┘
       ↓              ↓
   Ollama        ChromaDB
 (Llama 3.1)   (Vector Store)
```

---

## 📁 Project Structure

```
Delegent/
├── my_agent/
│   ├── agent.py                  # Main ADK agent with RAG integration
│   ├── rag/
│   │   ├── initialization.py     # Vector store builder
│   │   └── retrieval_tool.py     # LlamaIndex retrieval tool
│   ├── data/pdfs/               # PDF documents for RAG
│   ├── vectorstore/             # ChromaDB storage
│   ├── deploy_ec2.sh            # Automated deployment script
│   └── adk-agent.service        # Systemd service configuration
├── requirements.txt              # Python dependencies
├── DEPLOYMENT_GUIDE.md          # Complete deployment documentation
└── README.md                     # This file
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Agent Framework** | Google ADK | Agent orchestration and tool management |
| **LLM** | Llama 3.1 (via Ollama) | Natural language understanding |
| **Vector Database** | ChromaDB | Semantic search and embeddings |
| **Document Processing** | LangChain | PDF loading and text splitting |
| **Embeddings** | HuggingFace Transformers | Document vectorization |
| **Retrieval** | LlamaIndex | Advanced RAG implementation |
| **Web Server** | FastAPI | API and web interface |
| **Deployment** | AWS EC2 (Ubuntu 22.04) | Cloud hosting |
| **Process Management** | systemd | Auto-restart and monitoring |

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Ollama installed ([Download](https://ollama.com/download))

### Setup Steps

```bash
# 1. Clone repository
git clone <repository-url>
cd Delegent

# 2. Install Ollama and pull model
ollama pull llama3.1

# 3. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
cd my_agent
nano .env
# Add: OLLAMA_API_BASE=http://localhost:11434

# 6. (Optional) Add PDFs and build vector store
# Place PDFs in data/pdfs/
python -m rag.initialization

# 7. Run agent
cd ..
adk web my_agent
```

Access at: `http://localhost:8000`

---

## ☁️ Production Deployment (AWS EC2)

### Deployment Steps

**1. Launch EC2 Instance**
- Instance Type: `t3.medium` (minimum) or `g4dn.xlarge` (with GPU)
- AMI: Ubuntu 22.04 LTS
- Storage: 30GB+ SSD
- Security Group: Open ports 22 (SSH) and 8000 (HTTP)

**2. Run Automated Deployment**

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@<EC2_IP>

# Clone repository
git clone <repository-url>
cd Delegent

# Run deployment script
chmod +x my_agent/deploy_ec2.sh
./my_agent/deploy_ec2.sh
```

**3. Configure and Start**

```bash
# Add environment variables
cd my_agent
nano .env
# Add: OLLAMA_API_BASE=http://localhost:11434

# Set up systemd service
sudo cp adk-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable adk-agent
sudo systemctl start adk-agent

# Check status
sudo systemctl status adk-agent
```

**4. Access**
Open: `http://<EC2_PUBLIC_IP>:8000`

---

## 📊 Performance Considerations

### Current Setup (CPU)
- **Model**: Llama 3.1 (8B parameters)
- **Hardware**: AWS t3.medium (2 vCPU, 4GB RAM)
- **Response Time**: ~2-3 seconds per token (CPU inference)

### Optimization Options
1. **Faster Models**: Switch to `phi3` or `gemma2:2b` for 3-5x speedup
2. **GPU Instance**: Use `g4dn.xlarge` for 10-20x faster inference
3. **Cloud API**: Switch to `gemini-2.0-flash` for instant responses

---

## 📖 Documentation

- **[Complete Deployment Guide](DEPLOYMENT_GUIDE.md)** - Detailed setup instructions
- **[Quick Start Guide](my_agent/README.md)** - Local testing guide
- **[Reference Article](https://medium.com/@alirezakzt.cs/building-an-adk-agent-enhanced-with-rag-chromadb-langchain-and-llama-3-1-0f3c33f1f043)** - Implementation reference

---

## 🔒 Security Notes

- Vector store and PDFs excluded from git (see `.gitignore`)
- Environment variables managed via `.env` files
- Ollama API restricted to localhost only
- Production deployment should add authentication layer

---

## 🎯 Assessment Deliverables

✅ **Self-hosted LLM** - Llama 3.1 via Ollama  
✅ **RAG Implementation** - ChromaDB + LangChain  
✅ **Vector Database** - Semantic search capability  
✅ **Cloud Deployment** - Live on AWS EC2  
✅ **Web Interface** - Accessible via browser  
✅ **Production Ready** - Auto-restart with systemd  
✅ **Documentation** - Complete setup guides  
✅ **Code Quality** - Clean, modular architecture  

---

## 👤 Author

**Assessment for Diligent**  
Date: January 21, 2026

---

## 📝 License

MIT
