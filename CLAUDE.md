# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

CodePath AI 110 Module 1 lab: "Game Glitch Investigator." A Streamlit number-guessing game that ships **intentionally broken** so the student can practice debugging AI-generated code. The student's job is to (1) find the bugs, (2) fix them in `app.py`, (3) refactor the pure logic functions into `logic_utils.py` so the `pytest` suite passes.

Do not "clean up" the starter bugs unsolicited — they are the assignment. If the user asks for help, prefer Socratic hints over patches unless they ask for the fix directly.

## Commands

```bash
pip install -r requirements.txt          # install deps (streamlit, altair<5, pytest)
python -m streamlit run app.py           # run the game locally
pytest                                   # run the full test suite
pytest tests/test_game_logic.py::test_winning_guess   # run a single test
```

A `.venv/` is already present in the repo; activate it with `source .venv/bin/activate` if you want to use it.

## Architecture

Two-file design with a deliberate seam between UI and logic:

- **`app.py`** — Streamlit page. Currently holds *both* the UI (sidebar, buttons, `st.session_state`) *and* the four pure functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`). The refactor goal is to move those four functions into `logic_utils.py` and import them here.
- **`logic_utils.py`** — Stub module. Each of the four functions raises `NotImplementedError` until the student moves the real implementation over. Signatures defined here are the contract the tests rely on.
- **`tests/test_game_logic.py`** — Imports from `logic_utils` (not `app`). Currently expects `check_guess(guess, secret)` to return a bare string (`"Win"` / `"Too High"` / `"Too Low"`), but the implementation in `app.py` returns a `(outcome, message)` tuple. Reconciling this contract is part of the assignment.

### State model (Streamlit reruns)

Every widget interaction reruns `app.py` top-to-bottom. Persistent values live in `st.session_state` (`secret`, `attempts`, `score`, `status`, `history`) and are initialized with `if "x" not in st.session_state` guards. Bugs in this lab tend to cluster around: keys that get re-randomized on rerun, the "New Game" handler not resetting every key it should, and the difficulty selector not flowing through to dependent UI strings.

## Coursework artifacts

`reflection.md` and `ai_interactions.md` are templates the student fills in as part of the submission. They are not code — do not refactor or auto-complete them. Edit only when the user explicitly asks.
