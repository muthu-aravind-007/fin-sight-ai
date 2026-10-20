import json
import re
import time

from app.rag.document_processor import (
    process_document
)

from app.rag.multi_document_store import (
    build_multi_document_store,
    build_cache_key,
)

from app.rag.retriever import (
    get_retriever
)

from app.rag.hybrid_retriever import (
    get_bm25_retriever
)

from app.rag.reranker import (
    rerank_documents
)

from app.prompts.multi_rag_prompt import (
    build_multi_rag_prompt
)

from app.services.llm_service import (
    generate_analysis
)

from app.rag.query_expander import (
    expand_query
)

from app.rag.question_parser import (
    parse_question
)

def analyze_multiple_transcripts(
    documents,
    question
):
    
    overall_t = time.time()

    all_chunks = []

    # ------------------------
    # Process Documents
    # ------------------------

    for doc in documents:

        t = time.time()

        chunks = process_document(
            doc["pdf_path"],
            doc["company"],
            doc["quarter"]
        )

        print(
            "Document Processing:",
            round(time.time() - t, 2),
            "sec"
        )

        print(
            f"{doc['company']} -> {len(chunks)} chunks"
        )

        all_chunks.extend(
            chunks
        )

    # ------------------------
    # Parse Question
    # ------------------------

    question_data = parse_question(
        question
    )

    comparison_mode = (
        question_data.get(
            "comparison_mode",
            False
        )
    )

    filtered_chunks = all_chunks

    # ------------------------
    # Company Filtering
    # ------------------------

    with open(
        "data/company_registry.json",
        "r",
        encoding="utf-8"
    ) as f:

        company_registry = json.load(f)

    question_lower = question.lower()

    mentioned_companies = []

    for company in company_registry:

        aliases = company.get(
            "aliases",
            []
        )

        if any(
            re.search(
                rf"\b{re.escape(alias.lower())}\b",
                question_lower
            )
            for alias in aliases
        ):

            mentioned_companies.append(
                company["ticker"]
            )

    # Remove duplicates while preserving order
    mentioned_companies = list(
        dict.fromkeys(mentioned_companies)
    )

    # For comparison questions, use companies
    # represented in the uploaded transcripts.
    if comparison_mode:
        uploaded_companies = list(
            dict.fromkeys(
                chunk.metadata.get("company")
                for chunk in all_chunks
                if chunk.metadata.get("company")
            )
        )

        if len(uploaded_companies) >= 2:
            mentioned_companies = uploaded_companies


    print(
        "\nMentioned Companies:",
        mentioned_companies
    )

    if mentioned_companies:

        filtered_chunks = [

            chunk

            for chunk in filtered_chunks

            if chunk.metadata.get(
                "company"
            ) in mentioned_companies

        ]

        print(
            f"\nCompany Filter: {mentioned_companies}"
        )

        print(
            f"Chunks Remaining: {len(filtered_chunks)}"
        )

    # ------------------------
    # Quarter Filtering
    # ------------------------

    quarters = question_data.get(
        "quarters",
        []
    )

    if quarters:

        filtered_chunks = [

            chunk

            for chunk in filtered_chunks

            if chunk.metadata.get(
                "quarter"
            ) in quarters

        ]

        print(
            f"\nQuarter Filter: {quarters}"
        )

        print(
            f"Chunks Remaining: {len(filtered_chunks)}"
        )

    # ------------------------
    # No Matching Documents
    # ------------------------

    if not filtered_chunks:

        return {
            "answer": (
                "No relevant transcript content found."
            ),
            "context": ""
        }

    # ------------------------
    # Build Retrieval Index
    # ------------------------

    print(
        f"\nChunks going into retrieval: "
        f"{len(filtered_chunks)}"
    )

    cache_key = build_cache_key(documents)

    t = time.time()

    # Always index the complete uploaded corpus.
    # Never build the shared index from question-filtered chunks.
    db = build_multi_document_store(
        all_chunks,
        cache_key,
    )

    metadata_conditions = []

    if mentioned_companies:
        metadata_conditions.append({
            "company": {
                "$in": mentioned_companies
            }
        })

    if quarters:
        metadata_conditions.append({
            "quarter": {
                "$in": quarters
            }
        })

    metadata_filter = None

    if len(metadata_conditions) == 1:
        metadata_filter = metadata_conditions[0]
    elif len(metadata_conditions) > 1:
        metadata_filter = {
            "$and": metadata_conditions
        }

    vector_retriever = get_retriever(
        db,
        metadata_filter=metadata_filter,
    )

    bm25_retriever = get_bm25_retriever(
        filtered_chunks
    )

    expanded_question = expand_query(question)

    print(
        "Vector Store:",
        round(time.time() - t, 2),
        "sec"
    )

    # ------------------------
    # Hybrid Retrieval
    # ------------------------

    t = time.time()

    vector_results = (
        vector_retriever.invoke(
            expanded_question
        )
    )

    print(
        "Vector Retrieval:",
        round(time.time() - t, 2),
        "sec"
    )

    t = time.time()

    bm25_results = (
        bm25_retriever.invoke(
            expanded_question
        )
    )

    print(
        "BM25 Retrieval:",
        round(time.time() - t, 2),
        "sec"
    )

    
    # ------------------------
    # Reciprocal Rank Fusion
    # ------------------------

    def reciprocal_rank_fusion(
        ranked_lists,
        k=60
    ):
        scores = {}
        documents = {}

        for ranked_list in ranked_lists:
            for rank, doc in enumerate(
                ranked_list,
                start=1
            ):
                key = (
                    doc.metadata.get("company"),
                    doc.metadata.get("quarter"),
                    doc.metadata.get("page"),
                    doc.page_content
                )

                scores[key] = (
                    scores.get(key, 0.0)
                    + 1.0 / (k + rank)
                )

                documents[key] = doc

        ranked_keys = sorted(
            scores,
            key=lambda key: scores[key],
            reverse=True
        )

        return [
            documents[key]
            for key in ranked_keys
        ]


    results = reciprocal_rank_fusion([
        vector_results,
        bm25_results
    ])


    # ------------------------
    # Deduplicate
    # ------------------------

    final_results = []
    seen_pages = set()

    for doc in results:

        key = (
            doc.metadata.get("company"),
            doc.metadata.get("quarter"),
            doc.metadata.get("page"),
            doc.page_content
        )

        if key not in seen_pages:

            seen_pages.add(key)
            final_results.append(doc)

    results = final_results

    # ------------------------
    # Empty Retrieval Protection
    # ------------------------

    if not results:

        return {
            "answer": (
                "No relevant information "
                "found in transcripts."
            ),
            "context": ""
        }

    # ------------------------
    # Rerank
    # ------------------------

    t = time.time()

    if comparison_mode and len(mentioned_companies) >= 2:
        grouped_results = []

        for company in mentioned_companies:
            company_docs = [
                doc
                for doc in results
                if doc.metadata.get("company") == company
            ]

            if not company_docs:
                continue

            company_docs = rerank_documents(
                expanded_question,
                company_docs,
                top_k=5,
            )

            grouped_results.extend(company_docs)

        results = grouped_results

    else:
        results = rerank_documents(
            expanded_question,
            results,
            top_k=8,
        )

    print(
        "Reranking:",
        round(time.time() - t, 2),
        "sec",
    )

    print("\nRetrieved Documents:")

    for doc in results:

        print(
            doc.metadata.get("company"),
            doc.metadata.get("quarter"),
            doc.metadata.get("page")
        )

    # ------------------------
    # Build Context
    # ------------------------

    sources = []

    context_parts = []

    for doc in results:

        company = doc.metadata.get(
            "company",
            "Unknown"
        )

        quarter = doc.metadata.get(
            "quarter",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        sources.append(
            {
                "company": company,
                "quarter": quarter,
                "page": page
            }
        )

        source_id = (
            f"{company}-"
            f"{quarter}-"
            f"{page}"
        )

        context_parts.append(
            f"""
            Source ID: {source_id}

            Company: {company}
            Quarter: {quarter}
            Page: {page}

            {doc.page_content}

            ----------------------------------------
            """
        )

    context = "\n\n".join(
        context_parts
    )

    comparison_mode = (
        question_data.get(
            "comparison_mode",
            False
        )
    )

    prompt = build_multi_rag_prompt(
        context,
        question,
        comparison_mode,
        question_data.get("analysis_intent", "general"),
    )

    print(
        "Chunks sent to LLM:",
        len(results)
    )

    print(
        "Context Length:",
        len(context),
        "characters"
    )

    t = time.time()

    answer = generate_analysis(
        prompt,
        comparison_mode
    )

    print(
        "LLM Generation:",
        round(time.time() - t, 2),
        "sec"
    )

    print(
        "TOTAL PIPELINE:",
        round(time.time() - overall_t, 2),
        "sec"
    )
    return {
        "answer": answer,
        "context": context,
        "sources": sources
    }