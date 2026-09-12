"""Small cross-platform Tkinter GUI for visualizing N-Queens solutions."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .backtracking import solve_backtracking
from .hill_climbing import solve_hill_climbing
from .state_space import solve_state_space


class NQueensApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("N-Queens Algorithm Visualizer")
        self.root.minsize(720, 620)

        self.n_var = tk.IntVar(value=8)
        self.algorithm_var = tk.StringVar(value="Backtracking")
        self.status_var = tk.StringVar(value="Choose an algorithm and press Solve.")

        controls = ttk.Frame(root, padding=12)
        controls.pack(fill="x")

        ttk.Label(controls, text="N:").pack(side="left")
        ttk.Spinbox(controls, from_=4, to=14, width=5, textvariable=self.n_var).pack(
            side="left", padx=(6, 16)
        )

        ttk.Label(controls, text="Algorithm:").pack(side="left")
        ttk.Combobox(
            controls,
            state="readonly",
            width=22,
            textvariable=self.algorithm_var,
            values=("Backtracking", "Pruned state-space", "Hill climbing"),
        ).pack(side="left", padx=(6, 16))

        ttk.Button(controls, text="Solve", command=self.solve).pack(side="left")

        self.canvas = tk.Canvas(root, width=560, height=560, highlightthickness=0)
        self.canvas.pack(padx=12, pady=6, expand=True)
        ttk.Label(root, textvariable=self.status_var, padding=12).pack(fill="x")

        self.draw_board(tuple())

    def solve(self) -> None:
        n = int(self.n_var.get())
        algorithm = self.algorithm_var.get()

        if algorithm == "Backtracking":
            result = solve_backtracking(n)
            rows = result.first_solution
            status = f"Backtracking: visited {result.nodes_visited:,} placements in {result.elapsed_seconds:.6f}s"
        elif algorithm == "Pruned state-space":
            result = solve_state_space(n)
            rows = result.first_solution
            status = (
                f"State-space: examined {result.states_examined:,} states, "
                f"skipped {result.states_skipped:,} in {result.elapsed_seconds:.6f}s"
            )
        else:
            result = solve_hill_climbing(n, max_restarts=100)
            rows = result.rows if result.success else None
            status = (
                f"Hill climbing: {'solved' if result.success else 'local minimum'}; "
                f"steps={result.steps}, restarts={result.restarts}, "
                f"time={result.elapsed_seconds:.6f}s"
            )

        if rows is None:
            self.status_var.set(status + " — no solution found.")
            self.draw_board(tuple(), n=n)
            return
        self.status_var.set(status)
        self.draw_board(rows)

    def draw_board(self, rows: tuple[int, ...], *, n: int | None = None) -> None:
        self.canvas.delete("all")
        n = n or len(rows) or self.n_var.get()
        width = self.canvas.winfo_width()
        size = 560 if width < 100 else min(560, max(320, width))
        cell = size / n

        for row in range(n):
            for col in range(n):
                x1, y1 = col * cell, row * cell
                x2, y2 = x1 + cell, y1 + cell
                fill = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=fill)

        for col, row in enumerate(rows):
            x = col * cell + cell / 2
            y = row * cell + cell / 2
            self.canvas.create_text(x, y, text="♛", font=("Arial", max(16, int(cell * 0.65))))


def launch() -> None:
    root = tk.Tk()
    NQueensApp(root)
    root.mainloop()
