import os
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.utils.custom_exception import CustomException
from app.utils.logger import get_logger
from app.config.settings import DATA_PATH, CHUNK_OVERLAP, CHUNK_SIZE

logger = get_logger(__name__)


def load_pdf_files():
    try:
        if not os.path.exists(DATA_PATH):
            print(f"Data path {DATA_PATH} does not exist")
            return []

        # Look for various PDf document types in the data directory
        loader = DirectoryLoader(
            DATA_PATH,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            show_progress=True,  # Load all file types
        )

        documents = loader.load()
        return documents

    except Exception as e:
        logger.error(f"Error loading documents: {str(e)}")
        return []


def chunk_documents(documents: List[Document]) -> Optional[List[Document]]:
    try:
        if not len(documents):
            logger.warning("No documeents to chunk")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
        )
        logger.info("Splitting documents")
        text_chunks = text_splitter.split_documents(documents)
        return text_chunks

    except Exception as e:
        error = CustomException("Failed during chunking process", e)
        logger.error(str(error))
        return []
