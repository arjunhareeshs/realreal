from sentence_transformers import SentenceTransformer
import faiss, numpy as np, pickle, os

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2", index_path="faiss.index", meta_path="meta.pkl"):
        self.model = SentenceTransformer(model_name)
        self.index_path, self.meta_path = index_path, meta_path
        self.index, self.meta = None, []
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            with open(meta_path, "rb") as f: self.meta = pickle.load(f)

    def embed(self, texts): 
        return self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)

    def add(self, texts, metas):
        vecs = self.embed(texts).astype("float32")
        faiss.normalize_L2(vecs)
        if self.index is None:
            self.index = faiss.IndexFlatIP(vecs.shape[1])
        self.index.add(vecs)
        for m, t in zip(metas, texts): m["text"] = t
        self.meta.extend(metas)

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f: pickle.dump(self.meta, f)

    def search(self, query, k=5):
        qv = self.embed([query]).astype("float32")
        faiss.normalize_L2(qv)
        D, I = self.index.search(qv, k)
        return [{"score": float(D[0][j]), "meta": self.meta[I[0][j]]} for j in range(k)]
