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

- [x] Describe the game's purpose: A number guessing game where players guess a secret number within a range based on difficulty, using higher/lower hints.
- [x] Detail which bugs you found:
  1. **Swapped hints** - "Go HIGHER" shown when guess was too high, "Go LOWER" when too low
  2. **New Game broken** - status never reset to "playing", attempts reset to wrong value, history not cleared
  3. **No range validation** - negative numbers and out-of-range guesses were accepted
  4. **String conversion bug** - secret converted to string on even attempts, causing unreliable comparisons
  5. **Hardcoded range** - New Game and initial generation used 1-100 regardless of difficulty
- [x] Explain what fixes you applied:
  1. Swapped the hint messages so "Too High" says "Go LOWER" and vice versa
  2. Reset `status`, `history`, `score`, and `attempts` properly in New Game handler
  3. Added `validate_range()` function to reject out-of-range guesses
  4. Removed the string conversion — secret is always compared as an integer
  5. Used `low, high` from difficulty settings for all random number generation
  6. Refactored all game logic into `logic_utils.py` and updated imports in `app.py`

## 📸 Demo

- [ <img width="1839" height="749" alt="image" src="https://github.com/user-attachments/assets/23fdb826-c0ce-45f5-a1bc-77b1a03b4e70" />
] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
