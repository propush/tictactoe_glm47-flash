# Tests

Run tests using the local virtual environment:

```bash
source .venv/bin/activate
python -m pytest -q
```

`tests/test_refactored.py` is now pytest-native and should be run via `pytest`,
not as a standalone script.

If the venv doesn't exist yet:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest
python -m pytest -q
```
