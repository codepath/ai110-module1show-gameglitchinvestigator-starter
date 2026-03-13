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

The game's purpose was to allow the user to play a guessing game with a variety of different modes. Score is kept for each play with the option to create a new game. 

- [x] Detail which bugs you found.

The bugs that I found were the following: 

1. The number of attempt displayed were off by 1
2. The range to guess was hardcoded to "1 to 100"
3. The user's score was allowed to go below 0. 
4. The "New Game" button reset the secret number but did not allow a new game
5. The hints for Lower/Higher were not being displayed properly 
6. The range for each difficulty mode was not set properly.

- [x] Explain what fixes you applied.
1. The number of attempt was adjusted by 1
2. Low and High variables were used to display the proper range for each difficulty mode.
3. A minimum was set so that the user's score would not go below zero. 
4. When the "New Game" button was selected, the state was set to "playing" so that the user can play another game with their previous score. 
5. The logic was adjusted so that Lower/Higher would display properly for each guess
6. Low and High variables were used to set the range for the secret number that was produced on a new game or a change of difficulty mode. 

## 📸 Demo

- [x] https://i.imgur.com/Y5J703i.gif

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
