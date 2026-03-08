import os
import requests
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import cloudinary
import cloudinary.uploader

app = FastAPI()

# CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Cloudinary config
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


def search_photos(query):
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 3}

    res = requests.get(url, headers=headers, params=params)
    data = res.json()

    return [p["src"]["large"] for p in data.get("photos", [])]


def search_videos(query):
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 3}

    res = requests.get(url, headers=headers, params=params)
    data = res.json()

    return [v["video_files"][0]["link"] for v in data.get("videos", [])]


@app.get("/")
def home():
    return {"status": "backend running"}


@app.post("/chat")
async def chat(body: dict):

    message = body.get("message")

    completion = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": message}]
    )

    reply = completion.choices[0].message.content

    text = message.lower()

    if "photo" in text or "image" in text or "picture" in text:
        photos = search_photos(message)

        return {
            "type": "photo",
            "reply": reply,
            "media": photos
        }

    if "video" in text:
        videos = search_videos(message)

        return {
            "type": "video",
            "reply": reply,
            "media": videos
        }

    return {
        "type": "text",
        "reply": reply
    }


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):

    result = cloudinary.uploader.upload(file.file)

    return {
        "image_url": result["secure_url"]
    }
