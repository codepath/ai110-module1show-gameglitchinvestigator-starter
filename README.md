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

**Purpose of the game.** A classic number-guessing game built in Streamlit:
the app picks a secret number inside a range that depends on the difficulty
(Easy 1–20, Normal 1–100, Hard 1–50), and you guess until you find it or run
out of attempts. After each guess it tells you whether to go higher or lower
and tracks a score that rewards faster wins.

**Bugs found.**

1. **Backwards hints** — `check_guess` told you to go "HIGHER" when your guess
   was too high (and vice-versa); the two messages were swapped.
2. **Shape-shifting secret** — on every even-numbered attempt `app.py` cast the
   secret to a string, so an integer guess was compared against a string. You
   could never win on an even attempt and the Higher/Lower hint became
   lexicographic nonsense (e.g. `"9" > "100"`).
3. **Broken "New Game"** — it reset only `attempts` and `secret` (hardcoded to
   `1..100`), never `score`, `status`, or `history`. After a loss the status
   stayed `"lost"`, so `st.stop()` fired and the player was locked out.
4. **Off-by-one attempts** — `attempts` started at `1`, so "Attempts left" was
   wrong before the first guess.
5. **Hardcoded range text** — the info banner always said "between 1 and 100"
   even on Easy/Hard.
6. **Erratic scoring** — a wrong "Too High" guess *added* 5 points on even
   attempts, so the score could climb while losing.

**Fixes applied.** Moved the four core functions into `logic_utils.py` (now
pure and unit-testable) and imported them into `app.py`. `check_guess` returns
just the outcome string and a new `hint_for_outcome` helper produces the
corrected Higher/Lower text. Removed the str-cast so comparisons are always
numeric. `New Game` now resets the full state and uses the difficulty range.
`attempts` starts at 0, invalid input no longer burns an attempt, the banner
shows the real range, and scoring is consistent and floored at 0.

## 📸 Demo Walkthrough

A sample game on **Normal** difficulty (range 1–100, secret = 50):

1. The app shows "Guess a number between 1 and 100. Attempts left: 8".
2. User enters `40` → outcome **Too Low**, hint "📈 Too low — go HIGHER!".
3. User enters `70` → outcome **Too High**, hint "📉 Too high — go LOWER!".
4. User enters `55` → **Too High**; the score drops by 5 with each wrong guess.
5. User enters `50` → **Win**: balloons fire, the secret and final score are
   shown, and `status` flips to `"won"`.
6. Clicking **New Game 🔁** fully resets attempts, score, status, and history
   and draws a fresh secret from the current difficulty range.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ pytest tests/
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.1.0, pluggy-1.6.0
collected 15 items

tests/test_game_logic.py ...............                                 [100%]

============================== 15 passed in 0.02s ==============================
```

## 🚀 Stretch Features

- [x] **Challenge 1: Advanced Edge-Case Testing** — expanded the suite from 3
  to 15 tests covering negative numbers, very large values, the str/int
  comparison regression, `parse_guess` edge cases (empty/None/non-numeric/
  decimal), consistent non-negative scoring, and hint direction. The passing
  output is shown above and prompts are documented in `ai_interactions.md`.
