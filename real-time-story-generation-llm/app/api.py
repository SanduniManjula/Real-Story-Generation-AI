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

FEW_SHOT_EXAMPLES = """
### Instruction: Write a short whimsical story in third-person POV. Story seed: A lonely dragon guards a glowing crystal deep inside a mountain.
### Response: Deep within a misty cavern, a dragon curled around a glowing crystal, humming softly. For centuries, he waited for a friend brave enough to visit. One day, a small child entered the cavern, smiling instead of trembling. The dragon blinked in surprise, and warmth filled the cavern. The crystal’s glow softened, no longer a warning but a welcome. The dragon was lonely no more. The End.

### Instruction: Write a magical fairytale in first-person POV. Story seed: I found an old music box buried in the sand.
### Response: I brushed away the sand, and the music box sang a tune I somehow remembered. The melody drifted across the shore, and the waves glimmered with light. A door of moonlight appeared, inviting me in. I stepped through, humming the melody, and vanished into the song. The End.

### Instruction: Write a short adventure story in mythic style, third-person POV. Story seed: A knight sets out to find the last phoenix.
### Response: The knight rode through forests of ash, following faint traces of flame. At last, in a quiet valley, he found the phoenix—gentle and radiant. It sang a song of rebirth, and the knight lowered his sword. From that day, peace returned to the kingdom. The End.
"""



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
        f"{FEW_SHOT_EXAMPLES}\n"
        f"### Instruction: Write a {request.controls.length} {request.controls.genre} story "
        f"in {request.controls.style} style, from {request.controls.pov} point of view. "
        f"Constraints: {request.controls.constraints}. "
        f"Story seed: {request.prompt}\n### Response: "

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
        eos_token_id=tokenizer.encode("The End.")[0],
    )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    continuation = decoded[len(final_prompt):].strip()
    continuation = re.split(r"<\|endofstory\|>.*$", continuation)[0].strip()
    continuation = continuation.replace("\n", " ").replace("\r", " ").strip()

    story = f"{request.prompt}{continuation}"
    return story
