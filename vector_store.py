import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_vector_store(documents):
    vectors = model.encode(documents)

    dimension = len(vectors[0])
    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(vectors))

    return index, documents


def retrieve(query, index, documents):
    query_vector = model.encode([query])

    # 🔥 increase k here (not above)
    D, I = index.search(np.array(query_vector), k=5)

    results = [documents[i] for i in I[0]]

    return "\n".join(results)