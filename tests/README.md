# Tests

Run tests using the local virtual environment from the repo root:

```bash
source .venv/bin/activate
python -m pytest -q
```

`tests/test_refactored.py` is pytest-native and should be run via `pytest`,
not as a standalone script.

Note: `tests/conftest.py` adds the project root to `sys.path`, so running
`pytest` from the repo root works without setting `PYTHONPATH`.

Alternatively, use the project script which will create the venv (if needed),
install test dependencies, and run the suite:

```bash
./run_tests.sh
```

If the venv doesn't exist yet:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest
python -m pytest -q
```
