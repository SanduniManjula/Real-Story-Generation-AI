import os
import gdown
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import re

app = FastAPI()

# Google Drive folder link
DRIVE_URL = "https://drive.google.com/drive/folders/1qsiiHUM2g6JjrFX9uN7v3jVEkoJGtcIu"
MODEL_DIR = "./models/gpt2-fairytales3"

# Download if not exists
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR, exist_ok=True)
    # use --folder to download everything
    gdown.download_folder(DRIVE_URL, output=MODEL_DIR, quiet=False, use_cookies=False)

# Load model
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForCausalLM.from_pretrained(MODEL_DIR)


class StoryRequest(BaseModel):
    prompt: str


@app.post("/generate", response_class=PlainTextResponse)
async def generate(request: StoryRequest):
    inputs = tokenizer(request.prompt, return_tensors="pt")
    print("Generating story...")
    outputs = model.generate(
        **inputs,
        max_length=300,
        do_sample=True,
        temperature=0.9,
        top_k=50,
        top_p=0.9,
        repetition_penalty=1.2,
        num_return_sequences=1,
    )

    story = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    story = re.split(r"<\|endofstory\|>.*$", story)[0].strip()
    story = story.replace("\n", " ").replace("\r", " ").strip()

    return story
