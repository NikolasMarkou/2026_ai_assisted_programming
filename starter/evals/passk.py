"""pass@k and pass^k for one per-run success rate p, from the closed form.

Usage: python3 evals/passk.py [--p 0.8] [--k 5]
Prints one line per k from 1 to --k:
    k=3 pass@k=99.20% pass^k=51.20%
pass@k is the chance that at least 1 of k independent tries passes: 1 - (1 - p)^k.
pass^k is the chance that all k tries pass: p^k. Both are shown in percent with
2 decimals. Standard library only.
"""
import argparse


def pass_at_k(p: float, k: int) -> float:
    """Chance that at least 1 of k independent tries passes.

    p: per-run success rate between 0 and 1. k: number of tries, 1 or more.
    Returns a number between 0 and 1.
    """
    return 1 - (1 - p) ** k


def pass_hat_k(p: float, k: int) -> float:
    """Chance that all k independent tries pass. Same contract as pass_at_k."""
    return p**k


def rate(value: str) -> float:
    """argparse type: a number from 0 to 1."""
    number = float(value)
    if not 0 <= number <= 1:
        raise argparse.ArgumentTypeError("p must be between 0 and 1")
    return number


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--p", type=rate, default=0.8, help="per-run success rate")
    parser.add_argument("--k", type=int, default=5, help="largest number of tries")
    args = parser.parse_args()
    if args.k < 1:
        parser.error("k must be 1 or more")
    for k in range(1, args.k + 1):
        at_least_one = 100 * pass_at_k(args.p, k)
        all_pass = 100 * pass_hat_k(args.p, k)
        print(f"k={k} pass@k={at_least_one:.2f}% pass^k={all_pass:.2f}%")


if __name__ == "__main__":
    main()

# Hidden check (not shown)
assert abs(pass_at_k(0.8, 1) - 0.8) < 1e-9 and abs(pass_hat_k(0.8, 1) - 0.8) < 1e-9
assert abs(pass_at_k(0.8, 3) - 0.992) < 1e-9 and abs(pass_hat_k(0.8, 3) - 0.512) < 1e-9
assert abs(pass_at_k(0.8, 5) - 0.99968) < 1e-9
assert abs(pass_hat_k(0.8, 5) - 0.32768) < 1e-9
