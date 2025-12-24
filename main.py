from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import base64
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_acne(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        b64 = base64.b64encode(image_bytes).decode()

        response = client.responses.create(
    model="gpt-4.1-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "Describe el tipo de acné de forma orientativa."},
            {
                "type": "input_image",
                "image_url": f"data:image/jpeg;base64,{b64}"
            }
        ]
    }]
)



