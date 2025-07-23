from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.chat import chat
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
)

app.include_router(chat, prefix='/api')

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)