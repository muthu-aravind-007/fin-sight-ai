from app.rag.pdf_loader import load_pdf

path = r"data/uploads/aapl_q3_2026.pdf"

documents = load_pdf(path)

print("Pages with extracted text:", len(documents))
print("Total extracted characters:", sum(
    len(doc.page_content) for doc in documents
))

for doc in documents[:2]:
    print("\nPage:", doc.metadata.get("page"))
    print(doc.page_content[:500])