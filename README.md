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

The purpose of the game is to guess a hidden number using hints while managing a changing score. I found that the secret value and hint comparisons were inconsistent, the attempt counter lagged behind the guesses, the trial hint disappeared after reruns, and the score did not always match the final result. I fixed these problems with Streamlit session state, consistent numeric comparisons, a separate trial round, one-based real attempts, and score updates that stop when the game ends.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:
1. Start the app and choose a difficulty. The game starts with 50 points.
2. Enter a number and press **Submit Guess**. The first submission is a trial attempt that gives a higher or lower hint and sets a bound without using a real attempt.
3. Make real guesses starting with Attempt 1. The hint tells you whether to guess higher or lower, and the score can increase or decrease based on the attempt and feedback.
4. Watch the current score and attempts shown in the game. The score updates after each real guess, and the trial attempt does not count toward the attempt limit.
5. Win by guessing the secret number. You lose if you run out of attempts or if your score goes below 0, and the final score shows the score at the moment the game ends.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
================ test session starts =================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: /mnt/c/Users/bbydr/ai110-module1show-gameglitchinvestigator-starter
collected 11 items                                   

tests/test_game_logic.py ...........           [100%]

================= 11 passed in 0.41s =================
```

## 🚀 Stretch Features

- [x] Challenge 4: Enhanced UI

I improved the interface by making changes to difficulty selector, a sidebar showing the number range and attempt limit, a trial hint, attempt information, score display, guess history in the developer panel, and clear success or game-over messages. The **New Game** button also resets the visible game state so the player can start again.
