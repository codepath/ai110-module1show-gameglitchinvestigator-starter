# Prompt History

## Session: 2026-03-15

---

### 1. Diagnosing run issues
**User:** Could you let me know where I am having issues based on this terminal history. Right now im trying to get the project to run.

**Claude:** Noted that no terminal history was pasted. Inspected the project structure and found dependencies (streamlit, altair, pytest) already installed in `.venv`. Provided the correct run commands.

---

### 2. python3 note + running the app
**User:** One issue you might find is it should be python3 not python but go ahead and run it.

**Claude:** Ran `python3 -m streamlit run app.py` with the venv activated. App started successfully at http://localhost:8501.

---

### 3. Codebase explanation
**User:** Could you read logic_utils.py as well as app.py and offer me an explanation of what units of code are meant to do.

**Claude:** Explained each function in both files:
- `get_range_for_difficulty` — maps difficulty to a number range (noted Hard range 1–50 is easier than Normal 1–100, a bug)
- `parse_guess` — converts raw text input to int, handles decimals and invalid input
- `check_guess` — compares guess to secret, returns outcome and message
- `update_score` — adjusts score based on outcome and attempt number
- Streamlit UI sections: sidebar, session state init, debug expander, input/buttons, new game handler, submit handler
- `logic_utils.py` — all 4 functions are stubs raising `NotImplementedError`

---

### 4. #codebase
**User:** #codebase

**Claude:** Read remaining unread files (`tests/test_game_logic.py`, `reflection.md`). Summarized full codebase:
- `app.py` — Streamlit UI + game logic
- `logic_utils.py` — stubs, all raise `NotImplementedError`
- `tests/test_game_logic.py` — 3 pytest tests for `check_guess`, expect just the outcome string (not a tuple)
- `requirements.txt` — streamlit, altair, pytest
- `reflection.md` — partially filled in, sections 2–5 still blank
- Noted mismatch: tests expect `check_guess` to return a string, but `app.py` returns a tuple

---

### 5. Bug explanations
**User:** From your view of the code base I was able to get a set of unseen bugs and an explanation to why they were not working — explained these bugs found during testing.

**Claude:** Explained each bug with the specific code responsible:

1. **Invalid inputs counted against attempts** — `attempts` increments at `app.py:148` before input is validated
2. **Can't get a perfect score** — `app.py:52`: `points = 100 - 10 * (attempt_number + 1)` penalizes even the first guess
3. **Score can go negative / deductions on correct answers** — no `max(0, ...)` floor on score; deductions apply without a cap
4. **Decimals accepted as winning values** — `app.py:22-23`: `int(float("50.0"))` resolves to `50`, matching the secret
5. **Can't refresh to start a new game** — `st.stop()` at `app.py:145` locks the UI; session state persists across browser refresh
6. **Previous game history persists** — New Game handler never resets `st.session_state.history`
7. **Difficulty change keeps old state** — session state only initializes `if "secret" not in st.session_state`; changing difficulty doesn't reset the game
8. **Contradictory hints** — `app.py:158-163`: on even attempts, secret is cast to string, breaking numeric comparison and flipping hint direction

---
