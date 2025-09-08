import argparse
import json

from src.metrics import distinct_n, readability, repetition_rate


def evaluate_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return {
        "distinct-1": round(distinct_n(text, 1), 4),
        "distinct-2": round(distinct_n(text, 2), 4),
        "repetition_rate": round(repetition_rate(text), 4),
        "readability_flesch": round(readability(text), 2),
        "chars": len(text),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--path", required=True, help="Path to generated story .txt"
    )
    args = ap.parse_args()
    print(json.dumps(evaluate_file(args.path), indent=2))
