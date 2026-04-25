from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from ingest import ingest_document
from retriever import get_answer  
app = FastAPI()

os.makedirs("./uploads", exist_ok=True)
os.makedirs("./chroma_db", exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class QueryRequest(BaseModel):
    question: str
    doc_id: str

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = f"./uploads/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    doc_id = ingest_document(path)
    return {"doc_id": doc_id, "status": "ingested"}

@app.post("/query")                       
async def query(request: QueryRequest):
    answer, sources = get_answer(request.question, request.doc_id)
    return {"answer": answer, "sources": sources}