import nltk
nltk.download('punkt', quiet=True)
from nltk.tokenize import sent_tokenize

def chunk_text(text, max_words=500, overlap=80):
    sents = sent_tokenize(text)
    chunks, cur, count = [], [], 0
    for s in sents:
        w = len(s.split())
        if count + w > max_words:
            chunks.append(" ".join(cur))
            cur = cur[-(overlap//10):]  # keep small overlap
            count = sum(len(x.split()) for x in cur)
        cur.append(s); count += w
    if cur: chunks.append(" ".join(cur))
    return chunks
