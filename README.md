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

- [ ] The game's purpose is to teach AI assisted debuging and become familiar with Streamlit. 
- [ ] The bugs I found were that Go Lower and Go Higher were inverted and new game was not creating a new game after a win.
- [ ] Some of the changes I applied were swapping the go lower/go higher hint, adjusted the difficulty ranges and replace the hardcoded 1-100 to lower-higher variables depending on the level of difficulty.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. **Launch the game.** Run `python -m streamlit run app.py` and open the app in your browser. You'll see the "🎮 Game Glitch Investigator" title with a **Settings** sidebar.
2. **Pick a difficulty.** In the sidebar, choose **Easy**, **Normal**, or **Hard**. The range now scales with difficulty — Easy is 1–20, Normal is 1–50, Hard is 1–100 — and the sidebar shows the matching range and number of attempts allowed.
3. **Read the prompt.** The main panel shows "Guess a number between X and Y" using the *actual* range for your chosen difficulty (no longer hardcoded to 1–100), along with the correct number of attempts left.
4. **Make a guess.** Type a number into "Enter your guess:" and click **Submit Guess 🚀**. With "Show hint" checked, you'll get an accurate hint: guess too high → *"📉 Go LOWER!"*, guess too low → *"📈 Go HIGHER!"*.
5. **Follow the hints to win.** Keep guessing — the hints now point you toward the secret. The "Attempts left" counter decreases correctly by one per guess, and you get the full number of attempts the difficulty allows.
6. **Win the game.** When you guess correctly, balloons appear with "You won! The secret was N. Final score: …".
7. **Start a fresh game.** Click **New Game 🔁**. The secret is regenerated within the current difficulty's range, and the score, attempt counter, and guess history all reset — so the game is immediately playable again instead of staying stuck on "You already won."
8. *(Optional)* **Verify behind the scenes.** Expand "Developer Debug Info" to watch the secret, attempts, score, and history update live as you play.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.14.4, pytest-9.1.0, pluggy-1.6.0
rootdir: C:\Github\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.13.0
collected 6 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 16%]
tests/test_game_logic.py::test_too_high_tells_player_to_go_lower PASSED  [ 33%]
tests/test_game_logic.py::test_too_low_tells_player_to_go_higher PASSED  [ 50%]
tests/test_game_logic.py::test_string_fallback_win PASSED                [ 66%]
tests/test_game_logic.py::test_string_fallback_too_high_goes_lower PASSED [ 83%]
tests/test_game_logic.py::test_string_fallback_too_low_goes_higher PASSED [100%]

============================== 6 passed in 0.03s ==============================

```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
