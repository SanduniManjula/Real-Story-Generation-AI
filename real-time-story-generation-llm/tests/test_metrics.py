from src.metrics import distinct_n, readability, repetition_rate


def test_distinct():
    text = "a b c a b c"
    assert 0 <= distinct_n(text, 1) <= 1


def test_repetition():
    text = "hello hello world"
    r = repetition_rate(text)
    assert r >= 2 / 3 - 1e-6


def test_readability():
    text = "This is a simple sentence that is easy to read."
    score = readability(text)
    assert isinstance(score, float)
