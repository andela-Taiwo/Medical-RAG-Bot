# Medical RAG Chatbot

A Retrieval-Augmented Generation (RAG) based medical chatbot that answers medical questions using information from medical PDF documents. The application uses advanced NLP techniques to retrieve relevant context from medical literature and generate accurate, concise answers.

## 🎯 Overview

This application is a web-based medical question-answering system that:
- Processes medical PDF documents and converts them into searchable vector embeddings
- Retrieves relevant medical information based on user queries
- Generates accurate, concise answers using a Large Language Model (LLM)
- Provides an intuitive web interface for medical Q&A

## 🏗️ Architecture

### Components

1. **PDF Loader** (`app/rag_system/pdf_loader.py`)
   - Loads PDF files from the `data/` directory
   - Splits documents into chunks using recursive character text splitting
   - Configurable chunk size (500) and overlap (50)

2. **Embeddings** (`app/rag_system/embeddings.py`)
   - Uses HuggingFace embeddings model (`all-MiniLM-L6-v2`)
   - Converts text chunks into vector representations for semantic search

3. **Vector Store** (`app/rag_system/vector_store.py`)
   - Uses FAISS (Facebook AI Similarity Search) for efficient vector storage and retrieval
   - Persists vector database to disk for reuse
   - Enables fast similarity search across medical documents

4. **Retriever** (`app/rag_system/retriever.py`)
   - Creates a RetrievalQA chain using LangChain
   - Retrieves relevant document chunks based on user queries
   - Uses custom prompt template for medical Q&A

5. **LLM** (`app/rag_system/llm.py`)
   - Uses Groq API with `llama-3.1-8b-instant` model
   - Configured with temperature=0.3 for consistent, factual responses
   - Max tokens: 1024 for concise answers

6. **Web Application** (`app/application.py`)
   - Flask-based web interface
   - Session-based conversation history
   - RESTful API endpoints

## 🔄 Application Workflow

### 1. Initialization Phase
```
PDF Documents → Load & Parse → Text Chunking → Generate Embeddings → Store in FAISS
```

1. **Document Loading**: PDFs from `data/` directory are loaded using PyPDFLoader
2. **Text Chunking**: Documents are split into manageable chunks (500 chars with 50 char overlap)
3. **Embedding Generation**: Each chunk is converted to a vector using HuggingFace embeddings
4. **Vector Storage**: Embeddings are stored in FAISS vector database and persisted to `vectorstore/db_faiss/`

### 2. Query Processing Phase
```
User Query → Embed Query → Similarity Search → Retrieve Context → Generate Answer
```

1. **Query Input**: User submits a medical question via web interface
2. **Query Embedding**: Query is converted to vector representation
3. **Similarity Search**: FAISS finds most relevant document chunks
4. **Context Retrieval**: Top relevant chunks are retrieved as context
5. **Answer Generation**: LLM generates answer using retrieved context and custom prompt

### 3. Response Generation
- Custom prompt template ensures answers are:
  - Based only on provided context
  - Concise (2-3 lines maximum)
  - Medical question-focused

## 🚀 Development Workflow

### Prerequisites

- Python 3.13+
- Virtual environment (venv, conda, or uv)
- API Keys:
  - **Groq API Key**: Get from [Groq Console](https://console.groq.com/)
  - **HuggingFace Token**: Get from [HuggingFace Settings](https://huggingface.co/settings/tokens) (optional, for private models)

### Local Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd rag-medical-bot
   ```

2. **Create Virtual Environment**
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Or using uv (recommended)
   uv venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   # Using pip
   pip install -e .
   
   # Or using uv
   uv pip install -e .
   ```

4. **Configure Environment Variables**
   
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   HF_TOKEN=your_huggingface_token_here  # Optional
   ```

5. **Add Medical PDF Documents**
   
   Place your medical PDF files in the `data/` directory:
   ```bash
   # Example structure
   data/
     ├── medical_book_1.pdf
     ├── medical_book_2.pdf
     └── ...
   ```

6. **Initialize Vector Store** (First Run)
   
   The vector store is automatically created on first run. Alternatively, you can initialize it manually:
   ```bash
   python -m app.rag_system.data_loader
   ```

7. **Run the Application**
   ```bash
   python app/application.py
   # Or
   flask run --host=0.0.0.0 --port=8000
   ```

8. **Access the Application**
   
   Open your browser and navigate to: `http://localhost:8000`

### Development Commands

```bash
# Run the application
python app/application.py

# Initialize/rebuild vector store
python -m app.rag_system.data_loader

# Run linting (if configured)
ruff check .

# Run tests (if available)
pytest
```

### Project Structure

```
rag-medical-bot/
├── app/
│   ├── __init__.py
│   ├── application.py          # Flask web application
│   ├── config/
│   │   └── settings.py         # Configuration settings
│   ├── rag_system/
│   │   ├── data_loader.py      # PDF processing pipeline
│   │   ├── embeddings.py       # Embedding model setup
│   │   ├── llm.py             # LLM model setup
│   │   ├── pdf_loader.py       # PDF loading and chunking
│   │   ├── retriever.py        # QA chain creation
│   │   └── vector_store.py     # FAISS vector store management
│   ├── templates/
│   │   └── index.html          # Web interface template
│   └── utils/
│       ├── custom_exception.py # Custom exception handling
│       └── logger.py           # Logging configuration
├── data/                       # Medical PDF documents directory
├── vectorstore/                # FAISS vector database storage
│   └── db_faiss/
├── logs/                       # Application logs
├── main.py                     # Entry point
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project configuration
├── setup.py                    # Package setup
├── README.md                   # This file
└── wiki.md                     # Deployment documentation
```

### Configuration

Key configuration settings in `app/config/settings.py`:

- `CHUNK_SIZE`: 500 (characters per chunk)
- `CHUNK_OVERLAP`: 50 (overlap between chunks)
- `DB_FAISS_PATH`: `"vectorstore/db_faiss"` (vector store location)
- `DATA_PATH`: `"data/"` (PDF documents directory)
- `HUGGINGFACE_REPO_ID`: `"mistralai/Mistral-7B-Instruct-v0.3"` (for future use)

### Adding New Documents

1. Place new PDF files in the `data/` directory
2. Delete the existing vector store (optional, for clean rebuild):
   ```bash
   rm -rf vectorstore/db_faiss/*
   ```
3. Restart the application - it will automatically rebuild the vector store

## 🧪 Testing

### Manual Testing

1. Start the application
2. Navigate to the web interface
3. Test various medical questions:
   - "What is diabetes?"
   - "Explain the symptoms of hypertension"
   - "What are the treatment options for asthma?"

### Expected Behavior

- Vector store loads on startup (if exists)
- Queries return relevant medical information
- Answers are concise (2-3 lines)
- Session maintains conversation history
- Clear button resets conversation

## 📝 Logging

Application logs are stored in the `logs/` directory with daily rotation:
- Format: `log_YYYY-MM-DD.log`
- Includes info, warning, and error messages
- Helps debug issues during development and production

## 🔧 Troubleshooting

### Common Issues

1. **Vector Store Not Found**
   - Ensure PDFs are in `data/` directory
   - Run `python -m app.rag_system.data_loader` to initialize

2. **API Key Errors**
   - Verify `.env` file exists and contains valid keys
   - Check environment variables are loaded correctly

3. **Import Errors**
   - Ensure virtual environment is activated
   - Run `pip install -e .` to install package in development mode

4. **Port Already in Use**
   - Change port in `application.py` or use: `flask run --port=8001`

## 🚢 Deployment

For deployment instructions, CI/CD pipeline setup, Docker configuration, and AWS deployment, see the [Deployment Guide](wiki.md).

The deployment guide covers:
- Jenkins CI/CD setup
- Docker containerization
- Security scanning with Trivy
- AWS ECR integration
- AWS App Runner deployment

## 📦 Dependencies

### Core Dependencies

- **Flask**: Web framework
- **LangChain**: RAG pipeline orchestration
- **FAISS**: Vector similarity search
- **Groq**: LLM API provider
- **HuggingFace**: Embeddings and model hosting
- **PyPDF**: PDF document processing
- **Sentence Transformers**: Embedding models

See `requirements.txt` or `pyproject.toml` for complete dependency list.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

[Add your license information here]

## 🙏 Acknowledgments

- Medical PDF data source: The Gale Encyclopedia of Medicine
- Built with LangChain, Groq, and HuggingFace technologies

---

**Note**: This application is for educational and research purposes. Medical information provided should not replace professional medical advice, diagnosis, or treatment.

