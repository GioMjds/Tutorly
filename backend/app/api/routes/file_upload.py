from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.model.file_parser import FileParser
from app.model.ai_chain import TutorlyAI
from dotenv import load_dotenv
import os, io

load_dotenv()

upload = APIRouter()

@upload.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text = FileParser.parse(io.BytesIO(contents), file.filename)
        if not text.strip():
            raise ValueError("The file is empty or could not be parsed.")
        ai = TutorlyAI()
        key_points = ai.get_key_points(text)
        
        return JSONResponse(
            content={"key_points": key_points}, 
            status_code=200
        )
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)