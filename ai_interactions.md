# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Review `app.py` for logic bugs — specifically a reversed hint, a UI issue where
only the submitted guess seems to show after the 2nd click, and any scoring
issues — and point out the exact line numbers.

**What did the agent do?**

Read through `app.py` and identified the following bugs with line references:

| # | Bug | Line(s) |
|---|---|---|
| 1 | Reversed hint messages — `"Too High"` paired with "Go HIGHER" instead of "Go LOWER", and vice versa | 39, 41 (duplicated at 47, 48) |
| 2 | Secret type-flip forces a lexicographic string comparison instead of numeric | 159-162 (triggers except branch at 42-48) |
| 3 | Off-by-one in the win points formula (extra `+ 1`) | 53 |
| 4 | "Too High" branch rewards +5 on even attempt numbers instead of always deducting | 58-61 |
| 5 | Init/reset inconsistency (`attempts = 1` vs. `attempts = 0`); New Game ignores the difficulty range | 97, 136, 137 |
| 6 | Text input key doesn't vary per attempt, so the box doesn't clear after submit | 122-125 |

**What did you have to verify or fix manually?**

Manually traced the attempt-parity logic to confirm the secret-type bug
triggers on guess #1 (not #2 as it first appeared from the UI symptom), by
walking through `attempts` starting at 1 and incrementing before the parity
check. Still need to apply the fixes and re-test each scenario (hint
direction, scoring, new game reset) to confirm no other bugs surface.

**Bug Reproduction Logs**

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output | Suspected Code Location |
|---|---|---|---|---|
| Guess of 60 when secret is 30 | "Too High" hint (📉 Go LOWER) | "📈 Go HIGHER!" hint shown | none | `app.py`, `check_guess` (lines 38-41) |
| Guess of 9 when secret is 10, on an even-numbered attempt | "Too Low" outcome (9 < 10) | "Too High" outcome (wrong, string `"9" > "10"` compares lexicographically) | none | `app.py`, `check_guess` except branch (lines 42-48) + secret stringify (lines 159-162) |
| Win on attempt 1 | Score +90 (`100 - 10*1`) | Score +80 (`100 - 10*(1+1)`) | none | `app.py`, `update_score` (line 53) |
| Wrong guess ("Too High") on attempt 2 | Score -5 | Score +5 | none | `app.py`, `update_score` (lines 58-61) |
| Fresh page load, no guesses yet | "Attempts left: 8" (full limit) | "Attempts left: 7" | none | `app.py`, lines 97, 112 |
| Click "New Game" while Difficulty = Easy | Secret range 1-20 | Secret randomized 1-100 | none | `app.py`, line 137 |
| Submit guess "50", then start typing next guess | Input box empty, ready for new guess | Previous guess "50" still shown in box | none | `app.py`, lines 122-125 |

### Full Fix, Refactor & Enhancement Workflow

**Files modified:** `app.py`, `logic_utils.py`, `tests/test_game_logic.py`,
`README.md`, `reflection.md`, `ai_interactions.md` (this file).

**What I asked the agent to do:**
- Fix every bug listed in the table above (hints, scoring, attempts init,
  New Game range, input clearing).
- Refactor the game logic out of `app.py` into `logic_utils.py` and make the
  existing `tests/test_game_logic.py` pass.
- Write regression tests for the specific bugs it had just fixed, plus
  additional edge-case tests (Challenge 1).
- Diagnose and fix a follow-up bug where the guess box still needed two
  clicks to register a new guess after the first fix.
- Add an Enhanced UI (Challenge 4): score/attempts/difficulty metrics, a
  progress bar, an icon-coded guess history, and a sidebar "closeness"
  visualization for past guesses.
- Finalize `README.md` (Demo Walkthrough, Document Your Experience, Test
  Results) and `reflection.md` (all five reflection questions).

**What it completed:**
- All listed bugs fixed in `app.py`/`logic_utils.py`; `check_guess` and
  `update_score` moved into `logic_utils.py` with `app.py` importing them.
- 17 passing tests in `tests/test_game_logic.py`, including regression tests
  for the scoring bugs and edge-case tests for `parse_guess`/`check_guess`/
  `update_score`.
- Replaced the first input-clearing fix (an `on_click` callback) with
  `st.form(clear_on_submit=False)` once the callback approach proved
  unreliable in the running app.
- Added the Challenge 4 UI elements (metrics, progress bar, icon history,
  sidebar closeness bars) without touching the logic layer.
- Filled in `README.md` and `reflection.md` end to end.

**Manual corrections I made:**
- Rejected the agent's first `on_click`/callback fix for the input box after
  testing it myself in the browser and finding it still needed two clicks;
  asked for the `st.form` version instead.
- Asked it to stop auto-clearing the guess box after submit (`clear_on_submit`
  back to `False`) once I decided I wanted the submitted guess to stay
  visible until I edited it, instead of disappearing immediately.
- Caught that the secret was still visible in "Developer Debug Info" and had
  it removed, and asked for the secret to be shown on the persistent
  game-over screen instead of only the one-time win/loss message.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

**Prompt used:**

```
Generate pytest test cases for `parse_guess`, `check_guess`, and `update_score` covering edge cases: None input, empty string, whitespace, non-numeric strings, decimal truncation, negative numbers, and ensure the 10-point floor on wins works.
```

**Test cases AI suggested:**

| Edge Case | Test Name | Did It Pass? | Your Reasoning |
|-----------|-----------|--------------|----------------|
| `parse_guess(None)` | `test_parse_guess_none_returns_error` | ✓ Yes | Correctly rejected; error message "Enter a guess." |
| `parse_guess("")` | `test_parse_guess_empty_string_returns_error` | ✓ Yes | Same as None—both are missing input. |
| `parse_guess("   ")` (whitespace) | `test_parse_guess_whitespace_is_not_a_number` | ✓ Yes | Raised ValueError on `int("   ")`, caught as non-numeric. |
| `parse_guess("banana")` | `test_parse_guess_non_numeric_string_returns_error` | ✓ Yes | ValueError on `int("banana")` correctly mapped to error. |
| `parse_guess("12.7")` | `test_parse_guess_decimal_string_truncates_to_int` | ✓ Yes | `int(float("12.7"))` → 12, as designed. |
| `parse_guess("-15")` | `test_parse_guess_negative_number_is_accepted` | ✓ Yes | Negative numbers accepted; no range check in `parse_guess`. |
| `check_guess(-10, -5)`, etc. | `test_check_guess_handles_negative_numbers` | ✓ Yes | Numeric comparison works on negatives; outcome correct. |
| `update_score(0, "Win", 15)` | `test_update_score_win_floor_clamps_at_10` | ✓ Yes | Late-game win (attempt 15) clamped to 10-point floor, not negative. |
| `update_score(42, "Unknown", 1)` | `test_update_score_unknown_outcome_leaves_score_unchanged` | ✓ Yes | Unrecognized outcome passthrough—score stays 42. |

**Did you manually adjust any tests?**

No; all AI-suggested tests passed on first run after the scoring and parsing functions were fixed. The test structure and assertions matched the implementation exactly.

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
review your code for PEP 8 style compliance and apply its suggestions to
resolve any formatting or naming issues it identifies.
```

**Linting output before:**

```
app.py:83:100: E501 line too long (118 > 99 characters)
app.py:122:100: E501 line too long (115 > 99 characters)
tests/test_game_logic.py:3:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:8:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:13:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:18:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:24:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:32:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:38:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:43:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:48:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:53:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:59:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:64:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:69:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:75:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:80:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:85:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:91:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:96:22: W292 no newline at end of file
```

(Run via `python -m pycodestyle app.py logic_utils.py tests/test_game_logic.py
--max-line-length=99`; `logic_utils.py` had zero violations.)

**Changes applied:**

The AI pointed out two categories of issues: two comment lines in `app.py`
that exceeded 99 characters (E501), and every function in
`tests/test_game_logic.py` missing the PEP 8-required 2 blank lines before
top-level `def`s (E302), plus a missing trailing newline at end of file
(W292). I applied all of it as suggested — reworded the two long `# FIX:`
comments in `app.py` to say the same thing more concisely, and added the
blank-line spacing and trailing newline in the test file. Re-running
`pycodestyle` afterward produced no output, confirming full compliance, and
`pytest` still showed `17 passed`, so the formatting-only changes didn't
affect behavior.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

"For the old issue—The win-score formula subtracted one extra attempt's worth of points (`100 - 10 * (attempt_number + 1)`), and `"Too High"` sometimes rewarded +5 instead of deducting, depending on attempt parity—find a fix (don't use existing fix)."

| Criterion | Lina | Grok 4.6 | Sonnet 5.5 (mine) |
|-----------|------|----------|-------------------|
| **Win Formula** | `90 - earlier_attempts * 10` | `90 - 10 * (n - 1)` | `100 - 10 * attempts_used` |
| **Readability** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ Simplest | ⭐⭐⭐ Defensive |
| **Pythonic Style** | ⭐⭐⭐⭐ Penalty dict | ⭐⭐⭐⭐⭐ Direct branches | ⭐⭐⭐ Dict of negatives |
| **Explanation Quality** | None provided | None provided | Separated win/wrong logic |

**Which did you prefer and why?**

**Winner: Grok 4.6** — Most readable and Pythonic.
- Simple conditionals (`if outcome in ("Too High", "Too Low"): return current_score - 5`) instead of dict lookup overhead.
- Formula `90 - 10*(n-1)` is mathematically independent from the buggy code, proving genuine alternative approach.
- No unnecessary guards (`max(attempt_number, 1)`) or data structures.
- Explicit is better than implicit (Zen of Python).

**Runner-up: Lina** — Good Pythonic style, but overkill.
- Penalty dict `{"Too High": -5, "Too Low": -5}` is DRY and idiomatic, but redundant (two identical values).
- Variable name `earlier_attempts` is self-documenting.

**Third: Sonnet 5.5 (mine)** — Structurally reused existing code.
- Violated constraint: formula mirrors the buggy `100 - 10 * n` form instead of being independent.
- `max(attempt_number, 1)` guard is defensive but unnecessary (app.py guarantees attempt ≥ 1).
- Dict of negative values less intuitive than direct subtraction.
