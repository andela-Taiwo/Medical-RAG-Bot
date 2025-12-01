# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from app.config.settings import HF_TOKEN
from app.utils.custom_exception import CustomException
from app.utils.logger import get_logger

logger = get_logger(__name__)


def get_embeddings_model(
    model_name: str = "all-MiniLM-L6-v2", hf_token: str = HF_TOKEN
):
    try:
        logger.info("Creating HuggingFace embeddings instance")
        hf_embeddings = HuggingFaceEmbeddings(model_name=model_name)
        logger.info("HuggingFace embeddings instance created successfully")
        return hf_embeddings
    except Exception as e:
        error = CustomException("Failed to get HuggingFace embeddings", e)
        logger.error(str(error))
        return None
