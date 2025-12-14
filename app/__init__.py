"""
RAG Chatbot - Web Application Package
Streamlit-based web interface for the RAG chatbot.

Main module: streamlit_app.py
"""

__version__ = "1.0.0"

# App configuration
APP_CONFIG = {
    "title": "RAG Document Q&A Chatbot",
    "icon": "🤖",
    "layout": "wide",
    "description": "Ask questions about your documents using free local AI"
}

def get_app_config():
    """Return application configuration."""
    return APP_CONFIG