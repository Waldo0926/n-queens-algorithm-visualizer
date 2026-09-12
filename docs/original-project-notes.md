# Refactoring notes

This repository is a cleaned and re-engineered version of an earlier university **Algorithm Design and Analysis** course project.

The original work explored the Eight Queens problem using:

1. recursive backtracking,
2. state enumeration with prefix-based pruning, and
3. hill climbing with empirical success/failure testing.

For the public GitHub version, the code was reorganized into reusable modules, machine-specific absolute paths were removed, the Windows-only Pygame/Tk embedding code was replaced with a portable Tkinter interface, and automated tests plus a benchmark script were added.

The purpose of this refactor is to preserve the original algorithmic ideas while presenting them as a maintainable, reproducible software project rather than as a raw course-submission archive.
