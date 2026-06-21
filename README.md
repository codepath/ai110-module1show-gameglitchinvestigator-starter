# 🎮 Game Glitch Investigator: The Impossible Guesser

## 📝 Document Your Experience

The purpose of this game is to let the player guess a secret number within a limited number of attempts. The app gives feedback after each guess, tracks the number of attempts, keeps score, and shows whether the player has won or lost.

The bugs I found included incorrect higher/lower hints, the New Game button not fully resetting the game, attempts going into negative numbers, and the Show Hint checkbox not controlling when hints appeared.

I fixed the game by moving core logic into `logic_utils.py`, correcting the `check_guess()` logic, using `st.session_state` to preserve game values, resetting all important values when New Game is clicked, preventing negative attempts from displaying, and making the hint display depend on the checkbox.

## 📸 Demo Walkthrough

1. Run the app using `python -m streamlit run app.py`.
2. Choose a difficulty level from the sidebar.
3. Open the Developer Debug Info section to view the secret number for testing.
4. Enter a guess lower than the secret number and confirm that the app says to go higher.
5. Enter a guess higher than the secret number and confirm that the app says to go lower.
6. Enter the correct secret number and confirm that the game shows the winning message.
7. Click New Game and confirm that the secret number, attempts, score, status, history, and last hint reset correctly.



## 🧪 Test Results

python3 -m pytest test/test_game_logic.py
======================================================== test session starts =========================================================
platform darwin -- Python 3.14.2, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/cinthiaochoa/Desktop/CODEPath/Projects/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.12.1
collected 3 items                                                                                                                    

test/test_game_logic.py ...                                                                                                    [100%]

========================================================= 3 passed in 0.02s ==========================================================


## 🚀 Stretch Features

* No stretch features attempted.
