import os
import json
import numpy as np
from typing import List, Dict, Any, Tuple
from pathlib import Path

class VectorStore:
    def __init__(self, data_dir: str = "data/knowledge_base"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.vectors = {}
        self.load_vectors()
    
    def load_vectors(self):
        """Load all vector files from the data directory"""
        for file_path in self.data_dir.glob("*.json"):
            if file_path.name != "metadata.json":
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        self.vectors[file_path.stem] = data.get("vectors", [])
                        print(f"Loaded {len(data.get('vectors', []))} vectors from {file_path.name}")
                except Exception as e:
                    print(f"Error loading vectors from {file_path}: {e}")
    
    def save_vectors(self, vectors: List[Dict], filename: str):
        """Save vectors to a JSON file"""
        file_path = self.data_dir / f"{filename}.json"
        data = {
            "vectors": vectors,
            "metadata": {
                "total_vectors": len(vectors),
                "embedding_model": "text-embedding-3-small",
                "dimensions": len(vectors[0]["embedding"]) if vectors else 0
            }
        }
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Update in-memory vectors
        self.vectors[filename] = vectors
        print(f"Saved {len(vectors)} vectors to {file_path}")
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        return dot_product / (norm1 * norm2)
    
    def search(self, query_embedding: List[float], top_k: int = 3, 
               vector_type: str = None) -> List[Tuple[Dict, float]]:
        """Search for similar vectors and return top-k results with scores"""
        results = []
        
        # Determine which vector collections to search
        collections_to_search = [vector_type] if vector_type else self.vectors.keys()
        
        for collection_name in collections_to_search:
            if collection_name not in self.vectors:
                continue
                
            vectors = self.vectors[collection_name]
            
            for vector_entry in vectors:
                similarity = self.cosine_similarity(query_embedding, vector_entry["embedding"])
                results.append((vector_entry, similarity))
        
        # Sort by similarity score (descending) and return top-k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def get_all_vectors(self) -> Dict[str, List[Dict]]:
        """Get all loaded vectors"""
        return self.vectors
    
    def clear_vectors(self, vector_type: str = None):
        """Clear vectors from memory"""
        if vector_type:
            self.vectors[vector_type] = []
        else:
            self.vectors = {} 