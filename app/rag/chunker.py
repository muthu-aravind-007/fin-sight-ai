
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
        chunk_size=800,
        chunk_overlap=150,
        add_start_index=True,
    )

    chunks = splitter.split_documents(documents)

    for chunk in chunks:
        chunk.metadata["chunk_start"] = chunk.metadata.get(
            "start_index",
            0,
        )

    return chunks
