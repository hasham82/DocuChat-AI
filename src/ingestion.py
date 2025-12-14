"""
Document ingestion and chunking module for RAG chatbot.
"""
import os
from typing import List
from pathlib import Path

from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import yaml


class DocumentIngestion:
    """Handles document loading and chunking."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize with configuration."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.chunk_size = self.config['embeddings']['chunk_size']
        self.chunk_overlap = self.config['embeddings']['chunk_overlap']
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_document(self, file_path: str) -> List[Document]:
        """Load a single document based on file extension."""
        file_extension = Path(file_path).suffix.lower()
        
        loaders = {
            '.pdf': PyPDFLoader,
            '.txt': TextLoader,
            '.docx': Docx2txtLoader,
        }
        
        if file_extension not in loaders:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        loader = loaders[file_extension](file_path)
        documents = loader.load()
        
        # Add metadata
        for doc in documents:
            doc.metadata['source'] = file_path
            doc.metadata['filename'] = Path(file_path).name
        
        return documents
    
    def load_documents(self, directory: str) -> List[Document]:
        """Load all supported documents from a directory."""
        all_documents = []
        supported_extensions = ['.pdf', '.txt', '.docx']
        
        for file_path in Path(directory).glob('**/*'):
            if file_path.suffix.lower() in supported_extensions:
                try:
                    docs = self.load_document(str(file_path))
                    all_documents.extend(docs)
                    print(f"✓ Loaded: {file_path.name}")
                except Exception as e:
                    print(f"✗ Error loading {file_path.name}: {str(e)}")
        
        return all_documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks."""
        chunks = self.text_splitter.split_documents(documents)
        
        # Add chunk metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata['chunk_id'] = i
        
        print(f"Created {len(chunks)} chunks from {len(documents)} documents")
        return chunks
    
    def process_documents(self, directory: str) -> List[Document]:
        """Complete pipeline: load and chunk documents."""
        documents = self.load_documents(directory)
        chunks = self.chunk_documents(documents)
        return chunks


if __name__ == "__main__":
    # Test the ingestion
    ingestion = DocumentIngestion()
    chunks = ingestion.process_documents("data/raw")
    print(f"\nTotal chunks created: {len(chunks)}")
    if chunks:
        print(f"Sample chunk: {chunks[0].page_content[:200]}...")