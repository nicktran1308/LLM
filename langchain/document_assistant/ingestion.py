# ------------------------------- Import Libraries -------------------------------
import os
from langchain.document_loaders import ReadTheDocsLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
import pinecone

# ------------------------------- Pinecone Initialization -------------------------------
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
)
INDEX_NAME = "langchain-doc-index"

# ------------------------------- Ingest Documents -------------------------------
def ingest_docs():
    """
    Load documents from ReadTheDocs, process them, and add them to a Pinecone vector store.
    """
    # Load raw documents from ReadTheDocs
    loader = ReadTheDocsLoader("python.langchain.com/en/latest/index.html")
    raw_documents = loader.load()
    print(f"Loaded {len(raw_documents)} documents.")
    
    # Split raw documents into smaller chunks
    # Need to look more into Chunking Strategies
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400, chunk_overlap=50, separators=["\n\n", "\n", " ", ""]
    )
    documents = text_splitter.split_documents(raw_documents)
    
    # Update document metadata URLs
    for doc in documents:
        new_url = doc.metadata["source"].replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    # Embed documents and add to Pinecone vector store
    embeddings = OpenAIEmbeddings()
    print(f"Adding {len(documents)} documents to Pinecone.")
    Pinecone.from_documents(documents, embeddings, index_name=INDEX_NAME)
    print("Document loading to vector store completed.")

# ------------------------------- Main Execution -------------------------------
if __name__ == "__main__":
    ingest_docs()

