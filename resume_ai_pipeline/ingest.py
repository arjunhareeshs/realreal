from extractors import extract_text_auto
from sectioning import detect_sections
from chunking import chunk_text
from vector_store import VectorStore
import uuid, os

def ingest_file(path, store: VectorStore):
    text = extract_text_auto(path)
    sections = detect_sections(text)
    all_chunks, metas = [], []
    for sec, body in sections.items():
        for i, ch in enumerate(chunk_text(body)):
            metas.append({
                "id": str(uuid.uuid4()),
                "source": os.path.basename(path),
                "section": sec,
                "chunk_index": i
            })
            all_chunks.append(ch)
    store.add(all_chunks, metas)
    store.save()
    print(f"✅ Ingested {len(all_chunks)} chunks from {path}")
