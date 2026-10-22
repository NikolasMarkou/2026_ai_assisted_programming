"""A toy simulation for exercise E19: workers on one shared lock, or one file each.

Usage: python3 exercises/e19/lock_toy.py [--workers N] [--seed N]
Both variants use the same rules; only the place where a result is recorded differs.
A task is WORK ticks of a worker's own work, then RECORD ticks to write the result.
  one shared lock    every result goes into one file. A worker that finds the lock
                     held waits in a queue. One time in FORGET_ONE_IN a worker
                     forgets to release the lock, and it stays held FORGET_TICKS
                     longer.
  one file each      every worker records into its own file. Nobody waits.
The numbers it prints are counted by the loop below from these rules and the seed.
They are not typed in, and they are not data from any real system. The rules are ours:
change a number at the top and run again to see what moves. With --workers 1 the two
variants give the same count, because nobody is there to wait for.
Interface for other code: simulate(workers, ticks, wait, seed) runs the lock variant
and returns (tasks finished, ticks spent waiting); owned(workers, ticks) runs the
other variant and returns the tasks finished. A task counts when its record is
complete by the last tick. Standard library only; the output is the same on every
run for the same options.
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import random  # noqa: E402

BANNER = "SCRIPTED DEMONSTRATION by the course authors, not a measurement"
TOY = "TOY SIMULATION, our own rules, not Cursor's data"
WORKERS, TICKS, SEED = 20, 1000, 7
WORK, RECORD = 10, 2
FORGET_ONE_IN, FORGET_TICKS = 10, 8
WAIT = True


def simulate(workers, ticks, wait, seed):
    """The lock variant. Returns (tasks finished, worker-ticks spent waiting)."""
    rng = random.Random(seed)
    ready = [WORK] * workers  # the tick at which worker i asks for the lock
    queue, free_at, finished, waiting = [], 0, 0, 0
    for tick in range(ticks):
        queue += [i for i in range(workers) if ready[i] == tick]
        while queue and (tick >= free_at or not wait):
            worker = queue.pop(0)
            done = tick + RECORD
            finished += int(done <= ticks)
            free_at = done + (FORGET_TICKS if rng.randrange(FORGET_ONE_IN) == 0 else 0)
            ready[worker] = done + WORK
        waiting += len(queue)  # workers still in the queue wait through this tick
    return finished, waiting


def owned(workers, ticks):
    """The variant where each worker owns its file. Returns the tasks finished."""
    finished = 0
    for _ in range(workers):
        done = WORK + RECORD
        while done <= ticks:
            finished += 1
            done += WORK + RECORD
    return finished


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--workers", type=int, default=WORKERS, metavar="N")
    parser.add_argument("--seed", type=int, default=SEED, metavar="N")
    args = parser.parse_args(argv)
    if args.workers < 1:
        parser.error("--workers must be 1 or more")
    locked, waiting = simulate(args.workers, TICKS, WAIT, args.seed)
    own = owned(args.workers, TICKS)
    share = 100 * waiting // (args.workers * TICKS)
    print(BANNER)
    print(TOY)
    print(f"rules: {args.workers} workers, {TICKS} ticks, seed {args.seed}")
    print(f"  one task = {WORK} ticks of the worker's own work, then {RECORD} ticks "
          "to record the result")
    print(f"  shared lock: one file takes every result; a worker waits while it is "
          f"held;\n    one time in {FORGET_ONE_IN} the lock is held {FORGET_TICKS} "
          "ticks longer (the holder forgot to release it)")
    print("  own files: every worker records into its own file and never waits")
    print()
    print("variant         tasks finished   per worker   waiting")
    print(f"shared lock     {locked:>14}   {locked / args.workers:>10.1f}   "
          f"{share:>6}% of worker ticks")
    print(f"own files       {own:>14}   {own / args.workers:>10.1f}   "
          f"{0:>6}% of worker ticks")
    print()
    ratio = f"{own / locked:.1f}" if locked else "no"
    print(f"own files finished {ratio} times the tasks of the shared lock.")
    print("Both numbers come from the rules above. A real lock, real agents and a real")
    print("task differ. The toy shows only that waiting on one lock grows with the")
    print("number of workers who need it, and that separate files take that wait away.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
