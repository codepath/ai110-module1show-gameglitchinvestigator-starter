# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

**Purpose:** Glitchy Guesser is a Streamlit number-guessing game. You pick a
difficulty, the app picks a secret number in the matching range, and you have
a limited number of attempts to guess it, getting a "Too High"/"Too Low" hint
and a running score after each guess.

**Bugs found:**
- The "Too High"/"Too Low" hint messages were swapped (`check_guess`).
- The secret number was silently converted to a string on alternating
  attempts, causing lexicographic instead of numeric comparisons.
- The win-score formula subtracted one extra attempt's worth of points
  (`100 - 10 * (attempt_number + 1)`), and `"Too High"` sometimes rewarded
  +5 instead of deducting, depending on attempt parity.
- `attempts` was initialized to `1` instead of `0`, and "New Game" reset the
  secret with a hardcoded `randint(1, 100)` instead of the difficulty range.
- The guess input box lost or duplicated submissions because its widget key
  changed mid-script, and a later callback-based fix still needed two clicks
  to register a new guess.

**Fixes applied:**
- Rewrote `check_guess` to compare the guess/secret numerically and return a
  plain outcome string, with correct hint text looked up in `app.py`.
- Fixed the win formula and removed the parity bonus in `update_score`.
- Fixed `attempts` initialization and made "New Game" use `low`/`high` from
  the selected difficulty.
- Replaced the input handling with `st.form(clear_on_submit=False)` so the
  guess is read atomically with the submit click, with no race condition.
- Moved all of the game logic (`get_range_for_difficulty`, `parse_guess`,
  `check_guess`, `update_score`) into `logic_utils.py` and imported it from
  `app.py`.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User selects "Normal" difficulty (secret is between 1 and 100) and clicks into the guess box.
2. User enters a guess of 40 and clicks "Submit Guess" — the game shows "Too Low" (📈 Go HIGHER!) and the score drops by 5.
3. User enters a guess of 70 and submits — the game shows "Too High" (📉 Go LOWER!) and the score drops by another 5.
4. User enters a guess of 55 and submits — still "Too Low", score keeps updating correctly after every guess.
5. User enters the secret, 60, and submits — the game shows "🎉 Correct!", balloons appear, and the final score is displayed along with the secret number.
6. Clicking "New Game" resets attempts, score, and status, and picks a fresh secret within the selected difficulty's range.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
pytest tests/ -v
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
collected 5 items

tests\test_game_logic.py::test_winning_guess PASSED                      [ 20%]
tests\test_game_logic.py::test_guess_too_high PASSED                     [ 40%]
tests\test_game_logic.py::test_guess_too_low PASSED                      [ 60%]
tests\test_game_logic.py::test_win_on_first_attempt_scores_90_not_80 PASSED [ 80%]
tests\test_game_logic.py::test_too_high_always_deducts_even_on_even_attempt PASSED [100%]

========================= 5 passed, 1 warning in 0.08s =========================
```

## 🚀 Stretch Features

- [x] **Challenge 1: Advanced Edge-Case Testing** — added tests for `parse_guess` (previously untested: `None`, empty string, whitespace, non-numeric, decimal truncation, negative numbers), `check_guess` with negative numbers, and `update_score`'s 10-point floor clamp and unknown-outcome passthrough.

```
pytest tests/ -v
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
collected 14 items

tests\test_game_logic.py::test_winning_guess PASSED                      [  7%]
tests\test_game_logic.py::test_guess_too_high PASSED                     [ 14%]
tests\test_game_logic.py::test_guess_too_low PASSED                      [ 21%]
tests\test_game_logic.py::test_win_on_first_attempt_scores_90_not_80 PASSED [ 28%]
tests\test_game_logic.py::test_too_high_always_deducts_even_on_even_attempt PASSED [ 35%]
tests\test_game_logic.py::test_parse_guess_none_returns_error PASSED     [ 42%]
tests\test_game_logic.py::test_parse_guess_empty_string_returns_error PASSED [ 50%]
tests\test_game_logic.py::test_parse_guess_whitespace_is_not_a_number PASSED [ 57%]
tests\test_game_logic.py::test_parse_guess_non_numeric_string_returns_error PASSED [ 64%]
tests\test_game_logic.py::test_parse_guess_decimal_string_truncates_to_int PASSED [ 71%]
tests\test_game_logic.py::test_parse_guess_negative_number_is_accepted PASSED [ 78%]
tests\test_game_logic.py::test_check_guess_handles_negative_numbers PASSED [ 85%]
tests\test_game_logic.py::test_update_score_win_floor_clamps_at_10 PASSED [ 92%]
tests\test_game_logic.py::test_update_score_unknown_outcome_leaves_score_unchanged PASSED [100%]

========================= 14 passed, 1 warning in 0.11s =========================
```

- [x] **Challenge 4: Enhanced UI** — replaced the plain "Attempts left" text with `st.metric` cards for Score, Attempts Left, and Difficulty, added an `st.progress` bar for attempts used, fixed the range message to reflect the selected difficulty instead of a hardcoded "1 and 100", and added an icon-coded Guess History list (✅ win, ⬆️ too high, ⬇️ too low, ⚠️ invalid input) showing the most recent guess first.
