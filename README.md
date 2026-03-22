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

- This game is a number guessing game where players try to guess a secret number within a limited number of attempts, with 3 level. 
- Bugs found:
   - State bug — The secret number regenerated on every button click because it wasn't stored in st.session_state.
   - Inverted hints — The "Go Higher/Lower" hints were backwards (guess > secret said "Go Higher" instead of "Go Lower").
   - Difficulty range bug — Easy/Normal/Hard were mapped to the wrong number ranges.
   - core logic bug — The scoring system didn't correctly reward wins or penalize wrong guesses.
   - Status reset bug — After winning, starting a new game didn't reset status back to "playing", so the win message persisted.

- Fixes applied: All five bugs are fixed in the current app.py and logic_utils.py.

## Tests
![alt text](image-1.png)

## 📸 Demo
![alt text](image.png)

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
