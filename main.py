from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Mohashunno API",
    version="1.0",
    description="Simple working FastAPI backend"
)

# CORS (optional but useful for mobile/web apps)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home route
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Mohashunno backend is working"
    }

# Health check
@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# Example API endpoint
@app.get("/hello")
def hello(name: str = "world"):
    return {
        "message": f"Hello {name}"
    }

# Simple chat test endpoint
@app.get("/chat")
def chat(prompt: str):
    return {
        "prompt": prompt,
        "response": f"You said: {prompt}"
    }