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

**Purpose:** A Streamlit number guessing game. The player picks a difficulty (Easy 1–20, Normal 1–100, Hard 1–50), then guesses a secret number within a limited number of attempts, using "higher/lower" hints and earning points for winning quickly.

**Bugs found:**
- The hints were reversed: guessing above the secret said "Go HIGHER" and below said "Go LOWER".
- On even attempts the secret was turned into a string, so guesses were compared as text instead of numbers and the hints were wrong.
- The game counted an attempt before the first guess, and invalid input also used up an attempt.
- The "Attempts left" message didn't update after a guess.
- The hint jumped around the page and disappeared between guesses.
- "New Game" and changing the difficulty didn't fully reset the game, so attempts, history and the secret's range carried over.

**Fixes applied:**
- Moved `check_guess` into `logic_utils.py` and fixed it so a high guess says "Go LOWER" and a low guess says "Go HIGHER".
- Always compare the guess against the numeric secret.
- Start attempts at 0 and count only valid guesses; refresh the attempts-left message after each guess.
- Show the hint in a fixed spot under the input and keep it in session state so it stays visible.
- Reset attempts, status, history and the secret (from the difficulty's range) on New Game and on difficulty change.
- Updated the tests for `check_guess`'s `(outcome, message)` return value and added a test that the attempts-left count goes down only on valid guesses.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User enters a guess of 10
2. Game says go higher
3. Score updates after each guess
4. Game ends when the correct guess is made


**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
File	Coverage	Lines not run by any test
app.py	73%	Easy/Hard ranges, the parse_guess paths for empty and decimal input, all of update_score, the New Game button, and the win/lose endings
logic_utils.py	75%	The three functions that still raise NotImplementedError (get_range_for_difficulty, parse_guess, update_score)
$ pytest tests/
============================== 4 passed in 1.04s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
