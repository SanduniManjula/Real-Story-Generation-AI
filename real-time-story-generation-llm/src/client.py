import json
import os
import time
from typing import Dict, Generator, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODE = os.getenv("ENDPOINT_MODE", "INFERENCE_API")
MODEL_ID = os.getenv("HF_MODEL_ID", "tiiuae/falcon-7b-instruct")
ENDPOINT_URL = os.getenv("HF_ENDPOINT_URL")
TIMEOUT = 300


class HFClient:
    def __init__(self):
        if not HF_TOKEN:
            raise ValueError("HF_TOKEN is required")
        self.mode = MODE

    def _payload(self, prompt: str, gen: Dict) -> Dict:
        return {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": gen.get("max_new_tokens", 512),
                "temperature": gen.get("temperature", 0.9),
                "top_p": gen.get("top_p", 0.95),
                "top_k": gen.get("top_k", 50),
                "repetition_penalty": gen.get("repetition_penalty", 1.1),
                "return_full_text": False,
                "do_sample": True,
            },
        }

    def generate_stream(
        self, prompt: str, gen: Optional[Dict] = None
    ) -> Generator[bytes, None, None]:
        gen = gen or {}
        url = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json",
        }
        resp = requests.post(
            url, headers=headers, json=self._payload(prompt, gen), timeout=TIMEOUT
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict) and "error" in data:
            raise RuntimeError(f"Inference API error: {data['error']}")
        text = data[0].get("generated_text", "")
        step = 25
        for i in range(0, len(text), step):
            yield text[i : i + step].encode("utf-8")
            time.sleep(0.02)
