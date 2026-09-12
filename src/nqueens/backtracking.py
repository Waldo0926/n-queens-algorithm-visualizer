"""Depth-first backtracking solver for N-Queens."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from .board import validate_n


@dataclass(frozen=True)
class BacktrackingResult:
    n: int
    solutions: tuple[tuple[int, ...], ...]
    nodes_visited: int
    elapsed_seconds: float

    @property
    def first_solution(self) -> tuple[int, ...] | None:
        return self.solutions[0] if self.solutions else None


def solve_backtracking(n: int = 8, *, find_all: bool = False) -> BacktrackingResult:
    """Solve N-Queens using DFS + constraint checking.

    The solver places one queen per column. Sets make row and diagonal
    validation O(1) per attempted placement.
    """
    validate_n(n)
    started = perf_counter()
    rows: list[int] = []
    used_rows: set[int] = set()
    diag_down: set[int] = set()  # row - column
    diag_up: set[int] = set()    # row + column
    solutions: list[tuple[int, ...]] = []
    nodes_visited = 0

    def search(column: int) -> bool:
        nonlocal nodes_visited
        if column == n:
            solutions.append(tuple(rows))
            return not find_all

        for row in range(n):
            nodes_visited += 1
            down = row - column
            up = row + column
            if row in used_rows or down in diag_down or up in diag_up:
                continue

            rows.append(row)
            used_rows.add(row)
            diag_down.add(down)
            diag_up.add(up)

            should_stop = search(column + 1)

            rows.pop()
            used_rows.remove(row)
            diag_down.remove(down)
            diag_up.remove(up)

            if should_stop:
                return True
        return False

    search(0)
    return BacktrackingResult(
        n=n,
        solutions=tuple(solutions),
        nodes_visited=nodes_visited,
        elapsed_seconds=perf_counter() - started,
    )
