import requests
from src.metrics import distinct_n, repetition_rate, readability

API_URL = "http://127.0.0.1:8000/generate"

prompts = [
    "A knight sets out to retrieve a phoenix’s feather from the mountains.",
    "A sailor finds an island that appears and disappears at will.",
    "A brave child ventures into the forest to save a trapped unicorn."
]

for prompt in prompts:
    payload = {
        "prompt": prompt,
        "controls": {
            "style": "classic fairytale",
            "pov": "third-person",
            "length": "short",
            "genre": "fantasy",
            "constraints": "avoid explicit content"
        },
        "gen": {
            "temperature": 0.9,
            "top_p": 0.95,
            "top_k": 50,
            "repetition_penalty": 1.1,
            "max_new_tokens": 300
        }
    }

    try:
        print("Payload L : ", payload)
        resp = requests.post(API_URL, json=payload, timeout=300)
        resp.raise_for_status()
        story = resp.text

        print("Prompt: ",prompt)
        print("Generated Story:")
        print(story)
        print("Distinct-1:", distinct_n(story, 1))
        print("Distinct-2:", distinct_n(story, 2))
        print("Repetition rate:", repetition_rate(story))
        print("Readability:", readability(story))
        print("Chars:", len(story))
        print("---")

    except requests.exceptions.RequestException as e:
        print(f"Error generating story for prompt: {prompt}")
        print(e)
