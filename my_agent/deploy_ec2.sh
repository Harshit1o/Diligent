#!/bin/bash
# EC2 Deployment Script for ADK RAG Agent
# This script installs all dependencies and sets up the agent on Ubuntu EC2

set -e  # Exit on error

echo "=========================================="
echo "🚀 ADK RAG Agent - EC2 Deployment"
echo "=========================================="

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3.11+ and pip
echo "🐍 Installing Python 3.11..."
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip git curl

# Install Ollama
echo "🦙 Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
echo "🔧 Starting Ollama service..."
sudo systemctl enable ollama
sudo systemctl start ollama

# Pull Llama 3.1 model
echo "📥 Downloading Llama 3.1 model (this may take a while)..."
ollama pull llama3.1

# Create project directory
PROJECT_DIR="/home/ubuntu/adk-agent"
echo "📁 Creating project directory: $PROJECT_DIR"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Create virtual environment
echo "🔨 Creating Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "📚 Installing Python dependencies..."
cat > requirements.txt << 'EOF'
# Core ADK
google-adk
python-dotenv

# LLM Integration
litellm

# RAG Components
langchain
langchain-community
chromadb
llama-index
llama-index-vector-stores-chroma

# Document Processing
PyMuPDF
unstructured
pypdf

# Embeddings
sentence-transformers
huggingface-hub

# Text Processing
tiktoken
EOF

pip install -r requirements.txt

echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Copy your agent code to: $PROJECT_DIR"
echo "2. Add PDF documents to: $PROJECT_DIR/data/pdfs/"
echo "3. Build vector store: python -m rag.initialization"
echo "4. Run web server: adk web --host 0.0.0.0 --port 8000"
echo ""
echo "Your agent will be accessible at: http://<EC2_PUBLIC_IP>:8000"
echo ""
