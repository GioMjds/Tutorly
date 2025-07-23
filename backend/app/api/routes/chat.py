from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

load_dotenv()

chat = APIRouter()

@chat.get('/chat')
async def root():
    return JSONResponse(
        content={"message": "Sana ako nalang lods"},
        status_code=200
    )