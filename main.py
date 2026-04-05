from analyzer import analyze_transcript
from rag import (
    load_case_studies,
    create_vector_store,
    search_similar_cases
)
from generator import generate_solution_document


def main():

    print("Starting Enterprise Integration Agent...\n")

    # Read transcript
    with open(
        "transcripts/sample_transcript.txt",
        "r"
    ) as f:

        transcript = f.read()

    # STEP 1 — Analyze transcript
    client_info = analyze_transcript(
        transcript
    )

    # STEP 2 — Load case studies
    documents = load_case_studies()

    index = create_vector_store(
        documents
    )

    # STEP 3 — Search similar cases
    query = " ".join(
        client_info["pain_points"]
    )

    similar_cases = search_similar_cases(
        query,
        documents,
        index
    )

    # STEP 4 — Generate document
    generate_solution_document(
        client_info,
        similar_cases
    )

    print("\n🎉 FULL PIPELINE COMPLETED!")


if __name__ == "__main__":
    main()