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
    gdown.download_folder(DRIVE_URL, output=MODEL_DIR, quiet=False, use_cookies=False)

# Load model
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForCausalLM.from_pretrained(MODEL_DIR)


class Controls(BaseModel):
    style: str
    pov: str
    length: str
    genre: str
    constraints: str = "avoid explicit content"


class GenConfig(BaseModel):
    temperature: float = 0.9
    top_p: float = 0.9
    top_k: int = 50
    repetition_penalty: float = 1.1
    max_new_tokens: int = 300


class StoryRequest(BaseModel):
    prompt: str
    controls: Controls
    gen: GenConfig


@app.post("/generate", response_class=PlainTextResponse)
async def generate(request: StoryRequest):
    # Build enriched prompt
    final_prompt = (
        f"Write a {request.controls.length} {request.controls.genre} story "
        f"in {request.controls.style} style, from {request.controls.pov} point of view. "
        f"Constraints: {request.controls.constraints}. "
        f"Story seed: {request.prompt}\n"
    )

    inputs = tokenizer(final_prompt, return_tensors="pt")
    print("Generating story...")

    outputs = model.generate(
        **inputs,
        max_new_tokens=request.gen.max_new_tokens,
        do_sample=True,
        temperature=request.gen.temperature,
        top_k=request.gen.top_k,
        top_p=request.gen.top_p,
        repetition_penalty=request.gen.repetition_penalty,
        num_return_sequences=1,
    )

    story = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    story = re.split(r"<\|endofstory\|>.*$", story)[0].strip()
    story = story.replace("\n", " ").replace("\r", " ").strip()

    return story
