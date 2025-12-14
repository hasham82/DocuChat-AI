"""
Main RAG chatbot pipeline integrating all components.
"""
from typing import List, Dict, Any, Optional
from langchain.schema import HumanMessage, AIMessage
import yaml

from .embeddings import VectorStoreManager
from .retriever import AdvancedRetriever
from .llm import LLMManager
from .ingestion import DocumentIngestion


class RAGChatbot:
    """Complete RAG chatbot system."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize RAG chatbot with all components."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize components
        self.vs_manager = VectorStoreManager(config_path)
        self.retriever = AdvancedRetriever(self.vs_manager, config_path)
        self.llm_manager = LLMManager(config_path)
        self.ingestion = DocumentIngestion(config_path)
        
        # Chat history
        self.chat_history: List = []
        
        # Statistics
        self.stats = {
            "total_queries": 0,
            "successful_retrievals": 0,
            "average_context_length": 0
        }
    
    def initialize_knowledge_base(self, data_directory: str) -> Dict[str, Any]:
        """Initialize or update the knowledge base from documents."""
        print("Starting knowledge base initialization...")
        
        # Process documents
        chunks = self.ingestion.process_documents(data_directory)
        
        if not chunks:
            return {
                "success": False,
                "message": "No documents found to process",
                "chunks": 0
            }
        
        # Create or update vector store
        existing_store = self.vs_manager.load_vector_store()
        
        if existing_store:
            print("Updating existing vector store...")
            self.vs_manager.add_documents(chunks)
        else:
            print("Creating new vector store...")
            self.vs_manager.create_vector_store(chunks)
        
        return {
            "success": True,
            "message": "Knowledge base initialized successfully",
            "chunks": len(chunks),
            "documents": len(set(c.metadata.get('filename') for c in chunks))
        }
    
    def query(
        self, 
        question: str,
        use_history: bool = True,
        retrieval_method: str = "basic",
        k: int = None
    ) -> Dict[str, Any]:
        """
        Main query method for RAG chatbot.
        
        Args:
            question: User's question
            use_history: Whether to use chat history for context
            retrieval_method: 'basic', 'diverse', or 'threshold'
            k: Number of documents to retrieve
        
        Returns:
            Dictionary with answer and metadata
        """
        self.stats["total_queries"] += 1
        
        # Load vector store if not loaded
        if self.vs_manager.vector_store is None:
            self.vs_manager.load_vector_store()
            if self.vs_manager.vector_store is None:
                return {
                    "answer": "No knowledge base found. Please initialize with documents first.",
                    "sources": [],
                    "success": False
                }
        
        # Rephrase question if using history
        search_query = question
        if use_history and self.chat_history:
            search_query = self.llm_manager.rephrase_question(
                question, 
                self.chat_history
            )
            print(f"Rephrased query: {search_query}")
        
        # Retrieve relevant documents
        if retrieval_method == "diverse":
            documents = self.retriever.retrieve_diverse(search_query, k)
        elif retrieval_method == "threshold":
            documents = self.retriever.retrieve_with_threshold(search_query, k)
        else:
            documents = self.retriever.retrieve(search_query, k)
        
        if documents:
            self.stats["successful_retrievals"] += 1
        
        # Build context
        context = self.retriever.get_context_string(documents)
        self.stats["average_context_length"] = (
            (self.stats["average_context_length"] * (self.stats["total_queries"] - 1) 
             + len(context)) / self.stats["total_queries"]
        )
        
        # Generate answer
        chat_history = self.chat_history if use_history else None
        answer = self.llm_manager.generate_answer(
            question,
            context,
            chat_history
        )
        
        # Update chat history
        if use_history:
            self.chat_history.append(HumanMessage(content=question))
            self.chat_history.append(AIMessage(content=answer))
            
            # Keep only last 10 messages
            if len(self.chat_history) > 10:
                self.chat_history = self.chat_history[-10:]
        
        # Prepare sources
        sources = [
            {
                "filename": doc.metadata.get('filename', 'Unknown'),
                "page": doc.metadata.get('page', 'N/A'),
                "content_preview": doc.page_content[:150] + "..."
            }
            for doc in documents
        ]
        
        return {
            "answer": answer,
            "sources": sources,
            "context": context,
            "retrieved_docs": len(documents),
            "success": True
        }
    
    def query_streaming(
        self,
        question: str,
        use_history: bool = True,
        k: int = None
    ):
        """Query with streaming response for real-time display."""
        # Prepare retrieval
        if self.vs_manager.vector_store is None:
            self.vs_manager.load_vector_store()
        
        search_query = question
        if use_history and self.chat_history:
            search_query = self.llm_manager.rephrase_question(
                question,
                self.chat_history
            )
        
        documents = self.retriever.retrieve(search_query, k)
        context = self.retriever.get_context_string(documents)
        
        # Stream answer
        chat_history = self.chat_history if use_history else None
        full_answer = ""
        
        for chunk in self.llm_manager.generate_answer_streaming(
            question, context, chat_history
        ):
            full_answer += chunk
            yield {
                "chunk": chunk,
                "sources": [
                    {"filename": d.metadata.get('filename', 'Unknown')}
                    for d in documents
                ]
            }
        
        # Update history
        if use_history:
            self.chat_history.append(HumanMessage(content=question))
            self.chat_history.append(AIMessage(content=full_answer))
    
    def clear_history(self) -> None:
        """Clear chat history."""
        self.chat_history = []
        print("Chat history cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get chatbot statistics."""
        return {
            **self.stats,
            "chat_history_length": len(self.chat_history),
            "vector_store_exists": self.vs_manager.vector_store is not None
        }
    
    def reset_knowledge_base(self) -> None:
        """Delete and reset the knowledge base."""
        self.vs_manager.delete_vector_store()
        self.clear_history()
        self.stats = {
            "total_queries": 0,
            "successful_retrievals": 0,
            "average_context_length": 0
        }
        print("Knowledge base reset complete")


if __name__ == "__main__":
    # Test the complete RAG system
    chatbot = RAGChatbot()
    
    # Initialize knowledge base
    print("="*80)
    result = chatbot.initialize_knowledge_base("data/raw")
    print(f"Initialization: {result}")
    
    # Test queries
    print("\n" + "="*80)
    questions = [
        "What are the main topics in the documents?",
        "Can you provide more details?",  # Follow-up question
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        response = chatbot.query(question, use_history=True)
        print(f"A: {response['answer']}")
        print(f"Sources: {len(response['sources'])} documents")
    
    # Show statistics
    print("\n" + "="*80)
    print("Statistics:")
    for key, value in chatbot.get_stats().items():
        print(f"  {key}: {value}")