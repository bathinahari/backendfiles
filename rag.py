import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class RAGSystem:
    def __init__(self, data_folder="data"):
        print("🚀 Initializing RAG system...")
        self.data_folder = data_folder
        self.texts = []
        self.model = None
        self.index = None

        # Load model and build index
        self._load_model()
        self._build_index()

    def _load_model(self):
        print("🧠 Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ Model loaded successfully.")

    def _build_index(self):
        print("📂 Building FAISS index...")
        docs = []
        for filename in os.listdir(self.data_folder):
            if filename.endswith(".txt"):
                with open(os.path.join(self.data_folder, filename), "r", encoding="utf-8") as f:
                    docs.append(f.read())

        if not docs:
            raise ValueError("No text files found in /data folder!")

        self.texts = docs
        embeddings = self.model.encode(docs)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings, dtype=np.float32))
        print(f"✅ Indexed {len(docs)} documents successfully.")

    def retrieve(self, query, top_k=2):
        query_emb = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_emb, dtype=np.float32), top_k)
        return [self.texts[i] for i in indices[0]]