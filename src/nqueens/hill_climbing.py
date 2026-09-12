"""Steepest-descent hill climbing for N-Queens."""

from __future__ import annotations

from dataclasses import dataclass
import random
from time import perf_counter

from .board import conflict_count, validate_n


@dataclass(frozen=True)
class HillClimbingResult:
    n: int
    success: bool
    rows: tuple[int, ...]
    steps: int
    initial_conflicts: int
    final_conflicts: int
    restarts: int
    elapsed_seconds: float


def _best_neighbor(rows: tuple[int, ...], rng: random.Random) -> tuple[tuple[int, ...], int]:
    current_score = conflict_count(rows)
    best_score = current_score
    candidates: list[tuple[int, ...]] = []

    for column in range(len(rows)):
        for row in range(len(rows)):
            if row == rows[column]:
                continue
            neighbor = list(rows)
            neighbor[column] = row
            candidate = tuple(neighbor)
            score = conflict_count(candidate)
            if score < best_score:
                best_score = score
                candidates = [candidate]
            elif score == best_score and score < current_score:
                candidates.append(candidate)

    if not candidates:
        return rows, current_score
    return rng.choice(candidates), best_score


def solve_hill_climbing(
    n: int = 8,
    *,
    seed: int | None = None,
    max_steps: int = 1_000,
    max_restarts: int = 0,
) -> HillClimbingResult:
    """Solve N-Queens with steepest-descent hill climbing.

    The basic algorithm can become trapped in a local minimum. Optional random
    restarts make that limitation explicit while improving practical success.
    """
    validate_n(n)
    if max_steps < 1:
        raise ValueError("max_steps must be at least 1")
    if max_restarts < 0:
        raise ValueError("max_restarts cannot be negative")

    started = perf_counter()
    rng = random.Random(seed)
    total_steps = 0
    first_initial = 0
    last_rows: tuple[int, ...] = ()
    last_score = 0

    for restart in range(max_restarts + 1):
        rows = tuple(rng.randrange(n) for _ in range(n))
        score = conflict_count(rows)
        if restart == 0:
            first_initial = score

        for _ in range(max_steps):
            if score == 0:
                return HillClimbingResult(
                    n=n,
                    success=True,
                    rows=rows,
                    steps=total_steps,
                    initial_conflicts=first_initial,
                    final_conflicts=0,
                    restarts=restart,
                    elapsed_seconds=perf_counter() - started,
                )

            neighbor, neighbor_score = _best_neighbor(rows, rng)
            if neighbor_score >= score:
                break
            rows, score = neighbor, neighbor_score
            total_steps += 1

        last_rows, last_score = rows, score

    return HillClimbingResult(
        n=n,
        success=last_score == 0,
        rows=last_rows,
        steps=total_steps,
        initial_conflicts=first_initial,
        final_conflicts=last_score,
        restarts=max_restarts,
        elapsed_seconds=perf_counter() - started,
    )
