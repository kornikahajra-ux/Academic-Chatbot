#from openai import OpenAI
#client = OpenAI(base_url="https://openrouter.ai/api/v1", 
#               api_key = "<OPENROUTER_API_KEY>",)

import os
import base64
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

@app.get("/")
async def read_index():
    return FileResponse('templates/index.html')

@app.post("/chat")
async def chat(message: str = Form(...),history: str = Form(...), file: UploadFile = File(None)):
    messages = json.loads(history)
    content = [{"type": "text", "text": message}]
    if file and file.content_type.startswith('image/'):
        file_bytes = await file.read()
        base64_image = base64.b64encode(file_bytes).decode('utf-8')
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:{file.content_type};base64,{base64_image}"}
        })
    messages.append({"role": "user", "content": content})
    response = client.chat.completions.create(
        model="qwen/qwen-2.5-vl-7b-instruct:free",
        messages=[
            {"role": "system", "content": "Academic Tutor to help analyse notes and diagrams and answer doubts and questions."},
            {"role": "user", "content": content}
        ]
    )
    return {"response": response.choices[0].message.content}




