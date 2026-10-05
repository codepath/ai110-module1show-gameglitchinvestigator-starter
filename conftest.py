"""Pytest configuration.

The mere presence of this file at the project root puts that root on
``sys.path``, which is what lets ``tests/test_game_logic.py`` do
``from logic_utils import check_guess`` when you run a bare ``pytest tests/``.

Without it, pytest only adds ``tests/`` to the path and the import fails with
``ModuleNotFoundError: No module named 'logic_utils'``.
"""
