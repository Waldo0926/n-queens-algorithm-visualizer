"""Command-line interface for the N-Queens project."""

from __future__ import annotations

import argparse

from .backtracking import solve_backtracking
from .board import board_to_ascii
from .hill_climbing import solve_hill_climbing
from .state_space import solve_state_space


def _solve(args: argparse.Namespace) -> int:
    if args.algorithm == "backtracking":
        result = solve_backtracking(args.n, find_all=args.all)
        rows = result.first_solution
        print(f"algorithm: backtracking")
        print(f"n: {args.n}")
        print(f"solutions found: {len(result.solutions)}")
        print(f"placements visited: {result.nodes_visited:,}")
        print(f"elapsed: {result.elapsed_seconds:.6f}s")
    elif args.algorithm == "state-space":
        result = solve_state_space(args.n, find_all=args.all)
        rows = result.first_solution
        print("algorithm: pruned state-space")
        print(f"n: {args.n}")
        print(f"solutions found: {len(result.solutions)}")
        print(f"states examined: {result.states_examined:,}")
        print(f"states skipped: {result.states_skipped:,}")
        print(f"total state space: {result.total_state_space:,}")
        print(f"elapsed: {result.elapsed_seconds:.6f}s")
    else:
        result = solve_hill_climbing(
            args.n,
            seed=args.seed,
            max_steps=args.max_steps,
            max_restarts=args.restarts,
        )
        rows = result.rows if result.success else None
        print("algorithm: hill climbing")
        print(f"n: {args.n}")
        print(f"success: {result.success}")
        print(f"steps: {result.steps}")
        print(f"restarts: {result.restarts}")
        print(f"final conflicts: {result.final_conflicts}")
        print(f"elapsed: {result.elapsed_seconds:.6f}s")

    if rows:
        print("\nsolution rows by column:", rows)
        print(board_to_ascii(rows))
        return 0
    print("\nNo solution found with the selected configuration.")
    return 1


def _compare(args: argparse.Namespace) -> int:
    backtracking = solve_backtracking(args.n)
    state_space = solve_state_space(args.n)
    hill = solve_hill_climbing(args.n, seed=args.seed, max_restarts=args.restarts)

    print(f"N-Queens comparison (N={args.n})")
    print("-" * 76)
    print(f"{'Algorithm':<24} {'Solved':<8} {'Work metric':<24} {'Time (s)':>12}")
    print("-" * 76)
    print(
        f"{'Backtracking':<24} {str(backtracking.first_solution is not None):<8} "
        f"{('placements=' + format(backtracking.nodes_visited, ',')):<24} "
        f"{backtracking.elapsed_seconds:>12.6f}"
    )
    print(
        f"{'Pruned state-space':<24} {str(state_space.first_solution is not None):<8} "
        f"{('states=' + format(state_space.states_examined, ',')):<24} "
        f"{state_space.elapsed_seconds:>12.6f}"
    )
    print(
        f"{'Hill climbing':<24} {str(hill.success):<8} "
        f"{('steps=' + format(hill.steps, ',')):<24} "
        f"{hill.elapsed_seconds:>12.6f}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare N-Queens search algorithms.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    solve_parser = subparsers.add_parser("solve", help="solve one N-Queens instance")
    solve_parser.add_argument("--algorithm", choices=("backtracking", "state-space", "hill-climbing"), default="backtracking")
    solve_parser.add_argument("--n", type=int, default=8)
    solve_parser.add_argument("--all", action="store_true", help="enumerate all solutions where supported")
    solve_parser.add_argument("--seed", type=int, default=None)
    solve_parser.add_argument("--max-steps", type=int, default=1_000)
    solve_parser.add_argument("--restarts", type=int, default=100)
    solve_parser.set_defaults(func=_solve)

    compare_parser = subparsers.add_parser("compare", help="compare all three algorithms")
    compare_parser.add_argument("--n", type=int, default=8)
    compare_parser.add_argument("--seed", type=int, default=42)
    compare_parser.add_argument("--restarts", type=int, default=100)
    compare_parser.set_defaults(func=_compare)

    visualize_parser = subparsers.add_parser("visualize", help="launch the Tkinter GUI")
    visualize_parser.set_defaults(func=lambda _args: _launch_visualizer())
    return parser


def _launch_visualizer() -> int:
    from .visualizer import launch

    launch()
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
