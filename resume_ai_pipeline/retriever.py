from vector_store import VectorStore

def get_context(query, store: VectorStore, top_k=5):
    hits = store.search(query, k=top_k)
    context = "\n\n---\n\n".join([h["meta"]["text"] for h in hits])
    return context, hits
