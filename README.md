# deep-research-ai
# AI Agentic Research System

## Overview
This project implements a **multi-agent AI system** that performs **deep research** using web crawling and AI-generated answers. The system consists of:

1. **Research Agent** – Gathers information from the web using Tavily API.
2. **Answer Drafting Agent** – Uses LangChain and OpenAI API to generate responses.
3. **Multi-Agent Orchestration** – Managed via LangGraph.
4. **Vector Storage** – Stores research data in ChromaDB for efficient retrieval.
5. **FastAPI** – Provides an interactive API to query the system.

---

## Features
✅ **Web Scraping** – Uses **Tavily API** to fetch reliable information.  
✅ **AI-Powered Answers** – Utilizes **LangChain** and **GPT-4** for response generation.  
✅ **Vector Database** – Stores research data using **ChromaDB**.  
✅ **Modular & Scalable** – Easily extendable for future enhancements.  
✅ **API-Based System** – Deployable via **FastAPI** with endpoints for queries.  

---

## Setup & Installation
### 1️⃣ Install Dependencies
Ensure you have Python 3.8+ installed. Then run:
```bash
pip install fastapi uvicorn langchain tavily-openai chromadb
```

### 2️⃣ Set API Keys
This project requires **Tavily API** (for web search) and **OpenAI API** (for answer generation). Add them as environment variables:
```bash
export TAVILY_API_KEY="your_tavily_api_key"
export OPENAI_API_KEY="your_openai_api_key"
```

### 3️⃣ Run the Server
Start the FastAPI server using:
```bash
uvicorn ai_agentic_research:app --host 0.0.0.0 --port 8000 --reload
```

---

## Usage
Once the server is running, test it by making a **GET request**:

### API Endpoint:
```
GET /query?research_query=<SEARCH_TERM>&question=<YOUR_QUESTION>
```

### Example:
#### **Using a Browser or cURL**
```
http://127.0.0.1:8000/query?research_query=AI%20trends&question=What%20are%20the%20latest%20AI%20trends?
```
Or:
```bash
curl "http://127.0.0.1:8000/query?research_query=AI%20trends&question=What%20are%20the%20latest%20AI%20trends?"
```

#### **Using Python**:
```python
import requests

url = "http://127.0.0.1:8000/query"
params = {
    "research_query": "AI trends",
    "question": "What are the latest AI trends?"
}
response = requests.get(url, params=params)
print(response.json())
```

---

## Deployment
### **Option 1: Docker**
Create a `Dockerfile` in your project directory:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "ai_agentic_research:app", "--host", "0.0.0.0", "--port", "8000"]
```
Then build and run the container:
```bash
docker build -t ai-research-agent .
docker run -p 8000:8000 ai-research-agent
```

### **Option 2: Deploy on Render / Railway / AWS**
1. Push the project to GitHub.
2. Deploy as a **web service** on **Render** or **Railway**.
3. Add the required environment variables.



