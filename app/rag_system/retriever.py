from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from .llm import get_groq_model
from .vector_store import save_vectorstore, load_vectorstore
from app.config.settings import DB_FAISS_PATH
from app.utils.custom_exception import CustomException
from app.utils.logger import get_logger


logger = get_logger(__name__)

CUSTOM_PROMPT_TEMPLATE = """
    Answer the following medical question in 2-3 lines maximum using only the information provided in the context.

    Context:
    {context}

    Question:
    {question}

    Answer:
"""


def set_custom_prompt(prompt_template: str = CUSTOM_PROMPT_TEMPLATE):
    return PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )


def create_qa_chain():
    try:
        logger.info("Loading vectorstore")

        db = load_vectorstore(DB_FAISS_PATH)

        if db is None:
            error = CustomException("Failed to load vectorstore")
            logger.error(str(error))
            return None

        logger.info("Creating QA chain")

        llm = get_groq_model()

        if llm is None:
            error = CustomException("Failed to get Groq model")
            logger.error(str(error))
            return None

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": set_custom_prompt()},
        )
        logger.info("QA chain created successfully")
        return qa_chain
    except Exception as e:
        error = CustomException("Failed to create QA chain", e)
        logger.error(str(error))
        return None
