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

- [✔️] Describe the game's purpose.
- [✔️] Detail which bugs you found.
- [✔️] Explain what fixes you applied.

## 📸 Demo

- [✔️] Generates appropriate hint if guess is higher than secret:

  <img width="500" src="https://github.com/user-attachments/assets/2c1bb83f-2ba6-449d-bf02-df13df230d7e" />

- [✔️] Generates appropriate hint if guess is lower than secret:

  <img width="500" src="https://github.com/user-attachments/assets/245198f8-7d02-49e1-be6b-458ca062e9da" />

- [✔️] Difficulty level range from left sidebar and center message match:

  <img width="400" src="https://github.com/user-attachments/assets/ed9abf67-56db-45e7-b3e3-f7a077543bb0" />
  <img width="400" src="https://github.com/user-attachments/assets/3e0d766c-cb83-4560-b176-c20f97538d0f" />
  <img width="400" src="https://github.com/user-attachments/assets/8584ff7f-6bba-471a-94ab-b0354f7a4bc7" />

- [✔️] Documents the first guess input and the following ones as well:

    <img width="500" src="https://github.com/user-attachments/assets/20a9bed0-e138-4467-b47f-1c66e16427d8" />



      

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
