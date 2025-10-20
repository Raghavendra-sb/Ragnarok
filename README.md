# 🤖 Async RAG System: Ragnarok (⚡)

This project implements a scalable, **asynchronous RAG** (Retrieval-Augmented Generation) pipeline designed to handle document indexing without blocking the main application. It uses **Redis Queue (RQ)** and **Valkey** to manage the heavy document processing and embedding tasks.

## ✨ Features

* **Asynchronous Processing (RQ):** Offloads computationally intensive tasks (PDF loading, chunking, and embedding) to background workers.
* **Vector Database (Qdrant):** Used for efficient vector storage and fast retrieval.
* **Embeddings & LLM (GoogleGenAI):** Utilizes Gemini embeddings for vector creation.
* **Document Loading:** Employs **PyPDFLoader** and **RecursiveCharacterTextSplitter**.
* **Containerized Setup:** Uses **Docker Compose** to manage the entire backend environment (**Valkey** and **Qdrant**).

***

## ⚙️ Prerequisites

You must have the following installed:

1.  **Docker** and **Docker Compose**
2.  **Python 3.10+**
3.  **A Google Gemini API Key**

***

## 🚀 Installation & Setup

### 1. Configure Environment Variables

Create a file named **`.env`** in your project's root directory (`/workspaces/GenAi`) and add your API key:

```env
# .env file

GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
# Optional: Qdrant and Redis configuration (defaults used if omitted)
# QDRANT_HOST="http://qdrant:6333"
# REDIS_URL="redis://valkey:6379"
 `````
### 2. Launch Backend Services (Valkey & Qdrant)
Start the required services (Valkey/Redis queue broker and Qdrant vector database) using Docker Compose:

```Bash

docker compose up -d
 `````

### 3. Python Dependencies
Navigate to your project folder (rag_queue), set up your Python environment, and install all dependencies (assuming you have a requirements.txt file).

```Bash

cd rag_queue
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd .. # Return to the outer directory for execution
 `````

##  ▶️ Running the System

#### The RAG pipeline requires two separate processes to run in parallel: The Worker and The Server.

### 1. Start the RQ Worker (Indexing/Processing)
The worker is responsible for picking up document processing jobs from the queue and executing them.

Execute from the outer directory (/workspaces/GenAi):

```Bash

sh rag_queue/worker.sh
 `````
💡 Keep this terminal window open. The worker will start printing logs as soon as it picks up jobs from the next step.

### 2. Run the Main Server (Indexing/Inference)
The main server script handles enqueuing jobs (indexing) and the final RAG query/inference logic.

Execute from the outer directory (/workspaces/GenAi):
```Bash

python -m rag_queue.main
 `````
#### When this script runs, it will:
1 . Indexing Phase: Load source documents (e.g., PDF), chunk the data, and push embedding jobs to the Valkey queue.

2 . Worker Response: The worker (running in the other terminal) processes these jobs and inserts the embeddings into Qdrant.

3 . Inference Phase: Once indexing is complete, the script will handle the user interaction or query process.

## 📂 Project Structure
```
/workspaces/GenAi/
├── .env
├── docker-compose.yml
└── rag_queue/
    ├── .venv/
    ├── requirements.txt
    ├── worker.sh                # Starts the RQ Worker process
    ├── main.py                  # Main Server/App logic (Enqueueing and Inference)
    └── worker.py                # Defines the RQ job function (Embedding & Qdrant insertion)
    └── server.py                #setting up the fast api server

```

