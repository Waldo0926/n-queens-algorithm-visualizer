# Contributing

Small, focused pull requests are welcome.

1. Keep algorithm changes separate from UI-only changes where possible.
2. Add or update tests for behavior changes.
3. Avoid committing generated benchmark CSV files, virtual environments, IDE metadata, or machine-specific paths.
4. Run the test suite before opening a pull request:

```bash
python -m unittest discover -s tests -p "test_*.py"
```
