from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
import os

def build_vector_store():

    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    documents = []

    for file in os.listdir("knowledge_base"):
        loader = TextLoader(f"knowledge_base/{file}")
        documents.extend(loader.load())

    db = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory="db"
    )

    return db