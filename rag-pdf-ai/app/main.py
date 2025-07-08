from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import summarize
from app.routers import upload  
from app.routers import chat




## SET THE APP

app = FastAPI()

## SET  CORS -->> IT ALLOWS THE FRONTEND TO ACCESS THE BACKEND FROM ANYWHERE

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

## IMPORT ROUTERS

app.include_router(summarize.router)
app.include_router(upload.router)
app.include_router(chat.router)


@app.get("/")
def root():
    return {"message": "PDF-AI Backend is Alive 🧠"}
