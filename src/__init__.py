"""
RAG Chatbot - Source Package
A complete Retrieval-Augmented Generation system using free, local AI models.

Components:
- ingestion: Document loading and chunking
- embeddings: Vector store management with HuggingFace embeddings
- retriever: Advanced document retrieval strategies
- llm: LLM integration with Ollama
- chatbot: Complete RAG pipeline
"""

__version__ = "1.0.0"
__author__ = "Hesham Asif"

# Import main classes for easier access
from .ingestion import DocumentIngestion
from .embeddings import VectorStoreManager
from .retriever import AdvancedRetriever
from .llm import LLMManager
from .chatbot import RAGChatbot

# Define what's available when someone does "from src import *"
__all__ = [
    "DocumentIngestion",
    "VectorStoreManager",
    "AdvancedRetriever",
    "LLMManager",
    "RAGChatbot",
]

# Package metadata
PACKAGE_INFO = {
    "name": "rag-chatbot",
    "version": __version__,
    "description": "Free RAG chatbot using Ollama and HuggingFace",
    "author": __author__,
    "license": "MIT",
    "requires": [
        "langchain>=0.1.0",
        "ollama>=0.1.7",
        "sentence-transformers>=2.3.1",
        "chromadb>=0.4.22",  # or faiss-cpu>=1.7.4
        "streamlit>=1.29.0",
    ]
}

def get_version():
    """Return the current version."""
    return __version__

def get_package_info():
    """Return package information."""
    return PACKAGE_INFO