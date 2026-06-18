from langchain_core.documents import Document

from app.rag.retriever import (
    retrieve_documents
)

docs = [

    Document(
        page_content=
        "NVIDIA revenue increased 20 percent."
    ),

    Document(
        page_content=
        "Management expects strong AI demand."
    ),

    Document(
        page_content=
        "Margins may decline due to investments."
    )

]

results = retrieve_documents(
    docs,
    "AI demand"
)

for r in results:
    print(r.page_content)