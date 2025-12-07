from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_index(documents):
    vectors = model.encode(documents, convert_to_numpy=True)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    return index, vectors

def query_index(index, documents, query):
    q_vec = model.encode([query], convert_to_numpy=True)
    D, I = index.search(q_vec, 3)
    return [documents[i] for i in I[0]]
