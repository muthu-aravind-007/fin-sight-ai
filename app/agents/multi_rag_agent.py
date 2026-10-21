
import re
import time

from app.rag.document_processor import process_document
from app.rag.multi_document_store import (
    build_multi_document_store,
    build_cache_key,
)
from app.rag.retriever import get_retriever
from app.rag.hybrid_retriever import get_bm25_retriever
from app.rag.reranker import rerank_documents
from app.prompts.multi_rag_prompt import build_multi_rag_prompt
from app.services.llm_service import generate_analysis
from app.rag.query_expander import expand_query
from app.rag.question_parser import parse_question


def analyze_multiple_transcripts(documents, question):
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
            doc["quarter"],
        )

        print(
            "Document Processing:",
            round(time.time() - t, 2),
            "sec",
        )
        print(f"{doc['company']} -> {len(chunks)} chunks")

        all_chunks.extend(chunks)

    if not all_chunks:
        return {
            "answer": "No transcript content could be extracted from the uploaded PDFs.",
            "context": "",
            "sources": [],
        }

    # ------------------------
    # Parse Question
    # ------------------------
    question_data = parse_question(question)
    comparison_mode = question_data.get("comparison_mode", False)
    quarters = question_data.get("quarters", [])

    uploaded_companies = list(dict.fromkeys(
        str(doc["company"]).strip().upper()
        for doc in documents
        if doc.get("company")
    ))

    # Only match tickers belonging to uploaded documents.
    question_upper = question.upper()
    explicitly_mentioned_companies = [
        company
        for company in uploaded_companies
        if re.search(
            rf"(?<![A-Z0-9]){re.escape(company)}(?![A-Z0-9])",
            question_upper,
        )
    ]

    # An explicitly named ticker narrows the query unless the user
    # is comparing multiple companies. Otherwise, use the uploaded corpus.
    if explicitly_mentioned_companies:
        companies_used = explicitly_mentioned_companies
    else:
        companies_used = uploaded_companies

    # Treat broad questions over multiple uploaded transcripts as
    # cross-company questions, even if the user doesn't type "compare".
    cross_company_mode = (
        len(companies_used) > 1
        and (
            comparison_mode
            or not explicitly_mentioned_companies
        )
    )

    print("\nUploaded Companies:", uploaded_companies)
    print("Explicitly Mentioned:", explicitly_mentioned_companies)
    print("Companies Used:", companies_used)
    print("Cross-Company Retrieval:", cross_company_mode)

    # ------------------------
    # Apply Company / Quarter Scope
    # ------------------------
    filtered_chunks = [
        chunk
        for chunk in all_chunks
        if str(chunk.metadata.get("company", "")).strip().upper()
        in companies_used
    ]

    if quarters:
        filtered_chunks = [
            chunk
            for chunk in filtered_chunks
            if str(chunk.metadata.get("quarter", "")).strip().upper()
            in [q.upper() for q in quarters]
        ]

        print("Quarter Filter:", quarters)

    print("Chunks Remaining:", len(filtered_chunks))

    if not filtered_chunks:
        return {
            "answer": (
                "No transcript content matches the selected company "
                "and reporting-period filters. Check the uploaded "
                "metadata and the requested quarter."
            ),
            "context": "",
            "sources": [],
        }

    # ------------------------
    # Build / Load Full-Corpus Index
    # ------------------------
    print(f"\nChunks going into retrieval: {len(all_chunks)}")

    cache_key = build_cache_key(documents)
    t = time.time()

    # Keep the vector index independent of the current question.
    db = build_multi_document_store(all_chunks, cache_key)

    print("Vector Store:", round(time.time() - t, 2), "sec")

    expanded_question = expand_query(question)

    # ------------------------
    # Reciprocal Rank Fusion
    # ------------------------
    def reciprocal_rank_fusion(ranked_lists, k=60):
        scores = {}
        documents_by_key = {}

        for ranked_list in ranked_lists:
            for rank, doc in enumerate(ranked_list, start=1):
                key = (
                    str(doc.metadata.get("company", "")).upper(),
                    str(doc.metadata.get("quarter", "")).upper(),
                    doc.metadata.get("page"),
                    doc.page_content,
                )

                scores[key] = scores.get(key, 0.0) + 1.0 / (k + rank)
                documents_by_key[key] = doc

        ranked_keys = sorted(
            scores,
            key=lambda key: scores[key],
            reverse=True,
        )

        return [documents_by_key[key] for key in ranked_keys]

    # ------------------------
    # Hybrid Retrieval
    # ------------------------
    hybrid_start = time.perf_counter()
    results = []

    timings = {
        "bm25_build": 0.0,
        "vector_search": 0.0,
        "bm25_search": 0.0,
        "rrf": 0.0,
        "reranking": 0.0,
    }

    if cross_company_mode:
        # Give each company its own retrieval budget.
        # This prevents one company's many highly ranked chunks
        # from crowding out all the other companies.
        for company in companies_used:
            company_chunks = [
                chunk
                for chunk in filtered_chunks
                if str(chunk.metadata.get("company", "")).strip().upper()
                == company
            ]

            if not company_chunks:
                print(f"No matching chunks for {company}")
                continue

            metadata_conditions = [
                {"company": {"$eq": company}}
            ]

            if quarters:
                metadata_conditions.append({
                    "quarter": {
                        "$in": quarters
                    }
                })

            if len(metadata_conditions) == 1:
                metadata_filter = metadata_conditions[0]
            else:
                metadata_filter = {"$and": metadata_conditions}

            t = time.perf_counter()
            vector_retriever = get_retriever(
                db,
                metadata_filter=metadata_filter,
            )
            timings["vector_setup"] = timings.get("vector_setup", 0.0) + (
                time.perf_counter() - t
            )

            t = time.perf_counter()
            bm25_retriever = get_bm25_retriever(company_chunks)
            timings["bm25_build"] += time.perf_counter() - t

            t = time.perf_counter()
            vector_results = vector_retriever.invoke(expanded_question)
            timings["vector_search"] += time.perf_counter() - t

            t = time.perf_counter()
            bm25_results = bm25_retriever.invoke(expanded_question)
            timings["bm25_search"] += time.perf_counter() - t

            t = time.perf_counter()
            company_results = reciprocal_rank_fusion([
                vector_results,
                bm25_results,
            ])
            timings["rrf"] += time.perf_counter() - t

            # Remove duplicate passages before reranking.
            unique_candidates = []
            seen_candidates = set()

            for doc in company_results:
                key = (
                    str(doc.metadata.get("company", "")).upper(),
                    str(doc.metadata.get("quarter", "")).upper(),
                    doc.metadata.get("page"),
                    doc.page_content,
                )

                if key not in seen_candidates:
                    seen_candidates.add(key)
                    unique_candidates.append(doc)

            t = time.perf_counter()
            company_results = rerank_documents(
                expanded_question,
                unique_candidates,
                top_k=3,
            )
            timings["reranking"] += time.perf_counter() - t

            results.extend(company_results)

            print(
                f"{company}: {len(company_chunks)} available chunks, "
                f"{len(company_results)} selected chunks"
            )

    else:
        # For a single-company query, use the filtered corpus.
        metadata_conditions = []

        if companies_used:
            metadata_conditions.append({
                "company": {
                    "$in": companies_used
                }
            })

        if quarters:
            metadata_conditions.append({
                "quarter": {
                    "$in": quarters
                }
            })

        if len(metadata_conditions) == 1:
            metadata_filter = metadata_conditions[0]
        elif len(metadata_conditions) > 1:
            metadata_filter = {"$and": metadata_conditions}
        else:
            metadata_filter = None

        vector_retriever = get_retriever(
            db,
            metadata_filter=metadata_filter,
        )
        bm25_retriever = get_bm25_retriever(filtered_chunks)

        vector_results = vector_retriever.invoke(expanded_question)
        bm25_results = bm25_retriever.invoke(expanded_question)

        results = reciprocal_rank_fusion([
            vector_results,
            bm25_results,
        ])

        results = rerank_documents(
            expanded_question,
            results,
            top_k=8,
        )

    print("\n========== RETRIEVAL TIMINGS ==========")

    for stage, seconds in timings.items():
        print(f"{stage}: {seconds:.2f} sec")

    print(
        "Hybrid Retrieval Total:",
        round(time.perf_counter() - hybrid_start, 2),
        "sec",
    )
    print("=======================================\n")

    # ------------------------
    # Deduplicate
    # ------------------------
    final_results = []
    seen_chunks = set()

    for doc in results:
        key = (
            str(doc.metadata.get("company", "")).upper(),
            str(doc.metadata.get("quarter", "")).upper(),
            doc.metadata.get("page"),
            doc.page_content,
        )

        if key not in seen_chunks:
            seen_chunks.add(key)
            final_results.append(doc)

    results = final_results

    if not results:
        return {
            "answer": "No relevant information was retrieved from the matching transcripts.",
            "context": "",
            "sources": [],
        }

    # ------------------------
    # Evidence Coverage
    # ------------------------
    retrieved_companies = list(dict.fromkeys(
        str(doc.metadata.get("company", "")).strip().upper()
        for doc in results
        if doc.metadata.get("company")
    ))

    missing_companies = [
        company
        for company in companies_used
        if company not in retrieved_companies
    ]

    print("\nRetrieved Documents:")
    for doc in results:
        print(
            doc.metadata.get("company"),
            doc.metadata.get("quarter"),
            doc.metadata.get("page"),
        )

    print("Companies with Retrieved Evidence:", retrieved_companies)
    print("Companies without Retrieved Evidence:", missing_companies)

    # ------------------------
    # Build Context
    # ------------------------
    sources = []
    context_parts = []

    for index, doc in enumerate(results, start=1):
        company = doc.metadata.get("company", "Unknown")
        quarter = doc.metadata.get("quarter", "Unknown")
        page = doc.metadata.get("page", "Unknown")

        source_id = f"S{index}"

        sources.append({
            "source_id": source_id,
            "company": company,
            "quarter": quarter,
            "page": page,
        })

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

    context = "\n\n".join(context_parts)

    # Tell the model which companies were not represented in retrieval.
    coverage_note = ""
    if missing_companies:
        coverage_note = (
            "\n\nRETRIEVAL COVERAGE WARNING:\n"
            f"No chunks were retrieved for: {', '.join(missing_companies)}.\n"
            "Do not invent facts for these companies. State that the "
            "retrieved evidence is insufficient to assess them."
        )

    context = context + coverage_note

    prompt = build_multi_rag_prompt(
        context,
        question,
        cross_company_mode,
        question_data.get("analysis_intent", "general"),
    )

    print("Chunks sent to LLM:", len(results))
    print("Context Length:", len(context), "characters")

    # ------------------------
    # Generate Answer
    # ------------------------
    t = time.time()

    answer = generate_analysis(
    prompt,
    cross_company_mode,
    num_predict=1400,
    )
    
    
    # ------------------------
    # Validate Answer Coverage
    # ------------------------
    answer_upper = answer.upper()

    omitted_companies = [
        company
        for company in retrieved_companies
        if not re.search(
            rf"(?<![A-Z0-9]){re.escape(company)}(?![A-Z0-9])",
            answer_upper,
        )
    ]

    if omitted_companies:
        print(
            "WARNING: Companies potentially omitted from the final answer:",
            omitted_companies,
        )
    else:
        print("Answer coverage check: all retrieved company identifiers mentioned.")


    print("LLM Generation:", round(time.time() - t, 2), "sec")
    print("TOTAL PIPELINE:", round(time.time() - overall_t, 2), "sec")


    return {
        "answer": answer,
        "context": context,
        "sources": sources,
        "companies_used": companies_used,
        "retrieved_companies": retrieved_companies,
        "missing_companies": missing_companies,
    }
