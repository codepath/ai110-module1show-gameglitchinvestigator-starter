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

- [x] The game's purpose is to let the player guess a hidden number in a Streamlit app while learning how app state and logic bugs can break a simple game.
- [x] I found that the hint text was backwards, so guesses that were too high told the player to go higher and guesses that were too low told the player to go lower.
- [x] I also found state-related issues where the secret number and attempts count could behave inconsistently across reruns.
- [x] I fixed the logic by separating the helper functions into `logic_utils.py`, then using session state more consistently so the game state stays stable during play.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Open the app with `python -m streamlit run app.py` and choose a difficulty level from the sidebar.
2. Make an initial guess, such as 40, and the app responds with **Too Low** and the **Go HIGHER!** hint.
3. Make a second guess, such as 70, and the app responds with **Too High** and the **Go LOWER!** hint.
4. Keep adjusting the guess based on the hint until the secret number is found and the game shows the win message.
5. Click **New Game** to reset the secret, score, attempts, and history, then start another round.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
============================= test session starts ==============================
platform darwin -- Python 3.11.15, pytest-9.0.3, pluggy-1.6.0
collected 3 items

tests/test_game_logic.py ...                                             [100%]

============================== 3 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
