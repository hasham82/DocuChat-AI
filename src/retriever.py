"""
Advanced retrieval strategies for RAG chatbot.
"""
from typing import List, Dict, Any
from langchain.schema import Document
import yaml


class AdvancedRetriever:
    """Implements advanced retrieval strategies."""
    
    def __init__(self, vector_store_manager, config_path: str = "config.yaml"):
        """Initialize retriever with vector store manager."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.vs_manager = vector_store_manager
        self.k = self.config['retrieval']['k']
    
    def retrieve(self, query: str, k: int = None) -> List[Document]:
        """Basic retrieval."""
        if k is None:
            k = self.k
        
        results = self.vs_manager.similarity_search(query, k=k)
        return results
    
    def retrieve_with_scores(self, query: str, k: int = None):
        """Retrieve documents with relevance scores."""
        if k is None:
            k = self.k
        
        results = self.vs_manager.similarity_search_with_score(query, k=k)
        return results
    
    def retrieve_with_threshold(
        self, 
        query: str, 
        k: int = None,
        score_threshold: float = 0.7
    ) -> List[Document]:
        """Retrieve only documents above similarity threshold."""
        if k is None:
            k = self.k
        
        results = self.vs_manager.similarity_search_with_score(query, k=k)
        
        # Filter by threshold (lower score = more similar for some distance metrics)
        # Note: Chroma uses L2 distance, so lower is better
        filtered_results = [
            doc for doc, score in results 
            if score <= (1 - score_threshold)  # Adjust based on your distance metric
        ]
        
        return filtered_results
    
    def retrieve_diverse(self, query: str, k: int = None) -> List[Document]:
        """Retrieve diverse documents using MMR (Maximal Marginal Relevance)."""
        if k is None:
            k = self.k
        
        # Use MMR search from vector store
        if self.vs_manager.vector_store:
            results = self.vs_manager.vector_store.max_marginal_relevance_search(
                query, 
                k=k,
                fetch_k=k*3  # Fetch more candidates for diversity
            )
            return results
        return []
    
    def retrieve_with_metadata_filter(
        self, 
        query: str,
        metadata_filter: Dict[str, Any],
        k: int = None
    ) -> List[Document]:
        """Retrieve documents filtered by metadata."""
        if k is None:
            k = self.k
        
        if self.vs_manager.vector_store:
            results = self.vs_manager.vector_store.similarity_search(
                query,
                k=k,
                filter=metadata_filter
            )
            return results
        return []
    
    def get_context_string(self, documents: List[Document]) -> str:
        """Convert retrieved documents to context string."""
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get('filename', 'Unknown source')
            page = doc.metadata.get('page', 'N/A')
            
            context_parts.append(
                f"[Document {i}] (Source: {source}, Page: {page})\n"
                f"{doc.page_content}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    def print_retrieval_results(
        self, 
        query: str, 
        documents: List[Document]
    ) -> None:
        """Pretty print retrieval results."""
        print(f"\n{'='*80}")
        print(f"Query: {query}")
        print(f"Retrieved {len(documents)} documents")
        print(f"{'='*80}\n")
        
        for i, doc in enumerate(documents, 1):
            print(f"Document {i}:")
            print(f"  Source: {doc.metadata.get('filename', 'Unknown')}")
            print(f"  Page: {doc.metadata.get('page', 'N/A')}")
            print(f"  Content: {doc.page_content[:200]}...")
            print()


if __name__ == "__main__":
    from .embeddings import VectorStoreManager
    
    # Initialize
    vs_manager = VectorStoreManager()
    vs_manager.load_vector_store()
    
    retriever = AdvancedRetriever(vs_manager)
    
    # Test retrieval
    query = "What are the main topics discussed?"
    
    print("1. Basic Retrieval:")
    docs = retriever.retrieve(query, k=3)
    retriever.print_retrieval_results(query, docs)
    
    print("\n2. Retrieval with Scores:")
    results = retriever.retrieve_with_scores(query, k=3)
    for doc, score in results:
        print(f"Score: {score:.4f} | {doc.metadata.get('filename')}")
    
    print("\n3. Context String:")
    context = retriever.get_context_string(docs[:2])
    print(context[:500])