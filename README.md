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

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. To start the game input the command 'python3 -m streamlit run app.py' in the terminal. This will open the game in a browser with the title 'Game Glitch Investigator'
2. In the left sidebar the user has a option of difficulty levels (Easy, Normal, Hard). Each level has a range the user can guess to, but also it showcases the number of attempts the user has in that level.
3. Type a number into 'Enter your guess' box and click 'Submit Guess.' The game will compare your guess with the secret number, with that comparison it will either tell you if your guess is 'Too Low' or 'Too High.' This will point you to either try to re-guess based on the prompt you were given.
4. Keep guessing and use the hints to narrow it down. Each guess is recorded so, beware of your attempts. All of that will be displayed in Developer Debug Info panel.
5. When you guess the secret correctly, the game will prompt you with balloons and a congralutations text. It will also display your final score
6. Click 'New Game' to start over, this will restart your attempts, score, and the secret number. Basically all the history from the previous game is no longer present.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
======================================================== test session starts ========================================================
platform darwin -- Python 3.14.0, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/brooklynharden/CodePath/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.13.0
collected 3 items                                                                                                                   

tests/test_game_logic.py ...                                                                                                  [100%]

========================================================= 3 passed in 0.01s =========================================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
