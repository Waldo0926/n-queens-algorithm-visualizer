"""Algorithms for solving the N-Queens problem."""

from .backtracking import BacktrackingResult, solve_backtracking
from .hill_climbing import HillClimbingResult, solve_hill_climbing
from .state_space import StateSpaceResult, solve_state_space

__all__ = [
    "BacktrackingResult",
    "HillClimbingResult",
    "StateSpaceResult",
    "solve_backtracking",
    "solve_hill_climbing",
    "solve_state_space",
]
