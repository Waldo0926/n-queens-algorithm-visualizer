# Algorithm analysis

This project solves the same constraint-satisfaction problem with three different search strategies. The comparison is useful because the algorithms make very different trade-offs between completeness, memory, determinism, and practical speed.

## Problem representation

A board is represented as a tuple where `rows[column] = row`. There is exactly one queen in every column, so a candidate board has `N^N` possible row assignments before constraints are applied.

Two queens attack each other when they share a row or when the absolute row difference equals the column difference.

## 1. Backtracking

Backtracking constructs a solution one column at a time. Before a queen is placed, the implementation checks three sets: occupied rows, `row - column` diagonals, and `row + column` diagonals. Invalid partial boards are rejected immediately.

- Complete: yes.
- Deterministic: yes.
- Worst case: exponential.
- Strength: pruning happens during construction, so most invalid complete boards are never generated.

The `find_all=True` mode returns all solutions. For `N=8`, there are 92 distinct solutions when rotations/reflections are counted separately.

## 2. Pruned state-space enumeration

This implementation preserves the distinctive idea from the original course project. Every board is treated as an `N`-digit base-`N` number. A naive enumerator would inspect every one of the `N^N` boards.

Instead, the algorithm finds the first conflicting column `c`. Every board sharing the same invalid prefix through column `c` is also invalid, so the state counter jumps by:

```text
N ** (N - c - 1)
```

This makes the pruning behavior explicit and easy to visualize or benchmark.

- Complete: yes.
- Deterministic: yes.
- Worst case: still exponential.
- Strength: demonstrates how information about an invalid prefix can skip a contiguous region of the encoded search space.

## 3. Hill climbing

Hill climbing starts from a random board and repeatedly moves one queen to a neighboring state with fewer attacking pairs. It is a local-search method rather than an exhaustive search method.

- Complete: no.
- Deterministic: no (unless a random seed is fixed).
- Can fail: yes, at local minima.
- Strength: small memory footprint and often fast progress toward a solution.

The implementation supports random restarts. This is intentionally exposed as a parameter rather than hiding hill climbing's failure mode.

## What to measure

Runtime alone is not a fair comparison because each method performs different work. The benchmark therefore records a method-specific work metric:

- Backtracking: attempted placements.
- State-space search: encoded board states examined.
- Hill climbing: accepted improving moves and empirical success rate.

Run:

```bash
python benchmarks/benchmark.py --n 4 5 6 7 8 9 --hill-trials 100
```

The script writes `benchmark_results.csv`, which is ignored by Git so each machine can generate its own measurements.
