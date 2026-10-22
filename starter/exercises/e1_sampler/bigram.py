"""Bigram next-word sampler with temperature as a visible knob.

Usage: python3 bigram.py [--word the] [--temperature 1.0] [--seed 7] [--length 12]
       python3 bigram.py --compare      (seeds 1 to 3 at temperature 0.01 and at 1.5)
Counts which word follows which word in corpus.txt, turns the counts of the next
words after --word into probabilities with a softmax over log counts divided by
the temperature, prints the 5 most likely next words as bars, then generates
--length words. The same seed gives the same text. Standard library only.
"""
import argparse
import math
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

CORPUS = Path(__file__).with_name("corpus.txt")


def tokenize(text: str) -> list[str]:
    """Lowercase words, numbers and single punctuation marks."""
    return re.findall(r"[a-z_']+|\d+|[^\sa-z_\d]", text.lower())


def build_counts(tokens: list[str]) -> dict[str, Counter]:
    """Return {word: Counter of the words that follow it}."""
    counts = defaultdict(Counter)
    for current, following in zip(tokens, tokens[1:]):
        counts[current][following] += 1
    return dict(counts)


def next_probs(counts: dict[str, int], temperature: float) -> dict[str, float]:
    """Softmax over log counts divided by the temperature.

    counts: {word: count}. temperature: a number above 0. Returns {word: probability}
    with the probabilities summing to 1. At temperature 1 they equal count / total.
    """
    logits = {word: math.log(count) / temperature for word, count in counts.items()}
    top = max(logits.values())  # subtract the maximum so exp() cannot overflow
    weights = {word: math.exp(value - top) for word, value in logits.items()}
    total = sum(weights.values())
    return {word: weight / total for word, weight in weights.items()}


def generate(model: dict, word: str, temperature: float, seed: int, length: int) -> str:
    """Start at word and append length words, each sampled from next_probs."""
    rng = random.Random(seed)
    words = [word]
    for _ in range(length):
        if word not in model:  # the last word of the corpus has no successor
            break
        probs = next_probs(model[word], temperature)
        word = rng.choices(list(probs), weights=list(probs.values()))[0]
        words.append(word)
    return " ".join(words)


def print_bars(probs: dict[str, float], top: int = 5) -> None:
    """Print the top most likely words; the longest bar is the most likely word."""
    ranked = sorted(probs.items(), key=lambda item: -item[1])[:top]
    for word, p in ranked:
        print(f"  {p:.2f} {'#' * round(30 * p / ranked[0][1]):<30} {word}")


def compare(model: dict, word: str, length: int) -> None:
    """Print seeds 1 to 3 at temperature 0.01 and at 1.5, 6 lines in one run."""
    for temperature in (0.01, 1.5):
        for seed in (1, 2, 3):
            text = generate(model, word, temperature, seed, length)
            print(f"temperature {temperature} seed {seed}: {text}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--word", default="the")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--length", type=int, default=12)
    parser.add_argument("--compare", action="store_true",
                        help="print seeds 1 to 3 at temperature 0.01 and at 1.5")
    args = parser.parse_args(argv)
    model = build_counts(tokenize(CORPUS.read_text()))
    if args.temperature <= 0:
        parser.error("--temperature must be above 0")
    if args.word not in model:
        parser.error(f"'{args.word}' has no successor in corpus.txt")
    if args.compare:
        compare(model, args.word, args.length)
        return
    print(f"word: {args.word}  temperature: {args.temperature}  seed: {args.seed}")
    print("most likely next words:")
    print_bars(next_probs(model[args.word], args.temperature))
    print("generated:", generate(model, args.word, args.temperature, args.seed,
                                 args.length))


if __name__ == "__main__":
    main()

    # Hidden check (not shown)
    model = build_counts(tokenize(CORPUS.read_text()))
    cold = {generate(model, "the", 0.01, seed, 12) for seed in (1, 2, 3)}
    warm = {generate(model, "the", 1.5, seed, 12) for seed in (1, 2, 3)}
    assert len(cold) == 1, cold
    assert len(warm) >= 2, warm
    for temperature in (0.01, 0.5, 1.0, 1.5, 5.0):
        probs = next_probs(model["the"], temperature)
        assert abs(sum(probs.values()) - 1) < 1e-9
    total = sum(model["the"].values())
    assert all(abs(p - model["the"][w] / total) < 1e-9
               for w, p in next_probs(model["the"], 1.0).items())
