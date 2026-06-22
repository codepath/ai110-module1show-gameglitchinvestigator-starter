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
  
  > The game was created to test your number guessing skills by hiding intentional bugs in the code for players to investigate and fix. The game challenges both your guessing ability and your debugging skills.

- [ ] Detail which bugs you found.
  
  > **Bug 1:** After a win/loss, the game stuck and the difficulty picked by the user was ignored. 
  > 
  > **Bug 2:** The scoring system wasn't properly implemented, for example, It incremented the score every even attempt.
  > 
  > **Bug 3:** The hints were presenting the wrong information and the attempts were wonky. 
  > 
  > **Bug 4:** The attempts counter started at `1` on page load but reset to `0` on New Game, so the first session always showed one fewer attempt than available.
  > 
  > **Bug 5:** The win scoring formula used `attempt_number + 1` instead of `attempt_number - 1`, meaning a first-try win only awarded 80 points instead of the full 100.

- [ ] Explain what fixes you applied.
  
  > **New game fix**: Restarted every session variable and indicated a new game status to the user
  > 
  > **Scoring fix:** Removed the `if attempt_number % 2 == 0: return current_score + 5` branch from `update_score` so that any wrong guess ("Too High" or "Too Low") consistently subtracts 5 points.
  > 
  > **Attempts fix:** Changed the initial value of `st.session_state.attempts` from `1` to `0` to match the reset value used by New Game.
  > 
  > **Win formula fix:** Corrected `100 - 10 * (attempt_number + 1)` to `100 - 10 * (attempt_number - 1)` so a first-try win awards the full 100 points.
  > 
  > **Hint fix:** Removed the code that randomly converted the secret number to a string on even attempts, which was causing the type-mismatch bug that produced wrong "Too High"/"Too Low" hints.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User enters a guess of 50
2. Game returns "Go LOWER"
3. User enters a guess of 20 > "Go HIGHER"
4. Score updates correctly after each guess
5. Game ends after the correct guess 

**Screenshot** *(optional)*: 

<img title="" src="file:///C:/Users/tonis/AppData/Roaming/marktext/images/2026-06-21-16-27-10-image.png" alt="" width="410" data-align="center">

## 🧪 Test Results

```
pytest
============================ test session starts ==========================
platform win32 -- Python 3.14.0, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\user123\Documents\ai110-module1show-gameglitchinvestigator-starter
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.13.0
collected 19 items                                                                                                                                                                         

tests\test_game_logic.py ...................                        [100%]

============================ 19 passed in 0.23s ==========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]

  Challenge 1

```
 pytest
======================== test session starts ======================================
platform win32 -- Python 3.14.0, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\tonis\Documents\ai110-module1show-gameglitchinvestigator-starter
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.13.0
collected 29 items                                                                                                                                                                         

tests\test_game_logic.py .............................                                                                                                                               [100%]

======================== 29 passed in 0.11s ======================================
```

Challenge 2

```
platform win32 -- Python 3.14.0, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\tonis\Documents\ai110-module1show-gameglitchinvestigator-starter
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.13.0
collected 37 items                                                                                                                                                          

tests\test_game_logic.py .............................                                                                                                                [ 78%]
tests\test_high_score.py ........   
                                                                                                                                  [100%]
====================== 37 passed in 0.14s ===========================================================================
```
