import faiss
import numpy as np
import re
from typing import List
from sentence_transformers import SentenceTransformer


class VectorStore:
    """
    Lightweight FAISS-based vector store for text data.
    Pipeline:
    raw text -> cleaning -> chunking -> embeddings -> FAISS index
    """

    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        chunk_size: int = 300,
        overlap: int = 50
    ):
        self.model = SentenceTransformer(embedding_model)
        self.chunk_size = chunk_size
        self.overlap = overlap

        self.index = None
        self.chunks: List[str] = []
        self.dim = None

   
    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\w\s.,]", "", text)
        return text.strip()

   
    def chunk_text(self, text: str) -> List[str]:
        words = text.split()
        chunks = []

        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunk = words[start:end]
            chunks.append(" ".join(chunk))
            start += self.chunk_size - self.overlap

        return chunks

    
    def embed(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    
    def build(self, raw_texts: List[str]):
        self.chunks = []

        for text in raw_texts:
            cleaned = self.clean_text(text)
            self.chunks.extend(self.chunk_text(cleaned))

        embeddings = self.embed(self.chunks)
        self.dim = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(embeddings)

   
    def search(self, query: str, top_k: int = 5):
        if self.index is None:
            raise ValueError("Index not built yet. Call build() first.")

        query = self.clean_text(query)
        q_emb = self.embed([query])

        scores, indices = self.index.search(q_emb, top_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            results.append({
                "text": self.chunks[idx],
                "score": float(score)
            })

        return results

docs = [
    "The ALM optimization minimizes NII variance subject to duration constraints.",
    "Marketing ROI analysis focuses on conversion rate and CAC.",
    "Gradient descent minimizes loss functions in neural networks."
]

vs = VectorStore()
vs.build(docs)

results = vs.search("optimize hedge portfolio")

for r in results:
    print(r)