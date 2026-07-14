# vector_store.py - Uses TF-IDF (NO sentence-transformers needed)
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

class VectorStore:
    def __init__(self):
        self.vectorizer = None
        self.vectors = None
        self.chunks = []
        self.is_ready = False
    
    def create_index(self, chunks):
        """Create TF-IDF index from chunks"""
        if not chunks:
            raise ValueError("No chunks to index")
        
        self.chunks = chunks
        texts = [chunk.page_content for chunk in chunks]
        
        print(f"🔄 Creating TF-IDF index with {len(chunks)} chunks...")
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.vectors = self.vectorizer.fit_transform(texts)
        self.is_ready = True
        
        print("✅ TF-IDF index created successfully!")
        return self
    
    def similarity_search(self, query, k=5):
        """Search for similar chunks"""
        if not self.is_ready:
            raise ValueError("Index not created")
        
        # Vectorize query
        query_vec = self.vectorizer.transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vec, self.vectors)[0]
        
        # Get top k indices
        indices = np.argsort(similarities)[-k:][::-1]
        
        # Return chunks
        return [self.chunks[i] for i in indices]
    
    def save(self, path="tfidf_index.pkl"):
        """Save index to disk"""
        with open(path, 'wb') as f:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'vectors': self.vectors,
                'chunks': self.chunks
            }, f)
        print(f"✅ Index saved to {path}")
    
    def load(self, path="tfidf_index.pkl"):
        """Load index from disk"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.vectorizer = data['vectorizer']
            self.vectors = data['vectors']
            self.chunks = data['chunks']
            self.is_ready = True
        print(f"✅ Index loaded from {path}")
        return self
    
    def as_retriever(self, search_kwargs={"k": 5}):
        """Compatible with LangChain interface"""
        k = search_kwargs.get("k", 5)
        
        class Retriever:
            def __init__(self, store, k):
                self.store = store
                self.k = k
            
            def get_relevant_documents(self, query):
                return self.store.similarity_search(query, k=self.k)
        
        return Retriever(self, k)