"""
RAG Chatbot - Test Suite
Unit tests and integration tests for the RAG chatbot system.

Run tests with: pytest tests/ -v
"""

__version__ = "1.0.0"

# Test configuration
TEST_CONFIG = {
    "test_data_dir": "data/raw",
    "test_vector_store_dir": "test_chroma_db",
    "cleanup_after_tests": True
}

def get_test_config():
    """Return test configuration."""
    return TEST_CONFIG