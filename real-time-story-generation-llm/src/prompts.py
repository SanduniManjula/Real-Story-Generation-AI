from typing import Dict

SYSTEM_STYLE_GUIDE = """
You are an award-winning storyteller. Write vivid, engaging prose that balances plot momentum with sensory detail. Keep the language accessible.
"""

def build_prompt(user_prompt: str, controls: Dict) -> str:
    style = controls.get("style", "classic fairytale")
    pov = controls.get("pov", "third-person")
    length = controls.get("length", "short")
    genre = controls.get("genre", "fantasy")
    constraints = controls.get("constraints", "avoid explicit content; suitable for all ages")

    guide = f"Style: {style}. POV: {pov}. Length: {length}. Genre: {genre}. Constraints: {constraints}."
    seed = f"Story seed: {user_prompt.strip()}"
    return f"{SYSTEM_STYLE_GUIDE}\n{guide}\n{seed}\nNow write the story."
