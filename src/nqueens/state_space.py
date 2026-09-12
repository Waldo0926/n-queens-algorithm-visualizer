"""Pruned state-space enumeration inspired by the original course project."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from .board import validate_n


@dataclass(frozen=True)
class StateSpaceResult:
    n: int
    solutions: tuple[tuple[int, ...], ...]
    states_examined: int
    states_skipped: int
    total_state_space: int
    elapsed_seconds: float

    @property
    def first_solution(self) -> tuple[int, ...] | None:
        return self.solutions[0] if self.solutions else None


def _first_conflict(rows: tuple[int, ...]) -> int | None:
    """Return the first column that conflicts with an earlier queen."""
    for column in range(1, len(rows)):
        for earlier in range(column):
            same_row = rows[earlier] == rows[column]
            same_diagonal = abs(rows[earlier] - rows[column]) == column - earlier
            if same_row or same_diagonal:
                return column
    return None


def _decode_state(state: int, n: int) -> tuple[int, ...]:
    """Decode ``state`` as an n-digit base-n board representation."""
    digits = [0] * n
    value = state
    for index in range(n - 1, -1, -1):
        digits[index] = value % n
        value //= n
    return tuple(digits)


def solve_state_space(n: int = 8, *, find_all: bool = False) -> StateSpaceResult:
    """Enumerate N^N boards while pruning invalid prefixes.

    If the first conflict occurs at column ``c``, every state sharing the same
    prefix through that column is invalid. The state counter therefore jumps by
    ``n ** (n - c - 1)`` instead of incrementing by one.
    """
    validate_n(n)
    started = perf_counter()
    total = n**n
    state = 0
    examined = 0
    skipped = 0
    solutions: list[tuple[int, ...]] = []

    while state < total:
        rows = _decode_state(state, n)
        examined += 1
        conflict_column = _first_conflict(rows)

        if conflict_column is None:
            solutions.append(rows)
            state += 1
            if not find_all:
                break
            continue

        jump = n ** (n - conflict_column - 1)
        next_state = min(total, state + jump)
        skipped += max(0, next_state - state - 1)
        state = next_state

    return StateSpaceResult(
        n=n,
        solutions=tuple(solutions),
        states_examined=examined,
        states_skipped=skipped,
        total_state_space=total,
        elapsed_seconds=perf_counter() - started,
    )
