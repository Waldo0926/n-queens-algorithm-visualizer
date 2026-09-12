import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nqueens.backtracking import solve_backtracking
from nqueens.board import is_solution
from nqueens.hill_climbing import solve_hill_climbing
from nqueens.state_space import solve_state_space


class AlgorithmTests(unittest.TestCase):
    def test_backtracking_solves_eight_queens(self):
        result = solve_backtracking(8)
        self.assertIsNotNone(result.first_solution)
        self.assertTrue(is_solution(result.first_solution))

    def test_backtracking_enumerates_92_eight_queen_solutions(self):
        result = solve_backtracking(8, find_all=True)
        self.assertEqual(len(result.solutions), 92)

    def test_state_space_solves_eight_queens_and_prunes(self):
        result = solve_state_space(8)
        self.assertIsNotNone(result.first_solution)
        self.assertTrue(is_solution(result.first_solution))
        self.assertLess(result.states_examined, result.total_state_space)

    def test_hill_climbing_with_restarts_solves_eight_queens(self):
        result = solve_hill_climbing(8, seed=42, max_restarts=100)
        self.assertTrue(result.success)
        self.assertTrue(is_solution(result.rows))


if __name__ == "__main__":
    unittest.main()
