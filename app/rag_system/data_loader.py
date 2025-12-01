import os
from app.rag_system.pdf_loader import (
    load_pdf_files,
    chunk_documents as create_text_chunks,
)
from app.rag_system.vector_store import load_vectorstore, save_vectorstore
from app.config.settings import DB_FAISS_PATH

from app.utils.logger import get_logger
from app.utils.custom_exception import CustomException

logger = get_logger(__name__)


def process_and_store_pdfs():
    try:
        logger.info("Making the vectorstore....")
        db = load_vectorstore(DB_FAISS_PATH)
        if db is not None:
            logger.info("Vectorstore already exists")
            return
        documents = load_pdf_files()

        text_chunks = create_text_chunks(documents)
        save_vectorstore(text_chunks)

        logger.info("Vectorstore created sucesfully....")

    except Exception as e:
        error_message = CustomException("Faialedd to create vectorstore", e)
        logger.error(str(error_message))


if __name__ == "__main__":
    process_and_store_pdfs()
