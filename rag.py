import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

CASE_STUDY_FOLDER = "case_studies"

def load_case_studies():
    documents = []

    print("Reading case study files...")

    for filename in os.listdir(CASE_STUDY_FOLDER):

        if filename.endswith(".txt"):

            path = os.path.join(
                CASE_STUDY_FOLDER,
                filename
            )

            with open(path, "r") as f:
                content = f.read()

            documents.append(content)

    print(f"Loaded {len(documents)} case studies")

    return documents


def create_vector_store(documents):

    print("Creating embeddings...")

    embeddings = model.encode(documents)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    print("Vector store created")

    return index


def search_similar_cases(query,
                         documents,
                         index):

    print("Searching similar cases...")

    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding),
        k=2
    )

    results = []

    for idx in indices[0]:
        results.append(documents[idx])

    return results


if __name__ == "__main__":

    docs = load_case_studies()

    index = create_vector_store(docs)

    query = "manual data transfer between systems"

    results = search_similar_cases(
        query,
        docs,
        index
    )

    print("\n--- SIMILAR CASES FOUND ---\n")

    for r in results:
        print(r[:300])
        print("\n------------------\n")