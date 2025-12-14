"""
Vector store and embedding management for RAG chatbot - FREE VERSION.
"""
import os
from typing import List, Optional
from pathlib import Path

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
import yaml


class VectorStoreManager:
    """Manages vector store operations with FREE HuggingFace embeddings."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize vector store manager."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize FREE HuggingFace embeddings
        model_name = self.config['embeddings']['model']
        print(f"Loading embedding model: {model_name}")
        print("First run will download the model (one-time, ~80MB)...")
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},  # Use 'cuda' if you have GPU
            encode_kwargs={'normalize_embeddings': True}
        )
        
        print("✓ Embedding model loaded successfully!")
        
        self.persist_directory = self.config['vector_store']['persist_directory']
        self.vector_store = None
    
    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """Create a new vector store from documents."""
        print(f"Creating vector store with {len(documents)} documents...")
        
        # Create directory if it doesn't exist
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Create vector store
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        # Persist to disk
        self.vector_store.persist()
        print(f"✓ Vector store created and persisted to {self.persist_directory}")
        
        return self.vector_store
    
    def load_vector_store(self) -> Optional[Chroma]:
        """Load existing vector store from disk."""
        if not Path(self.persist_directory).exists():
            print(f"No vector store found at {self.persist_directory}")
            return None
        
        try:
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            print(f"✓ Vector store loaded from {self.persist_directory}")
            return self.vector_store
        except Exception as e:
            print(f"Error loading vector store: {str(e)}")
            return None
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add new documents to existing vector store."""
        if self.vector_store is None:
            self.vector_store = self.load_vector_store()
        
        if self.vector_store is None:
            self.create_vector_store(documents)
        else:
            self.vector_store.add_documents(documents)
            self.vector_store.persist()
            print(f"✓ Added {len(documents)} documents to vector store")
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Perform similarity search."""
        if self.vector_store is None:
            self.vector_store = self.load_vector_store()
        
        if self.vector_store is None:
            raise ValueError("No vector store available. Create one first.")
        
        results = self.vector_store.similarity_search(query, k=k)
        return results
    
    def similarity_search_with_score(self, query: str, k: int = 4):
        """Perform similarity search with relevance scores."""
        if self.vector_store is None:
            self.vector_store = self.load_vector_store()
        
        if self.vector_store is None:
            raise ValueError("No vector store available. Create one first.")
        
        results = self.vector_store.similarity_search_with_score(query, k=k)
        return results
    
    def delete_vector_store(self) -> None:
        """Delete the vector store."""
        import shutil
        if Path(self.persist_directory).exists():
            shutil.rmtree(self.persist_directory)
            print(f"✓ Vector store deleted from {self.persist_directory}")
        self.vector_store = None


if __name__ == "__main__":
    # Test vector store
    from .ingestion import DocumentIngestion
    
    # Load and chunk documents
    ingestion = DocumentIngestion()
    chunks = ingestion.process_documents("data/raw")
    
    if chunks:
        # Create vector store
        vs_manager = VectorStoreManager()
        vs_manager.create_vector_store(chunks)
        
        # Test search
        results = vs_manager.similarity_search("What is this document about?", k=3)
        print(f"\nSearch results: {len(results)} documents found")
        for i, doc in enumerate(results):
            print(f"\n{i+1}. {doc.metadata.get('filename', 'Unknown')}")
            print(f"   {doc.page_content[:150]}...")
    else:
        print("No documents found in data/raw/")