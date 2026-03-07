from fastapi import APIRouter
from pydantic import BaseModel
from services.groq_ai import generate_scenes
from services.pexels import search_video

router = APIRouter()

class Prompt(BaseModel):
    message: str


@router.post("/generate")

def generate(data: Prompt):

    scenes = generate_scenes(data.message)

    clips = []

    for scene in scenes:

        video = search_video(scene["visual"])

        clips.append(video)

    return {
        "scenes": scenes,
        "clips": clips
    }