from langchain_groq import ChatGroq
from app.config.settings import GROQ_API_KEY
from app.utils.custom_exception import CustomException
from app.utils.logger import get_logger

logger = get_logger(__name__)


def get_groq_model(
    model_name: str = "llama-3.1-8b-instant", grop_api_key: str = GROQ_API_KEY
):
    try:
        logger.info("Creating model instance")
        groq_model = ChatGroq(
            model=model_name,
            api_key=grop_api_key,
            temperature=0.3,
            max_tokens=1024,
        )
        logger.info("Model instance created successfully")
        return groq_model
    except Exception as e:
        error = CustomException("Failed to get Groq model", e)
        logger.error(str(error))
        return None
