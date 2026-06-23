def get_retriever(db):

    return db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 20,
            "fetch_k": 75
        }
    )