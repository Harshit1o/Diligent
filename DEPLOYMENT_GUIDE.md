# 🚀 ADK RAG Agent - Complete Deployment Guide

Production-ready AI agent with RAG (Retrieval-Augmented Generation) using:
- **Google ADK** - Agent framework
- **Ollama + Llama 3.1** - Self-hosted LLM
- **ChromaDB** - Vector database
- **LangChain** - Document processing

---

## 📋 Table of Contents

1. [Local Development Setup](#local-development)
2. [EC2 Deployment](#ec2-deployment)
3. [Usage Guide](#usage-guide)
4. [Troubleshooting](#troubleshooting)

---

## 🏠 Local Development

### Prerequisites
- Python 3.11+
- Ollama installed ([Download](https://ollama.com/download))

### Setup Steps

1. **Install Ollama & Pull Llama 3.1**
   ```bash
   # Install Ollama (follow instructions at ollama.com)
   ollama pull llama3.1
   ```

2. **Create Virtual Environment**
   ```bash
   cd my_agent
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```

4. **Add PDF Documents**
   ```bash
   # Place your PDF files in:
   data/pdfs/
   ```

5. **Build Vector Store**
   ```bash
   python -m rag.initialization
   ```

6. **Run the Agent**
   
   **Option A: Web UI (Recommended)**
   ```bash
   adk web
   ```
   Open http://localhost:8000
   
   **Option B: CLI**
   ```bash
   adk run
   ```
   
   **Option C: API Server**
   ```bash
   adk api_server
   ```

---

## ☁️ EC2 Deployment

### Step 1: Launch EC2 Instance

**Recommended Specs:**
- **Instance Type**: t3.medium or larger (2 vCPU, 4GB RAM minimum)
- **AMI**: Ubuntu 22.04 LTS
- **Storage**: 30GB+ SSD
- **GPU**: Optional (g4dn.xlarge for faster inference)

**Security Group Rules:**
| Type | Port | Source | Description |
|------|------|--------|-------------|
| SSH | 22 | Your IP | SSH access |
| Custom TCP | 8000 | 0.0.0.0/0 | ADK Web UI |
| Custom TCP | 11434 | 127.0.0.1/32 | Ollama (local only) |

### Step 2: Connect to EC2

```bash
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### Step 3: Run Deployment Script

```bash
# Upload deployment script
scp -i your-key.pem deploy_ec2.sh ubuntu@<EC2_PUBLIC_IP>:~/

# SSH into EC2
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>

# Run deployment
chmod +x deploy_ec2.sh
./deploy_ec2.sh
```

This will:
- ✅ Install Python 3.11
- ✅ Install Ollama
- ✅ Download Llama 3.1 model
- ✅ Create virtual environment
- ✅ Install all dependencies

### Step 4: Upload Your Agent Code

```bash
# From your local machine
scp -i your-key.pem -r my_agent ubuntu@<EC2_PUBLIC_IP>:/home/ubuntu/adk-agent/
```

### Step 5: Build Vector Store

```bash
# SSH into EC2
cd /home/ubuntu/adk-agent
source venv/bin/activate

# Add your PDFs to data/pdfs/ first
python -m rag.initialization
```

### Step 6: Run Agent

**Manual Start:**
```bash
adk web --host 0.0.0.0 --port 8000
```

**Auto-start with systemd:**
```bash
# Copy service file
sudo cp adk-agent.service /etc/systemd/system/

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable adk-agent
sudo systemctl start adk-agent

# Check status
sudo systemctl status adk-agent

# View logs
sudo journalctl -u adk-agent -f
```

### Step 7: Access Your Agent

Open in browser:
```
http://<EC2_PUBLIC_IP>:8000
```

---

## 📖 Usage Guide

### Adding Documents

1. Place PDF files in `data/pdfs/`
2. Rebuild vector store:
   ```bash
   python -m rag.initialization
   ```
3. Restart agent

### Example Queries

**With RAG:**
- "What information do you have about [topic from your PDFs]?"
- "Summarize the key points from the documents"
- "Find information about [specific detail]"

**General Questions:**
- "What's the weather like?"
- "Write me a Python function to..."

### Configuration

**Modify RAG Settings** in [rag/initialization.py](my_agent/rag/initialization.py):
```python
CHUNK_SIZE = 1000          # Size of text chunks
CHUNK_OVERLAP = 200        # Overlap between chunks
EMBEDDING_MODEL = "..."    # Embedding model to use
```

**Modify Agent Behavior** in [agent.py](my_agent/agent.py):
```python
agent_instruction = """Your custom instructions..."""
similarity_top_k = 6  # Number of docs to retrieve
```

**Change LLM Model:**
```python
# In agent.py
model=LiteLlm(model="ollama_chat/llama3.1")  # Current
model=LiteLlm(model="ollama_chat/mistral")   # Alternative
```

Available Ollama models: `ollama list`

---

## 🔧 Troubleshooting

### Ollama Not Running
```bash
sudo systemctl status ollama
sudo systemctl start ollama
ollama list  # Check available models
```

### Vector Store Not Found
```bash
# Rebuild vector store
cd my_agent
python -m rag.initialization
```

### Port 8000 Already in Use
```bash
# Find process
sudo lsof -i :8000
# Kill it
sudo kill -9 <PID>
# Or use different port
adk web --port 8080
```

### Low Memory Issues
- Use smaller models: `ollama pull llama3.1:8b`
- Reduce chunk size in `rag/initialization.py`
- Upgrade to larger EC2 instance

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### ChromaDB Issues
```bash
# Clear and rebuild
rm -rf vectorstore/
python -m rag.initialization
```

---

## 🔐 Security Best Practices

1. **Restrict SSH Access**: Use specific IP in security group
2. **API Authentication**: Add authentication layer for production
3. **HTTPS**: Use reverse proxy (nginx) with SSL certificate
4. **Environment Variables**: Store sensitive data in `.env`
5. **Firewall**: Use UFW to restrict ports
   ```bash
   sudo ufw allow 22
   sudo ufw allow 8000
   sudo ufw enable
   ```

---

## 📊 Monitoring

**Check Agent Status:**
```bash
sudo systemctl status adk-agent
```

**View Logs:**
```bash
sudo journalctl -u adk-agent -f
```

**System Resources:**
```bash
htop
nvidia-smi  # If using GPU
```

---

## 🚀 Production Enhancements

1. **Add Domain Name**
   - Point domain to EC2 IP
   - Use nginx as reverse proxy
   - Enable HTTPS with Let's Encrypt

2. **Load Balancing**
   - Use AWS Application Load Balancer
   - Scale horizontally with multiple instances

3. **Database Backup**
   - Regular backups of `vectorstore/`
   - S3 storage for PDFs

4. **Monitoring**
   - CloudWatch for metrics
   - Error tracking with Sentry

---

## 📞 Support

For issues or questions:
- Check [Google ADK Documentation](https://github.com/google/adk)
- Review [Medium Article](https://medium.com/@alirezakzt.cs/building-an-adk-agent-enhanced-with-rag-chromadb-langchain-and-llama-3-1-0f3c33f1f043)

---

## 📝 License

MIT
