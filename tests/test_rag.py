"""
Unit tests for RAG chatbot components.
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ingestion import DocumentIngestion
from embeddings import VectorStoreManager
from retriever import AdvancedRetriever
from llm import LLMManager
from chatbot import RAGChatbot


@pytest.fixture
def sample_documents():
    """Create sample documents for testing."""
    from langchain.schema import Document
    return [
        Document(
            page_content="Python is a programming language created by Guido van Rossum.",
            metadata={"source": "test.txt", "filename": "test.txt", "page": 1}
        ),
        Document(
            page_content="Python supports object-oriented and functional programming.",
            metadata={"source": "test.txt", "filename": "test.txt", "page": 2}
        ),
    ]


class TestDocumentIngestion:
    """Test document ingestion functionality."""
    
    def test_initialization(self):
        """Test ingestion initialization."""
        ingestion = DocumentIngestion()
        assert ingestion.chunk_size > 0
        assert ingestion.chunk_overlap >= 0
        assert ingestion.text_splitter is not None
    
    def test_chunk_documents(self, sample_documents):
        """Test document chunking."""
        ingestion = DocumentIngestion()
        chunks = ingestion.chunk_documents(sample_documents)
        
        assert len(chunks) >= len(sample_documents)
        assert all(hasattr(chunk, 'page_content') for chunk in chunks)
        assert all('chunk_id' in chunk.metadata for chunk in chunks)


class TestVectorStoreManager:
    """Test vector store operations."""
    
    @pytest.fixture
    def vs_manager(self):
        """Create vector store manager."""
        return VectorStoreManager()
    
    def test_initialization(self, vs_manager):
        """Test vector store initialization."""
        assert vs_manager.embeddings is not None
        assert vs_manager.persist_directory is not None
    
    def test_create_vector_store(self, vs_manager, sample_documents):
        """Test vector store creation."""
        # Clean up any existing store
        vs_manager.delete_vector_store()
        
        # Create new store
        vector_store = vs_manager.create_vector_store(sample_documents)
        assert vector_store is not None
        
        # Clean up
        vs_manager.delete_vector_store()
    
    def test_similarity_search(self, vs_manager, sample_documents):
        """Test similarity search."""
        vs_manager.delete_vector_store()
        vs_manager.create_vector_store(sample_documents)
        
        results = vs_manager.similarity_search("Who created Python?", k=1)
        assert len(results) > 0
        assert "Guido" in results[0].page_content
        
        vs_manager.delete_vector_store()


class TestAdvancedRetriever:
    """Test retriever functionality."""
    
    @pytest.fixture
    def retriever(self, sample_documents):
        """Create retriever with sample data."""
        vs_manager = VectorStoreManager()
        vs_manager.delete_vector_store()
        vs_manager.create_vector_store(sample_documents)
        return AdvancedRetriever(vs_manager)
    
    def test_basic_retrieval(self, retriever):
        """Test basic retrieval."""
        results = retriever.retrieve("Python programming", k=2)
        assert len(results) <= 2
        assert all(hasattr(doc, 'page_content') for doc in results)
    
    def test_context_string_generation(self, retriever):
        """Test context string generation."""
        docs = retriever.retrieve("Python", k=2)
        context = retriever.get_context_string(docs)
        
        assert isinstance(context, str)
        assert len(context) > 0
        assert "Document" in context


class TestLLMManager:
    """Test LLM functionality."""
    
    @pytest.fixture
    def llm_manager(self):
        """Create LLM manager."""
        return LLMManager()
    
    def test_initialization(self, llm_manager):
        """Test LLM initialization."""
        assert llm_manager.llm is not None
        assert llm_manager.rag_prompt is not None
    
    def test_answer_generation(self, llm_manager):
        """Test answer generation."""
        context = "Python was created by Guido van Rossum in 1991."
        question = "Who created Python?"
        
        answer = llm_manager.generate_answer(question, context)
        
        assert isinstance(answer, str)
        assert len(answer) > 0
        # Basic check that answer mentions Guido
        assert "Guido" in answer or "information" in answer.lower()


class TestRAGChatbot:
    """Test complete RAG system."""
    
    @pytest.fixture
    def chatbot(self):
        """Create chatbot instance."""
        return RAGChatbot()
    
    def test_initialization(self, chatbot):
        """Test chatbot initialization."""
        assert chatbot.vs_manager is not None
        assert chatbot.retriever is not None
        assert chatbot.llm_manager is not None
        assert chatbot.ingestion is not None
        assert isinstance(chatbot.chat_history, list)
    
    def test_clear_history(self, chatbot):
        """Test clearing chat history."""
        from langchain.schema import HumanMessage
        
        chatbot.chat_history.append(HumanMessage(content="test"))
        assert len(chatbot.chat_history) > 0
        
        chatbot.clear_history()
        assert len(chatbot.chat_history) == 0
    
    def test_get_stats(self, chatbot):
        """Test statistics retrieval."""
        stats = chatbot.get_stats()
        
        assert isinstance(stats, dict)
        assert "total_queries" in stats
        assert "successful_retrievals" in stats
        assert "chat_history_length" in stats


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])