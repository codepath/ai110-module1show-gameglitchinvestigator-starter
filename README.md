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

- [ ] The purpose of this game is to guess the randomized number in a set amount of guesses. This forces you to balance between luck and skill!
- [ ] The primary two bugs I found was how the hints were initially unhelpful and terrible, alongside how the "New Game" button didn't work at all.
- [ ] By reworking and refactoring some of the functions and testing it alongside an agentic model, I was able to resolve the bugs that I ran into.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Guess 50 => Too low, go higher!
2. Guess 75 => Too low, go higher!
3. Guess 88 => Too high, go lower!
4. Guess 82 => CORRECT!!!! *ballons float up on screen*

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
=============================================== test session starts ===============================================
platform darwin -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/brucenguyen/Library/CloudStorage/OneDrive-Personal/Documents/CodePath/AI 110/Projects/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.15.1
collected 1 item                                                                                                  

test/test_game_logic.py .                                                                                   [100%]

================================================ 1 passed in 0.02s ================================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
