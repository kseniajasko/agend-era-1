from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import DATABASE_URL

text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n"],
    chunk_size=500,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,  # literal "\n\n"
)
collection_name = "resumes"
vectorstore = PGVector(
    embeddings=OpenAIEmbeddings(),
    collection_name=collection_name,
    connection=DATABASE_URL,
    use_jsonb=True,
)


def get_retriever():
    return vectorstore.as_retriever()


def create_vectorstore_data():
    current_dir = Path(__file__).resolve().parent
    files_dir = current_dir.parent / "files"
    pdf_paths = sorted(files_dir.glob("*.pdf"))
    for author_id, pdf_path in enumerate(pdf_paths, start=1):
        loader = PyPDFLoader(str(pdf_path))
        documents = loader.load()
        pages = text_splitter.split_documents(documents)
        for page in pages:
            page.metadata["author_id"] = author_id
        vectorstore.add_documents(documents=pages)


if __name__ == "__main__":
    create_vectorstore_data()
