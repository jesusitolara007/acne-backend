from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import base64
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_acne(file: UploadFile = File(...)):
    image_bytes = await file.read()
    b64 = base64.b64encode(image_bytes).decode()

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"Eres un asistente dermatológico. Identifica el tipo de acné de forma orientativa."},
            {"role":"user","content":[
                {"type":"text","text":"¿Qué tipo de acné se observa?"},
                {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}
            ]}
        ]
    )

    return {"result": response.choices[0].message.content}
