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

It's a number-guessing game: the computer picks a secret number in a range based on difficulty (Easy 1–20, Normal 1–100, Hard 1–50), and you try to guess it within a limited number of attempts, using "higher/lower" hints to home in on it and earning a score. It was intentionally built with bugs as a "glitch investigator" exercise
- [ ] Detail which bugs you found.

Swapped high/low hints — when your guess was too high, the game told you to "Go HIGHER" (and "Go LOWER" when too low) — the exact opposite of what it should say. (Fixed)

Hint showing after a win — when you guessed correctly, the game still popped up a yellow hint warning ("🎉 Correct!") alongside the win celebration, instead of just showing the win. (You asked to leave this one unfixed.)

- [ ] Explain what fixes you applied.
Swapped high/low hints (logic_utils.py, check_guess) — Reversed the hint messages so a too-high guess now says "📉 Go LOWER!" and a too-low guess says "📈 Go HIGHER!". Fixed in both the normal path and the TypeError fallback.

String-comparison glitch (app.py) — Removed the code that converted the secret to a string on even-numbered attempts, which had been forcing buggy text comparisons (e.g. "50" < "7") and producing wrong directions. The secret now stays an integer every turn.

Broken "New Game" (app.py) — The reset only cleared attempts and secret, leaving status stuck on "won"/"lost" so the game immediately stopped. It now also resets status, score, and history, and picks the new secret from the selected difficulty's range instead of a hardcoded 1–100.



## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. user enters 55
2. game says to go higher
3. user enters 70
4. game says to go lower
5. user enter 65
6. game says to go higher
7. user enters 66
8. game says the user won

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0 -- C:\Users\skkpr\AppData\Local\Python\pythoncore-3.14-64\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\skkpr\Desktop\Github - codepath
plugins: anyio-4.13.0
collecting ... collected 13 items

ai110-module1show-gameglitchinvestigator-starter/test/test_game_logic.py::TestCheckGuessDirection::test_guess_too_high_says_go_lower PASSED [  7%]
ai110-module1show-gameglitchinvestigator-starter/test/test_game_logic.py::TestCheckGuessDirection::test_guess_too_low_says_go_higher PASSED [ 15%]
ai110-module1show-gameglitchinvestigator-starter/test/test_game_logic.py::TestCheckGuessDirection::test_correct_guess_wins PASSED [ 23%]
ai110-module1show-gameglitchinvestigator-starter/test/test_game_logic.py::TestCheckGuessDirection::test_outcome_matches_comparison[2-1-Too High] PASSED [ 30%]
ai110-module1show-gameglitchinvestigator-starter/test/test_game_logic.py::TestCheckGuessDirection::test_outcome_matches_comparison[1-2-Too Low] PASSED [ 38%]
ai110-module1show-gameglitchinvestigator-starter/test/test_game_logic.py::TestCheckGuessDirection::test_outcome_matches_comparison[100-99-Too High] PASSED [ 46%]
ai110-module1show-gameglitchinvestigator-starter/test/test_game_logic.py::TestCheckGuessDirection::test_outcome_matches_comparison[99-100-Too Low] PASSED [ 53%]
ai110-module1show-gameglitchinvestigator-starter/test/test_game_logic.py::TestCheckGuessDirection::test_hint_direction_is_consistent_with_outcome[80-50] PASSED [ 61%]
ai110-module1show-gameglitchinvestigator-starter/test/test_game_logic.py::TestCheckGuessDirection::test_hint_direction_is_consistent_with_outcome[20-50] PASSED [ 69%]
ai110-module1show-gameglitchinvestigator-starter/test/test_game_logic.py::TestCheckGuessDirection::test_hint_direction_is_consistent_with_outcome[2-1] PASSED [ 76%]
ai110-module1show-gameglitchinvestigator-starter/test/test_game_logic.py::TestCheckGuessDirection::test_hint_direction_is_consistent_with_outcome[1-2] PASSED [ 84%]
ai110-module1show-gameglitchinvestigator-starter/test/test_game_logic.py::TestCheckGuessTypeErrorFallback::test_string_secret_too_high_says_go_lower PASSED [ 92%]
ai110-module1show-gameglitchinvestigator-starter/test/test_game_logic.py::TestCheckGuessTypeErrorFallback::test_string_secret_too_low_says_go_higher PASSED [100%]

============================= 13 passed in 0.03s ==============================


## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
