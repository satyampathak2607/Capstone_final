from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os, json

class ChatRequest(BaseModel):
    question: str

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_best_chunk(question, chunks):
    question_embed = model.encode([question])
    summaries = [c["summary"] for c in chunks]
    summary_embeds = model.encode(summaries)

    sims = cosine_similarity(question_embed, summary_embeds)[0]
    best_idx = np.argmax(sims)
    return summaries[best_idx]

router = APIRouter()

@router.post("/chat")
async def chat(req: ChatRequest):
    path = "summaries/latest.json"
    
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="No summaries available. Run /summarize first.")

    try:
        with open(path, "r", encoding="utf-8") as f:
            chunks = json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read summary file: {e}")

    answer = get_best_chunk(req.question, chunks)
    return {"answer": answer}
