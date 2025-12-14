"""
Streamlit web interface for RAG chatbot.
"""
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
from src.chatbot import RAGChatbot
from src.ingestion import DocumentIngestion
import yaml


# Page configuration
st.set_page_config(
    page_title="RAG Document Q&A Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stat-card {
        background-color: #e8eaf6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_chatbot():
    """Load chatbot (cached to avoid reloading)."""
    return RAGChatbot()


def initialize_session_state():
    """Initialize Streamlit session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chatbot_initialized" not in st.session_state:
        st.session_state.chatbot_initialized = False
    if "uploaded_files_processed" not in st.session_state:
        st.session_state.uploaded_files_processed = False


def sidebar():
    """Render sidebar with controls."""
    with st.sidebar:
        st.markdown("### 📚 Knowledge Base Management")
        
        # File upload section
        st.markdown("#### Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload PDF, TXT, or DOCX files",
            type=['pdf', 'txt', 'docx'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            if st.button("Process Documents", type="primary"):
                with st.spinner("Processing documents..."):
                    # Save uploaded files
                    save_dir = Path("data/raw")
                    save_dir.mkdir(parents=True, exist_ok=True)
                    
                    for file in uploaded_files:
                        file_path = save_dir / file.name
                        with open(file_path, "wb") as f:
                            f.write(file.getvalue())
                    
                    # Initialize knowledge base
                    chatbot = load_chatbot()
                    result = chatbot.initialize_knowledge_base("data/raw")
                    
                    if result['success']:
                        st.session_state.chatbot_initialized = True
                        st.session_state.uploaded_files_processed = True
                        st.success(
                            f"✅ Processed {result['documents']} documents "
                            f"into {result['chunks']} chunks"
                        )
                    else:
                        st.error(f"❌ {result['message']}")
        
        st.markdown("---")
        
        # Settings
        st.markdown("#### ⚙️ Settings")
        
        retrieval_method = st.selectbox(
            "Retrieval Method",
            ["basic", "diverse", "threshold"],
            help="Choose how documents are retrieved"
        )
        
        num_docs = st.slider(
            "Number of Documents",
            min_value=1,
            max_value=10,
            value=4,
            help="Number of documents to retrieve"
        )
        
        use_history = st.checkbox(
            "Use Chat History",
            value=True,
            help="Consider previous messages for context"
        )
        
        st.markdown("---")
        
        # Actions
        st.markdown("#### 🔧 Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear Chat"):
                st.session_state.messages = []
                chatbot = load_chatbot()
                chatbot.clear_history()
                st.rerun()
        
        with col2:
            if st.button("Reset KB"):
                chatbot = load_chatbot()
                chatbot.reset_knowledge_base()
                st.session_state.chatbot_initialized = False
                st.session_state.messages = []
                st.success("Knowledge base reset!")
        
        # Statistics
        if st.session_state.chatbot_initialized:
            st.markdown("---")
            st.markdown("#### 📊 Statistics")
            chatbot = load_chatbot()
            stats = chatbot.get_stats()
            
            st.metric("Total Queries", stats['total_queries'])
            st.metric("Successful Retrievals", stats['successful_retrievals'])
            st.metric("Chat History", stats['chat_history_length'])
        
        return retrieval_method, num_docs, use_history


def display_sources(sources):
    """Display source documents."""
    if not sources:
        return
    
    with st.expander("📄 View Sources", expanded=False):
        for i, source in enumerate(sources, 1):
            st.markdown(f"**Source {i}: {source['filename']}** (Page {source['page']})")
            if 'content_preview' in source:
                st.text(source['content_preview'])
            st.markdown("---")


def main():
    """Main application."""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">🤖 RAG Document Q&A Chatbot</div>', 
                unsafe_allow_html=True)
    st.markdown("Ask questions about your documents using AI-powered retrieval")
    
    # Sidebar
    retrieval_method, num_docs, use_history = sidebar()
    
    # Main chat area
    if not st.session_state.chatbot_initialized:
        st.info(
            "👋 Welcome! Please upload documents in the sidebar to get started. "
            "The chatbot will analyze your documents and answer questions about them."
        )
        
        # Show example
        with st.expander("💡 How to use this chatbot"):
            st.markdown("""
            1. **Upload Documents**: Use the sidebar to upload PDF, TXT, or DOCX files
            2. **Process**: Click "Process Documents" to create the knowledge base
            3. **Ask Questions**: Type your questions in the chat below
            4. **View Sources**: Expand the sources section to see where answers come from
            
            **Example questions:**
            - "What are the main topics discussed in the documents?"
            - "Can you summarize the key findings?"
            - "What does the document say about [specific topic]?"
            """)
        return
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                display_sources(message["sources"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            chatbot = load_chatbot()
            
            with st.spinner("Thinking..."):
                response = chatbot.query(
                    prompt,
                    use_history=use_history,
                    retrieval_method=retrieval_method,
                    k=num_docs
                )
            
            if response['success']:
                message_placeholder.markdown(response['answer'])
                display_sources(response['sources'])
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response['answer'],
                    "sources": response['sources']
                })
            else:
                error_msg = response['answer']
                message_placeholder.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })


if __name__ == "__main__":
    main()