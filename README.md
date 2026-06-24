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
The game's purpose is to illustrate how bugs can be detrimental to the player's experience to where the player is constantly sabotaged from ever guessing the secret number if the bugs make the game impossible to play. 
- [ ] Detail which bugs you found.
I found several bugs in the game that make it difficult for anyone to play. First, there was a bug with the hints as the player would receive incorrect hints from their guesses to find the secret number. Secondly, there was a bug with the restart button where the player couldn't restart the game after presssing the option as they either correctly guess the secret number or they ran out of attempts that a new secret number would appear, but the player couldn't enter their guesses anymore. Finally, there was a bug with setting the game's difficulty as the game would always default to Normal difficulty where the player only had the option to guess a number in the range of 1 through 200, and not have the other two difficulty options, such as Easy and Hard.
- [ ] Explain what fixes you applied.
I focused on fixing two bugs in the game. First, I applied fixes to repair the hints bug where I coerced the secret variable to become an integer, and changed the sign in a comparison statement to be '<' in a function so that the player is being provided with the correct hints to have a better chance at guessing the secret number. Next, I applied fixes to repair the difficulty bug where I made a wider range for the game's Hard difficulty to have values from 1 through 200, and ensured the game read the low and high values in correspondance to the difficulty so that the player is guessing a secret number that falls within the range of numbers, which is dependent on the difficulty option chosen beforehand. 

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Game is set to Normal difficulty by default (range of 1-100)
2. Player guesses the number 40
3. Game returns "Go LOWER!"
4. Player guesses the number 30
5. Game returns "Go HIGHER!"
6. Score is updated correctly for each guess made by the player
7. Game ends after the correct guess (First Option)
8. Game ends after all attempts have been used (Second Option)

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
