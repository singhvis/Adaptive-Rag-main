"""
Retriever setup and vector store configuration (LLM Studio compatible).
"""

import os
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_core.tools import create_retriever_tool
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from src.core.config import settings

# Load environment variables
load_dotenv()

# Use LLM Studio embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Global vector store
_faiss_vectorstore = None


def retriever_chain(chunks: list[Document]):
    """Initialize and store documents in FAISS vector database."""
    global _faiss_vectorstore

    try:
        if not chunks:
            print("⚠️ No chunks provided to retriever_chain")
            return False

        vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=embeddings
        )

        _faiss_vectorstore = vectorstore

        print("✅ FAISS vector store initialized successfully")
        print(f"📄 Stored {len(chunks)} document chunks")

        return True

    except Exception as e:
        print(f"❌ Error storing documents in FAISS: {e}")
        return False


def get_retriever():
    """Get a retriever tool connected to the FAISS vector store."""
    global _faiss_vectorstore

    try:
        if _faiss_vectorstore is not None:
            print("✅ Using existing FAISS vectorstore")
            retriever = _faiss_vectorstore.as_retriever()
        else:
            print("⚠️ No documents uploaded → creating dummy vectorstore")

            dummy_doc = Document(
                page_content="No documents uploaded yet. Please upload documents first.",
                metadata={"source": "init"}
            )

            _faiss_vectorstore = FAISS.from_documents(
                documents=[dummy_doc],
                embedding=embeddings
            )

            retriever = _faiss_vectorstore.as_retriever()

        description = "uploaded documents"
        if os.path.exists("description.txt"):
            with open("description.txt", "r", encoding="utf-8") as f:
                description = f.read().strip()

        retriever_tool = create_retriever_tool(
            retriever,
            "retriever_customer_uploaded_documents",
            f"Use this tool ONLY for answering questions related to: {description}. "
            "Do NOT use this tool for general knowledge questions."
        )

        return retriever_tool

    except Exception as e:
        print(f"❌ Error initializing retriever: {e}")
        raise Exception(e)
