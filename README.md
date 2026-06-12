# 🎮 Game Glitch Investigator

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

  This is a number guessing game where the player tries to guess a 
  secret number within a limited number of attempts. The player 
  selects a difficulty (Easy, Normal, or Hard) which changes the 
  number range and attempt limit. After each guess the game gives 
  a hint telling the player to go higher or lower, and the score 
  updates based on how many attempts it took to win.

- [x] Detail which bugs you found.

  - **Backwards hints** — on every second guess the secret number 
    was converted to a string causing wrong comparisons
  - **Wrong difficulty ranges** — Hard mode had range 1–50 which 
    was easier than Normal mode's 1–100
  - **Score bug** — wrong guesses sometimes gained points instead 
    of losing them
  - **Attempts counter** — counter started at 1 instead of 0 
    causing an off-by-one error from the first guess
  - **Double click submit** — Submit button required two clicks 
    to register a guess

- [x] Explain what fixes you applied.

  - Moved all game logic functions into `logic_utils.py` and 
    removed the `raise NotImplementedError` stubs
  - Removed the `str(secret)` cast that caused backwards hints — 
    now always compares integer to integer
  - Fixed difficulty ranges so Easy=1–20, Normal=1–100, Hard=1–500
  - Fixed score logic so wrong guesses always lose 5 points
  - Fixed attempts counter to initialize at 0 instead of 1
  - Added `conftest.py` so pytest can find `logic_utils.py`

## 📸 Demo Walkthrough

1. Game starts on Normal difficulty, secret number is chosen randomly 
   between 1 and 100, player has 8 attempts
2. Player enters guess of **40** → Game returns "📈 Go HIGHER!" 
   because 40 is less than the secret, score decreases by 5
3. Player enters guess of **80** → Game returns "📉 Go LOWER!" 
   because 80 is greater than the secret, score decreases by 5
4. Player enters guess of **60** → Game returns "📉 Go LOWER!" 
   score decreases by 5
5. Player enters guess of **50** → Game returns "📉 Go LOWER!" 
   score decreases by 5
6. Player enters guess of **45** → Game returns "🎉 Correct!" 
   balloons appear on screen and final score is displayed
7. Player clicks New Game button to reset everything and play again

## 🧪 Test Results

```
collected 18 items

tests/test_game_logic.py::test_check_guess_too_high PASSED        [  6%]
tests/test_game_logic.py::test_check_guess_too_low PASSED         [ 13%]
tests/test_game_logic.py::test_check_guess_win PASSED             [ 20%]
tests/test_game_logic.py::test_check_guess_always_int_comparison PASSED [ 26%]
tests/test_game_logic.py::test_hard_range_bigger_than_normal PASSED [ 33%]
tests/test_game_logic.py::test_wrong_guess_loses_points PASSED    [ 40%]
tests/test_game_logic.py::test_win_gains_points PASSED            [ 46%]
tests/test_game_logic.py::test_parse_valid_guess PASSED           [ 53%]
tests/test_game_logic.py::test_parse_empty_guess PASSED           [ 60%]
tests/test_game_logic.py::test_negative_number PASSED             [ 66%]
tests/test_game_logic.py::test_decimal_input PASSED               [ 73%]
tests/test_game_logic.py::test_very_large_number PASSED           [ 80%]
tests/test_game_logic.py::test_letters_input PASSED               [ 86%]
tests/test_game_logic.py::test_whitespace_input PASSED            [ 93%]
tests/test_game_logic.py::test_zero_input PASSED                  [100%]

18 passed in 0.03s
```

## 🚀 Stretch Features

- [x] Challenge 1: Advanced Edge-Case Testing — added 6 edge case 
  tests covering negative numbers, decimals, very large numbers, 
  letters, whitespace, and zero. All 18 tests pass. See 
  `ai_interactions.md` for the prompts used and reasoning behind 
  each edge case chosen.