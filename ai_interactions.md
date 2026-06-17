# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.
>
> Sections completed below: **Agent Workflow (SF8)** and **Test Generation (SF7)**. Linting (SF9) and Model Comparison (SF11) were not attempted and have been removed.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

"Find the bugs in the AI-generated guessing game, refactor the core logic out of
`app.py` into `logic_utils.py`, fix the bugs, and make the pytest suite pass."

**What did the agent do?**

- Marked each bug location in `app.py` with a `# FIXME` comment and logged them
  in `reflection.md` (commit 1).
- Implemented the four stubbed functions in `logic_utils.py` with docstrings,
  added a `hint_for_outcome` helper, and rewrote `app.py` to import them and fix
  the state bugs (commit 2).
- Expanded `tests/test_game_logic.py` to 15 tests and saved the passing run to
  `test_results.txt` (commit 3).
- Finalized `README.md`, `reflection.md`, and this file (commit 4).

**What did you have to verify or fix manually?**

I reviewed every diff. The key manual decision was rejecting the agent's first
instinct to "fix" the even-attempt type mismatch by also stringifying the guess —
that hides the symptom but compares numbers lexicographically. I had it delete the
str-cast instead and add a regression test (`check_guess(9, 100) == "Too Low"`).

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

**Prompt used:** *"Given these pure functions in `logic_utils.py`, list edge-case
inputs that could still break the game and write pytest cases for each. Cover
negative numbers, decimals, and very large values."*

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Negative numbers | (above) | `check_guess(-5, -1) == "Too Low"` | ✅ Yes | Comparison must stay numeric for negatives, not crash. |
| Very large values | (above) | `check_guess(1_000_000, 999_999) == "Too High"` | ✅ Yes | Python ints are unbounded, so this confirms no overflow/str issues. |
| str/int regression | (above) | `check_guess(9, 100) == "Too Low"` | ✅ Yes | Pins the original bug: `"9" > "100"` is True lexicographically. |
| Decimal input | (above) | `parse_guess("3.9") == (True, 3, None)` | ✅ Yes | Decimals should be accepted and truncated, not rejected. |
| Empty / None input | (above) | `parse_guess("")` and `parse_guess(None)` return `ok=False` | ✅ Yes | Game must prompt for a guess instead of erroring. |
