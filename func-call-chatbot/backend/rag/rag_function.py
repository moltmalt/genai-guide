import json
from typing import List, Dict, Any, Optional
from .embedding_generator import EmbeddingGenerator
from .vector_store import VectorStore
from .knowledge_base import KnowledgeBase

class RAGSystem:
    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = VectorStore()
        self.knowledge_base = KnowledgeBase()
        
        # load vectors if they exist, otherwise create them
        if not self.vector_store.get_all_vectors():
            self._initialize_vectors()
    
    def _initialize_vectors(self):
        """Initialize vector store with knowledge base content"""
        print("Initializing vector store...")
        
        # vectors for each content type
        product_vectors = self.knowledge_base.create_product_vectors()
        faq_vectors = self.knowledge_base.create_faq_vectors()
        policy_vectors = self.knowledge_base.create_policy_vectors()
        
        # save
        self.vector_store.save_vectors(product_vectors, "product_vectors")
        self.vector_store.save_vectors(faq_vectors, "faq_vectors")
        self.vector_store.save_vectors(policy_vectors, "policy_vectors")
        
        print("Vector store initialized successfully!")
    
    def search(self, query: str, top_k: Optional[int] = None, content_type: Optional[str] = None) -> str:
        """
        Main RAG search function that can be called from the chatbot
        
        Args:
            query: User's search query
            top_k: Number of top results to return
            content_type: Optional filter for specific content type (products, faq, policies)
        
        Returns:
            Formatted string with relevant information
        """
        try:
            # default top_k 
            if top_k is None:
                top_k = 3
                
            # generate embedding 
            query_embedding = self.embedding_generator.generate_embedding(query)
            
            if not query_embedding:
                return "I'm sorry, I couldn't process your search query at the moment."
            
            # search for similar vectors
            results = self.vector_store.search(query_embedding, top_k, content_type)
            
            if not results:
                return "I couldn't find any relevant information for your query."
            
            # format 
            formatted_results = self._format_search_results(results, query)
            
            return formatted_results
            
        except Exception as e:
            print(f"Error in RAG search: {e}")
            return "I encountered an error while searching for information."
    
    def _format_search_results(self, results: List[tuple], original_query: str) -> str:
        """Format search results into a readable response"""
        if not results:
            return "No relevant information found."
        
        response_parts = []
        
        for vector_entry, similarity_score in results:
            metadata = vector_entry.get("metadata", {})
            content_type = metadata.get("type", "unknown")
            
            if content_type == "product":
                response_parts.append(self._format_product_result(vector_entry, similarity_score))
            elif content_type == "faq":
                response_parts.append(self._format_faq_result(vector_entry, similarity_score))
            elif content_type == "policy":
                response_parts.append(self._format_policy_result(vector_entry, similarity_score))
            else:
                response_parts.append(self._format_generic_result(vector_entry, similarity_score))
        
        # combine all results
        combined_response = "\n\n".join(response_parts)
        
        # helpful prefix
        if len(results) > 1:
            combined_response = f"Here's what I found related to your query about '{original_query}':\n\n{combined_response}"
        else:
            combined_response = f"Here's what I found about '{original_query}':\n\n{combined_response}"
        
        return combined_response
    
    def _format_product_result(self, vector_entry: Dict, similarity_score: float) -> str:
        """Format a product search result"""
        metadata = vector_entry.get("metadata", {})
        content = vector_entry.get("content", "")
        
        # extract key information
        name = metadata.get("name", "Unknown Product")
        category = metadata.get("category", "")
        tags = metadata.get("tags", [])
        sizes = metadata.get("sizes", [])
        colors = metadata.get("colors", [])
        
        # formatted response
        response = f"**{name}**\n"
        response += f"Category: {category.title()}\n"
        
        if sizes:
            response += f"Available sizes: {', '.join(sizes)}\n"
        if colors:
            response += f"Available colors: {', '.join(colors)}\n"
        
        # brief description (first 200 characters)
        description = content[:200] + "..." if len(content) > 200 else content
        response += f"\n{description}"
        
        return response
    
    def _format_faq_result(self, vector_entry: Dict, similarity_score: float) -> str:
        """Format an FAQ search result"""
        content = vector_entry.get("content", "")
        metadata = vector_entry.get("metadata", {})
        category = metadata.get("category", "").title()
        
        # extract question and answer from content
        if "Question:" in content and "Answer:" in content:
            parts = content.split("Answer:")
            question = parts[0].replace("Question:", "").strip()
            answer = parts[1].strip()
            
            response = f"**{category} FAQ**\n"
            response += f"Q: {question}\n"
            response += f"A: {answer}"
        else:
            response = f"**{category} Information**\n{content}"
        
        return response
    
    def _format_policy_result(self, vector_entry: Dict, similarity_score: float) -> str:
        """Format a policy search result"""
        content = vector_entry.get("content", "")
        metadata = vector_entry.get("metadata", {})
        category = metadata.get("category", "").title()
        
        response = f"**{category} Policy**\n{content}"
        return response
    
    def _format_generic_result(self, vector_entry: Dict, similarity_score: float) -> str:
        """Format a generic search result"""
        content = vector_entry.get("content", "")
        metadata = vector_entry.get("metadata", {})
        
        response = f"**Relevant Information**\n{content}"
        return response
    
    def get_product_info(self, product_name: str) -> str:
        """Get specific product information"""
        return self.search(f"product information about {product_name}", top_k=1, content_type="product_vectors")
    
    def get_faq_answer(self, question: str) -> str:
        """Get FAQ answer for a specific question"""
        return self.search(question, top_k=1, content_type="faq_vectors")
    
    def get_policy_info(self, policy_topic: str) -> str:
        """Get policy information for a specific topic"""
        return self.search(f"policy about {policy_topic}", top_k=1, content_type="policy_vectors") 