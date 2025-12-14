🌟 Features

100% Free: No API costs! Uses Ollama (local LLM) and HuggingFace (free embeddings)
Multiple Document Formats: Support for PDF, TXT, and DOCX files
Intelligent Chunking: Smart document splitting for optimal context
Vector Search: Semantic similarity search using embeddings
Advanced Retrieval: Multiple retrieval strategies (basic, diverse, threshold-based)
Chat History: Context-aware conversations with history tracking
Web Interface: Beautiful Streamlit UI for easy interaction
Source Citations: View exactly which documents answered your questions
Streaming Responses: Real-time answer generation
Production Ready: Modular architecture with comprehensive testing

🏗️ Architecture
User Question
      ↓
Question Rephrasing (with chat history)
      ↓
Vector Similarity Search
      ↓
Document Retrieval (Top K relevant chunks)
      ↓
Context Formation
      ↓
LLM Generation (with context)
      ↓
Answer + Source Citations
Component Breakdown

Document Ingestion (src/ingestion.py)

Load documents from various formats
Split into optimally-sized chunks
Preserve metadata for citations


Embeddings & Vector Store (src/embeddings.py)

Generate vector embeddings using OpenAI
Store in ChromaDB for fast retrieval
Persist to disk for reuse


Retriever (src/retriever.py)

Semantic similarity search
Multiple retrieval strategies
Context string formatting


LLM Integration (src/llm.py)

GPT-4 integration for answer generation
Prompt engineering for RAG
Streaming support


RAG Pipeline (src/chatbot.py)

Orchestrates all components
Manages chat history
Tracks statistics


Web Interface (app/streamlit_app.py)

User-friendly chat interface
Document upload
Settings and controls



🚀 Quick Start
Prerequisites

Python 3.12+
NO API KEYS NEEDED! Everything runs locally and free 🎉

Installation

Clone the repository

bashgit clone https://github.com/hasham82/DocuChat-AI
cd rag-chatbot

Create virtual environment

bashpython -m venv venv
venv\Scripts\activate  # Windows

Install dependencies

bashpip install -r requirements.txt

Install and setup Ollama (FREE Local LLM)

Download from ollama.ai and install.
Then pull a model:
bash# Recommended: Llama 3.1 (8B)
ollama pull llama3.1

# Or try Mistral (7B) - faster
ollama pull mistral

# Or Phi-3 (3.8B) - very fast
ollama pull phi3

Run the application

bashstreamlit run app/streamlit_app.py
The app will open in your browser at http://localhost:8501
📖 Usage
Web Interface

Upload Documents: Use the sidebar to upload PDF, TXT, or DOCX files
Process Documents: Click "Process Documents" to create the knowledge base
Ask Questions: Type questions in the chat interface
View Sources: Expand the sources section to see citations

Programmatic Usage
pythonfrom src.chatbot import RAGChatbot

# Initialize chatbot
chatbot = RAGChatbot()

# Initialize knowledge base
result = chatbot.initialize_knowledge_base("data/raw")
print(f"Processed {result['chunks']} chunks")

# Query
response = chatbot.query("What are the main topics?")
print(response['answer'])
print(f"Sources: {len(response['sources'])}")

# Query with streaming
for chunk in chatbot.query_streaming("Explain in detail"):
    print(chunk['chunk'], end='', flush=True)
⚙️ Configuration
Edit config.yaml to customize:
yaml# Embeddings - FREE HuggingFace
embeddings:
  provider: "huggingface"
  model: "all-MiniLM-L6-v2"  # Fast and good
  chunk_size: 1000
  chunk_overlap: 200

# LLM - FREE Ollama
llm:
  provider: "ollama"
  model: "llama3.1"  # or "mistral" or "phi3"
  base_url: "http://localhost:11434"
  temperature: 0.7

# Retrieval
retrieval:
  search_type: "similarity"
  k: 4
🧪 Testing
Run the test suite:
bashpytest tests/ -v
Run specific test:
bashpytest tests/test_rag.py::TestRAGChatbot -v
📊 Advanced Features
Multiple Retrieval Strategies
python# Basic similarity search
response = chatbot.query(question, retrieval_method="basic")

# Diverse results (MMR)
response = chatbot.query(question, retrieval_method="diverse")

# Threshold-based filtering
response = chatbot.query(question, retrieval_method="threshold")
Chat History Management
python# With history (default)
response = chatbot.query(question, use_history=True)

# Without history
response = chatbot.query(question, use_history=False)

# Clear history
chatbot.clear_history()
Knowledge Base Management
python# Add more documents
chatbot.initialize_knowledge_base("data/additional")

# Reset knowledge base
chatbot.reset_knowledge_base()

# Get statistics
stats = chatbot.get_stats()
🎯 Use Cases

Documentation Q&A: Answer questions about technical documentation
Research Assistant: Query research papers and articles
Legal Document Analysis: Search through contracts and legal documents
Educational Tool: Learn from textbooks and course materials
Business Intelligence: Extract insights from reports and presentations

🔧 Troubleshooting
Common Issues
Issue: "No knowledge base found"

Solution: Make sure you've uploaded and processed documents first

Issue: "API key not found"

Solution: No API keys needed! This version is 100% free and local

Issue: "Cannot connect to Ollama"

Solution:

Make sure Ollama is installed from ollama.ai
Run ollama pull llama3.1 to download the model
Ollama should run automatically after installation
Check if it's running: ollama list



Issue: "Memory error with large documents"

Solution: Reduce chunk_size in config.yaml or process fewer documents at once

Issue: "Slow response times"

Solution: Reduce k (number of retrieved documents) or use a faster embedding model

📈 Performance Tips

Choose the Right Model:

llama3.1 (8B): Best quality, slower (~2-5 sec per response)
mistral (7B): Good balance (~1-3 sec per response)
phi3 (3.8B): Fastest (~0.5-2 sec per response)


Optimize Chunk Size: Balance between context and performance (800-1200 tokens)
Adjust K Value: More documents = more context but slower responses
GPU Acceleration: If you have NVIDIA GPU, change device: 'cpu' to device: 'cuda' in embeddings.py
First Run: Initial model downloads may take time (Ollama ~4-8GB, embeddings ~80MB)

🛣️ Roadmap

 Add support for more document formats (HTML, Markdown, CSV)
 Implement caching for frequently asked questions
 Add evaluation metrics (RAGAS, BERTScore)
 Support for multiple vector stores (Pinecone, Weaviate)
 Add user authentication and multi-tenancy
 Implement hybrid search (keyword + semantic)
 Add document summarization feature
 Support for images and tables in documents

🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

Built with LangChain
Vector storage powered by ChromaDB
UI created with Streamlit
LLM provided by Ollama (FREE!)
Embeddings by HuggingFace (FREE!)

📧 Contact
Email - hashaamasif82@gmail.com
Project Link: https://github.com/yourusername/rag-chatbot

Built with ❤️ for the AI community