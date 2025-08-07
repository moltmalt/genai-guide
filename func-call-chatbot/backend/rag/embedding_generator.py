import os
import json
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Any

class EmbeddingGenerator:
    def __init__(self, api_key=None):
        load_dotenv(override=True)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "text-embedding-3-small"
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text string"""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts"""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            print(f"Error generating batch embeddings: {e}")
            return []
    
    def create_vector_entry(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create a vector entry with content, embedding, and metadata"""
        embedding = self.generate_embedding(content)
        return {
            "content": content,
            "embedding": embedding,
            "metadata": metadata
        } 