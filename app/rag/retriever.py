def get_retriever(db, metadata_filter=None):
    search_kwargs = {
        "k": 10,
        "fetch_k": 30,
    }

    if metadata_filter:
        search_kwargs["filter"] = metadata_filter

    return db.as_retriever(
        search_type="mmr",
        search_kwargs=search_kwargs,
    )
