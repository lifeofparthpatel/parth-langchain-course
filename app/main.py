from fastapi import FastAPI
from app.api.analyze import router

app = FastAPI(title="ResumeSense")

app.include_router(router)