from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.file_upload import upload
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
)

app.include_router(upload, prefix='/api')

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)