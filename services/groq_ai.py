import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_scenes(prompt):

    system_prompt = f"""
Create 3 cinematic scenes for a short video.

Return JSON:

{{
 "scenes":[
   {{"visual":"", "text":""}}
 ]
}}

Topic: {prompt}
"""

    res = client.chat.completions.create(

        model="llama3-70b-8192",

        messages=[{"role":"user","content":system_prompt}]
    )

    text = res.choices[0].message.content

    data = json.loads(text)

    return data["scenes"]