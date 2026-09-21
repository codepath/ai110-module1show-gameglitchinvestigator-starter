"""Pytest configuration: make the repo root importable from any working directory.

# FIX: the starter layout could not be tested with the command the instructions
# give you. `tests/test_game_logic.py` does `from logic_utils import ...`, but
# `logic_utils.py` sits in the repo root, and pytest only puts the *test* file's
# directory (`tests/`) on sys.path. So plain `pytest` failed at collection with
# `ModuleNotFoundError: No module named 'logic_utils'` -- it only appeared to
# work if you happened to type `python -m pytest` from the repo root, because
# that form adds the current directory to sys.path for you.
#
# A conftest.py at the repo root fixes it: pytest prepends the directory
# containing the rootdir conftest to sys.path, so `pytest`, `pytest tests/`,
# and `python -m pytest` all resolve the import the same way from anywhere.
# The explicit insert below keeps that true even if pytest's import mode is
# changed later.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
