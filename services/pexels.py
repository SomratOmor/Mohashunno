import requests
import os
from dotenv import load_dotenv

load_dotenv()

PEXELS_KEY = os.getenv("PEXELS_API_KEY")


def search_video(query):

    r = requests.get(

        "https://api.pexels.com/videos/search",

        headers={"Authorization":PEXELS_KEY},

        params={
            "query":query,
            "per_page":1
        }
    )

    data = r.json()

    if data["videos"]:

        return data["videos"][0]["video_files"][0]["link"]

    return None