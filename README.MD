# 🤖 DocuChat-AI

> Chat with your documents using 100% free, local AI - no API costs, complete privacy

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Cost](https://img.shields.io/badge/cost-FREE-brightgreen.svg)

---

## 📖 About

DocuChat-AI is a production-ready **Retrieval-Augmented Generation (RAG)** chatbot that enables natural conversations with your documents. Built with 100% free and open-source tools, it runs entirely on your local machine with no API costs or data privacy concerns.

### ✨ Key Features

- 🆓 **100% Free** - No API costs, runs locally using Ollama
- 🔒 **Privacy-First** - All data stays on your machine
- 📄 **Multi-Format** - Supports PDF, TXT, and DOCX files
- 🧠 **Smart Search** - Semantic similarity search with vector embeddings
- 💬 **Context-Aware** - Maintains conversation history
- 📚 **Source Citations** - Shows which documents answered your questions
- ⚡ **Fast Setup** - Running in under 30 minutes
- 🎨 **Beautiful UI** - Built with Streamlit

### 🎯 Perfect For

- 🎓 Learning RAG architecture and LLMs
- 💼 Document analysis and research
- 🔐 Sensitive documents that require privacy
- 💰 Cost-conscious AI applications

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [Ollama](https://ollama.ai) installed
- 8GB RAM minimum (16GB recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hasham82/DocuChat-AI
   cd docuchat-ai
   ```

2. **Install Ollama and download a model**
   ```bash
   # Download from https://ollama.ai
   # Then pull a model:
   ollama pull llama3.1
   ```

3. **Run setup script**
   ```bash
   setup.bat
   ```

4. **Launch the application**
   ```bash
   run.bat
   ```

The web interface will open automatically at `http://localhost:8501`

### Manual Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app/streamlit_app.py
```

---

## 📊 Architecture

```
User Question
      ↓
Question Rephrasing (with chat history)
      ↓
Vector Similarity Search (HuggingFace embeddings)
      ↓
Document Retrieval (Top K relevant chunks)
      ↓
Context Formation
      ↓
LLM Generation (Ollama)
      ↓
Answer + Source Citations
```

### Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| **LLM** | Ollama (Llama 3.1) | Free, local, privacy-first |
| **Embeddings** | HuggingFace | Free, high-quality vectors |
| **Vector DB** | ChromaDB | Efficient similarity search |
| **Framework** | LangChain | RAG orchestration |
| **UI** | Streamlit | Rapid development |
| **Language** | Python 3.12 | ML ecosystem |

---

## 💡 Usage

### 1. Upload Documents

- Click "Browse files" in the sidebar
- Select PDF, TXT, or DOCX files
- Click "Process Documents"

### 2. Ask Questions

Type questions like:
- "What are the main topics discussed in the documents?"
- "Summarize the key findings about [topic]"
- "What does the document say about [specific subject]?"

### 3. View Sources

- Expand the "View Sources" section
- See exactly which documents and pages were used

---

## 🎓 Project Structure

```
docuchat-ai/
├── src/
│   ├── ingestion.py      # Document loading and chunking
│   ├── embeddings.py     # Vector store management
│   ├── retriever.py      # Semantic search logic
│   ├── llm.py           # Ollama LLM integration
│   └── chatbot.py       # Main RAG pipeline
│
├── app/
│   └── streamlit_app.py  # Web interface
│
├── tests/
│   └── test_rag.py      # Unit tests
│
├── data/
│   └── raw/             # Upload your documents here
│
├── config.yaml          # Configuration
├── requirements.txt     # Dependencies
└── README.md           # This file
```

---

## ⚙️ Configuration

Edit `config.yaml` to customize:

```yaml
# LLM settings
llm:
  model: "llama3.1"  # or "mistral", "phi3"
  temperature: 0.7

# Embeddings
embeddings:
  model: "all-MiniLM-L6-v2"
  chunk_size: 1000

# Retrieval
retrieval:
  k: 4  # Number of documents to retrieve
```

---

## 🧪 Testing

Run the test suite:

```bash
pytest tests/ -v
```

Test individual components:

```bash
python src/ingestion.py
python src/embeddings.py
python src/llm.py
```

---

## 📈 Performance

| Model | Response Time | Quality | RAM Usage |
|-------|--------------|---------|-----------|
| Llama 3.1 (8B) | 2-5 sec | ⭐⭐⭐⭐⭐ | ~6GB |
| Mistral (7B) | 1-3 sec | ⭐⭐⭐⭐ | ~5GB |
| Phi-3 (3.8B) | 0.5-2 sec | ⭐⭐⭐ | ~3GB |

*Tested on: Intel i3 10100f, 16GB RAM, no GPU*

---

## 🔧 Troubleshooting

### Cannot connect to Ollama

```bash
# Check if Ollama is running
ollama list

# Start Ollama service
ollama serve
```

### Slow responses

- Use a faster model: `ollama pull phi3`
- Reduce `k` in config to 2-3
- Consider GPU acceleration if available

### Out of memory

- Use smaller model (phi3)
- Reduce `chunk_size` in config
- Process fewer documents at once

See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) for detailed troubleshooting.

---

## Some Demo Screenshots
![image alt](https://github.com/hasham82/DocuChat-AI/blob/d15d2233db7acfc5fc370a04cbbfe6efa5bbbe28/Demo/ss0.png)

---

## 🛣️ Roadmap

- [ ] Add support for more file formats (HTML, Markdown, CSV)
- [ ] Implement hybrid search (keyword + semantic)
- [ ] Add document summarization feature
- [ ] Support for multiple vector stores
- [ ] GPU acceleration optimization
- [ ] Docker containerization
- [ ] Mobile-responsive UI
- [ ] Multi-language support

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) - Free local LLM inference
- [LangChain](https://www.langchain.com/) - RAG framework
- [HuggingFace](https://huggingface.co/) - Free embeddings
- [Streamlit](https://streamlit.io/) - Web UI framework
- [ChromaDB](https://www.trychroma.com/) - Vector database

---

## 📧 Contact
**Hesham Asif**
- GitHub: [hasham82](https://github.com/hasham82)
- LinkedIn: [hesham-asif-84b793345](https://www.linkedin.com/in/hesham-asif-84b793345/)
- Email: hashaamasif82@gmail.com

---

**Built with ❤️ using 100% free and open-source tools**

[Report Bug](https://github.com/hasham82/issues) · [Request Feature](https://github.com/hasham82/issues)

</div>
