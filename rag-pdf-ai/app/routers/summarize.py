from fastapi import APIRouter, HTTPException
from app.utils.summarizer import summarize_text
from concurrent.futures import ThreadPoolExecutor
import os
import fitz
import json

router = APIRouter()

UPLOAD_DIR = "uploads"

def get_latest_pdf():
    files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith('.pdf')]
    if not files:
        raise HTTPException(status_code=404, detail="No PDF files found")
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(UPLOAD_DIR, f)))
    return os.path.join(UPLOAD_DIR, latest_file)

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text() # type: ignore
    return text

def chunk_text(text, max_words =700):
    words = text.split()
    return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

def summarize_all_chunks(chunks):
    summaries = []
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(summarize_text, chunks))
    for i, chunk in enumerate(chunks):
        summaries.append({
            "chunk_number": i + 1,
            "original": chunk,
            "summary": results[i]
        })
    return summaries

@router.post("/summarize")
async def summarize_pdf():
    pdf_path = get_latest_pdf()
    raw_text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(raw_text)
    MAX_CHUNKS = 50
    if len(chunks) > MAX_CHUNKS:
            print(f"[!] Limiting chunks to first {MAX_CHUNKS} for performance.")
            chunks = chunks[:MAX_CHUNKS]
    if not chunks:
        raise HTTPException(status_code=400, detail="No text found in the PDF file")
    summarized = summarize_all_chunks(chunks)
    os.makedirs("summaries", exist_ok=True)
    with open("summaries/latest.json", "w", encoding="utf-8") as f:
        json.dump(summarized, f, ensure_ascii=False, indent=4)
    return {
        "message": "Summarization complete",
        "chunks": len(chunks),
        "summaries": summarized
       
    }
