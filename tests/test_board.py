import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nqueens.board import conflict_count, is_solution


class BoardTests(unittest.TestCase):
    def test_known_solution_has_no_conflicts(self):
        solution = (0, 4, 7, 5, 2, 6, 1, 3)
        self.assertEqual(conflict_count(solution), 0)
        self.assertTrue(is_solution(solution))

    def test_conflicting_board_is_detected(self):
        self.assertGreater(conflict_count((0, 0, 2, 3)), 0)


if __name__ == "__main__":
    unittest.main()
