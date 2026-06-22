# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

An AI built a simple "Number Guessing Game" using Streamlit — then walked away. The result was a game that:

- Gave backwards hints (told you to go HIGHER when you were already too high)
- Changed the secret number's type mid-game, breaking comparisons
- Adjusted the score even on wrong guesses
- Listed "Hard" as a 1–50 range (easier than Normal's 1–100)

This repo documents the debugging, refactoring, and testing work done to fix all four issues.

## 🐛 Bugs Found

| # | Bug | Location | Root Cause |
|---|-----|----------|-----------|
| 1 | Inverted hints | `app.py` `check_guess` | Message strings were swapped: "Go HIGHER!" fired when `guess > secret` |
| 2 | String/int type switch | `app.py` lines 158–161 | On even attempts, `secret` was cast to `str`, breaking `>` comparison |
| 3 | Score changes on wrong guesses | `app.py` `update_score` | `+5` / `-5` awarded on every wrong guess based on parity of attempt number |
| 4 | Hard difficulty easier than Normal | `app.py` `get_range_for_difficulty` | `"Hard"` returned range `1–50`; Normal was `1–100` |
| 5 | Attempts off-by-one | `app.py` session state init | `attempts` initialized to `1` instead of `0` |

## 🛠️ Fixes Applied

1. **Refactored all game logic** into `logic_utils.py` — `check_guess`, `parse_guess`, `update_score`, `get_range_for_difficulty` are now properly implemented there.
2. **Fixed inverted hints** — `check_guess` now correctly returns `"Too High"` when `guess > secret`; display messages live in a `HINT_MESSAGES` dict in `app.py`.
3. **Removed the string cast** — `secret` is always passed as an `int` to `check_guess`, eliminating lexicographic comparison bugs.
4. **Simplified score logic** — `update_score` now only awards points on a `"Win"`; wrong guesses leave the score unchanged.
5. **Fixed Hard difficulty** — range is now `1–200`, making it genuinely harder than Normal's `1–100`.
6. **Fixed attempts init** — session state starts at `0`, so attempt #1 is correctly counted as the first guess.
7. **Fixed New Game button** — now resets `status` and `history` alongside `attempts` and `secret`.

## 🛠️ Setup

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

## 📝 Document Your Experience

**Game purpose:** A number-guessing game where the player tries to identify a secret number within a limited number of attempts. Hints ("Too High" / "Too Low") guide each guess, and a score rewards faster wins.

**Bugs found:** Five bugs, all in the starter `app.py` — inverted hints, type-switching on even attempts, erratic score changes, wrong difficulty range, and an off-by-one in the attempt counter.

**Fixes applied:** Refactored all game logic into `logic_utils.py` with correct implementations; fixed all five bugs in `app.py` and added 15 pytest cases to verify the fixes.

## 📸 Demo Walkthrough

1. Player opens the app and selects **Normal** difficulty (range 1–100, 8 attempts).
2. Player enters **40** as a first guess. Secret is 65. Game returns "Too High — Go LOWER!" — wait, that's wrong. Actually 40 < 65, so game returns **"Too Low — Go HIGHER!"**. Score stays 0 (no points for wrong guesses).
3. Player enters **70**. Secret is 65. Game returns **"Too High — Go LOWER!"**. Score stays 0.
4. Player enters **65**. Secret is 65. Game returns **"🎉 Correct!"**. Score jumps to **70** (100 − 10 × 3 attempts = 70 points). Balloons appear.
5. Player clicks **New Game** — all state resets (secret, attempts, score, history, status). A fresh game begins immediately.

## 🧪 Test Results

```
============================= test session starts ==============================
platform linux -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/pouya/Documents/codepath-ai110/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.13.0
collecting ... collected 15 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  6%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 13%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 20%]
tests/test_game_logic.py::test_parse_guess_non_numeric_string PASSED     [ 26%]
tests/test_game_logic.py::test_parse_guess_empty_string PASSED           [ 33%]
tests/test_game_logic.py::test_parse_guess_none PASSED                   [ 40%]
tests/test_game_logic.py::test_parse_guess_negative_number PASSED        [ 46%]
tests/test_game_logic.py::test_parse_guess_float_string PASSED           [ 53%]
tests/test_game_logic.py::test_parse_guess_valid_integer PASSED          [ 60%]
tests/test_game_logic.py::test_score_only_increases_on_win PASSED        [ 66%]
tests/test_game_logic.py::test_score_only_increases_on_too_low PASSED    [ 73%]
tests/test_game_logic.py::test_score_win_first_attempt PASSED            [ 80%]
tests/test_game_logic.py::test_score_win_clamped_at_minimum PASSED       [ 86%]
tests/test_game_logic.py::test_difficulty_hard_is_harder_than_normal PASSED [ 93%]
tests/test_game_logic.py::test_difficulty_easy_range PASSED              [100%]

============================== 15 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- **Advanced Edge-Case Testing:** 12 additional pytest cases cover non-numeric inputs (`"abc"`, `""`), `None`, negative numbers, float strings, score behavior on wrong guesses, score floor clamping, and difficulty ordering. All 15 tests pass (see output above).
- **Professional Documentation & Style:** All functions in `logic_utils.py` have docstrings explaining parameters, return values, and the specific bug each fixed. Code follows PEP 8 naming and style conventions throughout.
- **Enhanced UI:** Hint messages are stored in a `HINT_MESSAGES` lookup dict rather than inline string literals, making them easy to customize. The info banner now correctly shows the difficulty-specific range (e.g., "Guess a number between 1 and 200" on Hard).
