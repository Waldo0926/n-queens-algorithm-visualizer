"""Board utilities shared by all N-Queens algorithms."""

from __future__ import annotations


def validate_n(n: int) -> None:
    if n < 1:
        raise ValueError("n must be at least 1")


def conflict_count(rows: tuple[int, ...] | list[int]) -> int:
    """Return the number of attacking queen pairs.

    ``rows[column]`` stores the row occupied by the queen in that column.
    """
    conflicts = 0
    for left in range(len(rows)):
        for right in range(left + 1, len(rows)):
            same_row = rows[left] == rows[right]
            same_diagonal = abs(rows[left] - rows[right]) == right - left
            if same_row or same_diagonal:
                conflicts += 1
    return conflicts


def is_solution(rows: tuple[int, ...] | list[int]) -> bool:
    return len(rows) > 0 and conflict_count(rows) == 0


def board_to_ascii(rows: tuple[int, ...] | list[int]) -> str:
    """Render a board as portable terminal text."""
    n = len(rows)
    lines: list[str] = []
    border = "+" + "---+" * n
    for row in range(n):
        lines.append(border)
        cells = [" Q " if rows[col] == row else "   " for col in range(n)]
        lines.append("|" + "|".join(cells) + "|")
    lines.append(border)
    return "\n".join(lines)
