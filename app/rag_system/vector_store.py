import os
from langchain_community.vectorstores import FAISS
from app.config.settings import DB_FAISS_PATH
from app.utils.custom_exception import CustomException
from app.utils.logger import get_logger
from .embeddings import get_embeddings_model
from typing import List
from langchain_core.documents import Document

logger = get_logger(__name__)


def load_or_save_vectorstore(text_chunks: List[Document] = []):
    try:
        logger.info("Creating vectorstore instance")
        model = get_embeddings_model()
        if os.path.exists(DB_FAISS_PATH):
            logger.info("Loading vectorstore from existing file")
            vectorstore = FAISS.load_local(DB_FAISS_PATH, model)
        else:
            logger.info("Creating new vectorstore")
            vectorstore = FAISS.from_documents(documents=text_chunks, embedding=model)
            vectorstore.save_local(DB_FAISS_PATH)
        logger.info("Vectorstore instance created successfully")
        return vectorstore
    except Exception as e:
        error = CustomException("Failed to load vectorstore", e)
        logger.error(str(error))
        return None
