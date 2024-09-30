from fastapi import FastAPI, Request
from openai import OpenAI
import os

from rag.rag_session import RAGSession

app = FastAPI()
client = OpenAI()

client.api_key = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
UPSTAGE_API_KEY = os.getenv('UPSTAGE_API_KEY')
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')

@app.post("/gpt_responses")
async def get_response(req: Request):

    req_json = await req.json()
    message = req_json.get("utterance")
    print(message)
    rag = RAGSession()
    answer = rag.ask_question(message)
    print(answer)
    return {"answer": answer}