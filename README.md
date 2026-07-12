# Enterprise RAG Assistant
> Secure, role-based Retrieval-Augmented Generation (RAG) assistant built with FastAPI, ChromaDB, LangChain, and Groq.
> 
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Table of Contents**

- Project Overview
- Features
- Live Demo
- System Architecture
- Tech Stack
- Project Structure
- Getting Started
- API Endpoints
- Authentication Flow
- RAG Workflow
- Testing
- Future Improvements
- Screenshots
- Learning Outcomes

**Project Overview**

An enterprise-grade Retrieval-Augmented Generation (RAG) assistant built using FastAPI, LangChain, ChromaDB, Groq, and SQLAlchemy.

The application enables secure, role-based document retrieval using JWT authentication and Retrieval-Augmented Generation (RAG). Users receive responses generated from department-specific knowledge bases while Role-Based Access Control (RBAC) ensures they can only access authorized documents.

The project follows a modular backend architecture with REST APIs, SQLite for user management, ChromaDB for vector storage, Docker support, and automated API testing using Pytest.

**Features**

- JWT Authentication & Authorization
- Role-Based Access Control (RBAC)
- Retrieval-Augmented Generation (RAG)
- Semantic Search using ChromaDB
- Groq LLM Integration
- LangChain Prompt Pipeline
- SQLite with SQLAlchemy ORM
- Streamlit Chat Interface
- Dockerized Deployment
- Automated API Testing using Pytest

**Live Demo**

| Service | Link |
|----------|------|
| Frontend | Coming Soon |
| Backend API | Coming Soon |

**System Architecture**
<p align="center">
  <img src="assets/architecture.png" alt="System Architecture" width="350">
</p>
The application follows a modular client-server architecture where Streamlit communicates with FastAPI through REST APIs. The backend authenticates users using JWT, retrieves relevant document chunks from ChromaDB, constructs a Retrieval-Augmented Generation (RAG) prompt, and sends it to the Groq LLM for response generation.

**Tech Stack**

| Category | Technologies |
|----------|--------------|
| Backend | FastAPI |
| Language | Python |
| Database | SQLite |
| ORM | SQLAlchemy |
| Authentication | JWT, OAuth2 |
| Vector Database | ChromaDB |
| LLM | Groq API |
| RAG Framework | LangChain |
| Embeddings | Sentence Transformers |
| Testing | Pytest |
| Containerization | Docker, Docker Compose |

**Project Structure**

```text
enterprise-rag-assistant/
│
├── app/
│   ├── api/            # Authentication & Chat endpoints
│   ├── core/           # Config, Database & Security
│   ├── crud/           # Database CRUD operations
│   ├── models/         # SQLAlchemy models
│   ├── rag/            # Retrieval, Prompt & LLM Pipeline
│   └── schemas/        # Request & Response models
│
├── frontend/           # Streamlit UI
├── resources/          # Knowledge base documents
├── tests/              # Automated API tests
├── assets/             # Images used in README
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

**Getting Started**

    **Prerequisites**
    - Python 3.11+
     - Groq API or Ollama(for local)
     - Git
     - Docker (Optional)
    **Installation**
    Clone the repository

     ```bash
     git clone <repository-url>
     cd enterprise-rag-assistant
     ```

     Create a virtual environment

     ```bash
     python -m venv .venv
     ```

     Activate it

     Windows

     ```bash
     .venv\Scripts\activate
     ```

     Linux / macOS

     ```bash
     source .venv/bin/activate
     ```

     Install dependencies

     ```bash
     pip install -r requirements.txt
     ```

     Configure environment variables

     ```bash
     cp .env.example .env
     ```
     ```bash
     GROQ_API_KEY=your_api_key
     GROQ_MODEL=llama-3.3-70b-versatile
     ```
     
     ```
   **Docker Setup**
     Build the Docker image

     ```bash
     docker build -t enterprise-rag .
     ```

     Run the container

     ```bash
     docker run -p 8000:8000 --env-file .env enterprise-rag
     ```

     Or using Docker Compose

     ```bash
     docker compose up --build
     ```

**API Endpoints**

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Authenticate user and return JWT |
| POST | `/chat` | Query the RAG assistant |
| GET | `/test` | Verify JWT authentication |

**Authentication Flow**

1. Register a new account.
2. Login using valid credentials.
3. FastAPI validates the user.
4. JWT Access Token is generated.
5. Token is stored in Streamlit session state.
6. Protected endpoints validate the JWT before processing requests.

**RAG Workflow**

```text
User Question
      │
      ▼
JWT Authentication
      │
      ▼
Role-Based Access Control
      │
      ▼
Semantic Search (ChromaDB)
      │
      ▼
Retrieve Relevant Documents
      │
      ▼
Prompt Construction
      │
      ▼
Groq LLM
      │
      ▼
AI Response
```

**Testing**

Automated API tests are written using **Pytest** and **FastAPI TestClient**.

Current test coverage includes:

- User Registration
- Login Authentication
- JWT Validation
- Protected Endpoints
- Chat API

**Future Improvements**
- PostgreSQL support
- Redis caching
- Conversation history
- Streaming LLM responses
- Admin dashboard
- CI/CD with GitHub Actions

**Screenshots**

### Swagger UI

<p align="center">
<img src="assets/swagger.png" width="900">
</p>

---

### Chat Interface

<p align="center">
<img src="assets/streamlit.png" width="900">
</p>

**Note:** This project currently runs locally using Ollama for privacy and offline inference. A cloud deployment can be achieved by replacing the local LLM with a hosted inference provider such as OpenAI or Groq.

**Key Learning Outcomes**

This project helped me gain practical experience with:

- FastAPI backend development
- REST API design
- JWT Authentication & Authorization
- SQLAlchemy ORM
- Dependency Injection
- Retrieval-Augmented Generation (RAG)
- ChromaDB vector database
- LangChain
- Groq API integration
- Docker containerization
- Automated API testing

**Author:**
**Poornesh**

Integrated M.Tech Software Engineering  
VIT Vellore

Feel free to connect or contribute to the project.
