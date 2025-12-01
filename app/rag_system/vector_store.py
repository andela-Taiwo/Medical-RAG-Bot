import os
from langchain_community.vectorstores import FAISS
from app.config.settings import DB_FAISS_PATH
from app.utils.custom_exception import CustomException
from app.utils.logger import get_logger
from .embeddings import get_embeddings_model
from typing import List
from langchain_core.documents import Document

logger = get_logger(__name__)


def save_vectorstore(text_chunks: List[Document] = []):
    try:
        model = get_embeddings_model()

        if len(text_chunks) == 0:
            error = CustomException(
                "Cannot create vectorstore: no documents provided and no existing vectorstore found"
            )
            logger.error(str(error))
            return None

        vectorstore = FAISS.from_documents(documents=text_chunks, embedding=model)
        logger.info("Saving vectorstore to file")
        vectorstore.save_local(DB_FAISS_PATH)
        logger.info("Vectorstore instance created successfully")
        return vectorstore
    except Exception as e:
        error = CustomException("Failed to load vectorstore", e)
        logger.error(str(error))
        return None


def load_vectorstore(db_path: str = None):
    try:
        logger.info("Loading vectorstore from file")
        model = get_embeddings_model()
        if os.path.exists(db_path):
            return FAISS.load_local(
                db_path, model, allow_dangerous_deserialization=True
            )
        else:
            error = CustomException("Vectorstore file not found")
            logger.error(str(error))
            return None
    except Exception as e:
        error = CustomException("Failed to load vectorstore", e)
        logger.error(str(error))
        return None
