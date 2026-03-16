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
  - A Streamlit-powered number guessing game where the player tries to guess a secret number with limited attempts.
- [x] Detail which bugs you found.
  - Hints were reversed (too high said go higher and vice versa).
  - New Game reset was incomplete (session state not fully reset and secret generated from wrong range).
  - Attempts counter was off by one and game ended prematurely.
- [x] Explain what fixes you applied.
  - Refactored core logic (`parse_guess`, `check_guess`, `update_score`, `get_range_for_difficulty`) into `logic_utils.py`.
  - Corrected hint logic and score update behavior.
  - Reset attempts, score, status, history on new game and start attempts at 0.

## 📸 Demo

- ![alt text](Final_image.png)

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
