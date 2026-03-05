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
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when you click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.** A number-guessing game where you pick a difficulty (Easy 1–20, Normal 1–100, Hard 1–50), guess the secret number, and receive hints (Too High / Too Low) until you win or run out of attempts.
- [x] **Detail which bugs you found.** (1) Reversed hints — "Too High" said "Go HIGHER!" instead of "Go LOWER!". (2) Wrong hints on even attempts — secret was passed as string, causing bad string comparison (e.g., 9 vs "50" gave "Too High"). (3) New Game ignored difficulty — always used 1–100. (4) Info message hardcoded to "1 and 100". (5) Attempts display off by one.
- [x] **Explain what fixes you applied.** Refactored `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` into `logic_utils.py`. Fixed hint messages in `check_guess`. Normalized guess/secret to ints to fix type comparison. New Game now uses `(low, high)` from difficulty. Info message uses actual range. Attempts start at 0 for correct display.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

*To capture: Run `python -m streamlit run app.py`, play until you win, then take a screenshot.*

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
