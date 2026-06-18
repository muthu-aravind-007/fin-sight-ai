from langchain_core.documents import Document

from app.rag.vector_store import (
    create_vector_store
)

docs = [
    Document(
        page_content=
        "NVIDIA revenue increased 20 percent."
    ),

    Document(
        page_content=
        "Management expects strong AI demand."
    )
]

db = create_vector_store(
    docs
)

print(
    db._collection.count()
)