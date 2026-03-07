from fastapi import FastAPI
from api.generate import router

app = FastAPI(title="AI Shorts Generator")

app.include_router(router)