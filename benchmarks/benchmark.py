"""Reproducible benchmark for the three implementations."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import statistics
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from nqueens.backtracking import solve_backtracking  # noqa: E402
from nqueens.hill_climbing import solve_hill_climbing  # noqa: E402
from nqueens.state_space import solve_state_space  # noqa: E402


def run(n_values: list[int], hill_trials: int, output: Path) -> None:
    rows: list[dict[str, object]] = []

    for n in n_values:
        backtracking = solve_backtracking(n)
        rows.append({
            "n": n,
            "algorithm": "backtracking",
            "success_rate": 1.0 if backtracking.first_solution else 0.0,
            "work": backtracking.nodes_visited,
            "elapsed_seconds": backtracking.elapsed_seconds,
        })

        state_space = solve_state_space(n)
        rows.append({
            "n": n,
            "algorithm": "pruned_state_space",
            "success_rate": 1.0 if state_space.first_solution else 0.0,
            "work": state_space.states_examined,
            "elapsed_seconds": state_space.elapsed_seconds,
        })

        successes = 0
        durations: list[float] = []
        steps: list[int] = []
        for trial in range(hill_trials):
            result = solve_hill_climbing(n, seed=trial)
            successes += int(result.success)
            durations.append(result.elapsed_seconds)
            steps.append(result.steps)
        rows.append({
            "n": n,
            "algorithm": "hill_climbing",
            "success_rate": successes / hill_trials,
            "work": round(statistics.mean(steps), 2),
            "elapsed_seconds": statistics.mean(durations),
        })

    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("n", "algorithm", "success_rate", "work", "elapsed_seconds"))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} benchmark rows to {output}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", nargs="+", type=int, default=[4, 5, 6, 7, 8, 9])
    parser.add_argument("--hill-trials", type=int, default=100)
    parser.add_argument("--output", type=Path, default=ROOT / "benchmark_results.csv")
    args = parser.parse_args()
    started = time.perf_counter()
    run(args.n, args.hill_trials, args.output)
    print(f"Total benchmark time: {time.perf_counter() - started:.3f}s")


if __name__ == "__main__":
    main()
