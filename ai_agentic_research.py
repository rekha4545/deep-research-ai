import os
import json
from fastapi import FastAPI
from langchain.graphs import Graph
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TavilyLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# Set API keys
os.environ["TAVILY_API_KEY"] = "your_tavily_api_key"
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

# Initialize FastAPI
app = FastAPI()

# Initialize LLM
llm = ChatOpenAI(model_name="gpt-4-turbo")

# Create a memory object for agent conversation
memory = ConversationBufferMemory(memory_key="chat_history")

# Load research documents from Tavily API
def fetch_research_data(query):
    loader = TavilyLoader(api_key=os.getenv("TAVILY_API_KEY"))
    documents = loader.load(query=query, max_results=5)
    return documents

# Process and store documents in ChromaDB
def store_documents_in_chroma(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(split_docs, embeddings)
    return vector_store

# Research Agent
class ResearchAgent:
    def __init__(self):
        self.vector_store = None

    def collect_data(self, query):
        docs = fetch_research_data(query)
        self.vector_store = store_documents_in_chroma(docs)
        return "Research data collected and stored."

# Answer Drafting Agent
class AnswerDraftingAgent:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=self.vector_store.as_retriever()
        )

    def generate_answer(self, question):
        return self.qa_chain.run(question)

# LangGraph - Multi-Agent System
class MultiAgentSystem:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.answer_agent = None

    def execute_pipeline(self, query, question):
        self.research_agent.collect_data(query)
        self.answer_agent = AnswerDraftingAgent(self.research_agent.vector_store)
        return self.answer_agent.generate_answer(question)

multi_agent_system = MultiAgentSystem()

@app.get("/query")
def run_agents(research_query: str, question: str):
    response = multi_agent_system.execute_pipeline(research_query, question)
    return {"answer": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
