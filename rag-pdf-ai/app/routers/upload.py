from fastapi import APIRouter
from fastapi import UploadFile, File, HTTPException
import os
import logging
# pyright: reportOptionalMemberAccess=false
# type: ignore



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


router = APIRouter()

@router.post("/upload")

async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'): #IGNORE VSC IS ON DRUGS
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    UPLOAD_DIR = "uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)# type: ignore _IGNORE VSC IS ON DRUGS 
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
