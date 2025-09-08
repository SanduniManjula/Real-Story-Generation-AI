from collections import Counter

import regex as re
import textstat


def distinct_n(text: str, n: int) -> float:
    tokens = text.split()
    if len(tokens) < n:
        return 0.0
    ngrams = [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]
    return len(set(ngrams)) / max(1, len(ngrams))


def repetition_rate(text: str) -> float:
    tokens = [t.lower() for t in re.findall(r"\w+", text)]
    counts = Counter(tokens)
    if not tokens:
        return 0.0
    most = max(counts.values())
    return most / len(tokens)


def readability(text: str) -> float:
    # Flesch Reading Ease (higher is easier)
    try:
        return textstat.flesch_reading_ease(text)
    except Exception:
        return 0.0
