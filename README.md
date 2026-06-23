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

- The game's purpose is to be able to input numbers in order to guess the value of the mystery target number.
- The game had multiple bugs that impacted gameplay. The "New Game" button does not function correctly after a win or loss, causing the game to become stuck and requiring a full page refresh to restart. Additionally, pressing the Enter key does not submit a guess despite the UI suggesting it should, forcing users to click the "Submit Guess" button instead. The attempts counter is incorrectly initialized at 1, and users often need to press the "Submit Guess" button twice before receiving feedback, with some guesses not being recorded on the first click. The hint system is also unreliable, occasionally providing incorrect guidance (e.g., suggesting to guess higher when the input is already above the target number). Furthermore, the "New Game" button only works while the game is still in progress. Input validation is flawed, as non-integer values are still accepted and stored.
- The fixes for this app were: The game logic was moved into a separate module, making the main app easier to read and maintain. Added a start_new_game() function, which makes sure session state variables (like attempts, score, and history) reset correctly, fixing issues where the game would get stuck or start with incorrect values. Reworked the st.form in order to allow the Enter key to properly submit guesses and prevent the need to click the submit button multiple times. Input validation now happens before updating the game state. The new game button resets the game at any time using st.rerun(). Made sure feedback is accurate and consistent.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User sets difficulty to normal
2. Makes a guess of 80
3. Game returns "Too High"
4. User enters a guess of 78 → "Too Low"
5. Score updates correctly after each guess
6. Game ends after the correct guess

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
tests/test_game_logic.py::test_winning_guess PASSED                      [ 20%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 40%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 60%]
tests/test_game_logic.py::test_parse_guess_only_accepts_integers PASSED  [ 80%]
tests/test_game_logic.py::test_hint_direction_is_correct PASSED          [100%]

============================== 5 passed in 0.02s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
