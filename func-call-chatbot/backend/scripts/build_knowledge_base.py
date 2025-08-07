#!/usr/bin/env python3
"""
Script to build the knowledge base and generate vector embeddings
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.knowledge_base import KnowledgeBase
from rag.vector_store import VectorStore

def main():
    print("Building knowledge base and generating vectors...")
    
    try:
        # Initialize knowledge base and vector store
        kb = KnowledgeBase()
        vs = VectorStore()
        
        print("Creating product vectors...")
        product_vectors = kb.create_product_vectors()
        vs.save_vectors(product_vectors, "product_vectors")
        
        print("Creating FAQ vectors...")
        faq_vectors = kb.create_faq_vectors()
        vs.save_vectors(faq_vectors, "faq_vectors")
        
        print("Creating policy vectors...")
        policy_vectors = kb.create_policy_vectors()
        vs.save_vectors(policy_vectors, "policy_vectors")
        
        print("Knowledge base built successfully!")
        print(f"Total vectors created:")
        print(f"  - Products: {len(product_vectors)}")
        print(f"  - FAQ: {len(faq_vectors)}")
        print(f"  - Policies: {len(policy_vectors)}")
        
    except Exception as e:
        print(f"Error building knowledge base: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 