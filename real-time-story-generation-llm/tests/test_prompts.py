from src.prompts import build_prompt

seed = "A city where shadows have names."

controls = {
    "style": "noir",
    "pov": "first-person",
    "length": "short",
    "genre": "mystery"
}

result = build_prompt(seed, controls)
print(result)