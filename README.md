# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python -m streamlit run app.py   # then open http://localhost:8501

# 4. Run the tests
pytest
```

> **Note on macOS:** recent versions ship `python3` but no bare `python`, so
> `python -m streamlit ...` fails with `command not found` until the virtual
> environment above is activated. Outside a venv, use `python3 -m streamlit run app.py`.

To see the secret number while testing, start the app with debug output enabled:

```bash
GLITCH_DEBUG=1 python -m streamlit run app.py
```

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

**The game's purpose.** A number-guessing game. The app picks a secret number
inside a range set by the difficulty, and you have a limited number of attempts
to find it, with a higher/lower hint after each guess and a score that rewards
winning in fewer tries.

**Bugs found and fixed.** Six, none of which produced an error message: the
higher/lower hints were inverted; the secret was cast to a string on every even
attempt, which made the comparison alphabetical (`"9" > "100"`); New Game never
reset the game's status, so a finished game could not be restarted; the hint
disappeared whenever the "Show hint" checkbox was toggled; wrong guesses gained
points on even turns and lost them on odd; and the secret was printed onto the
page in a debug panel. Full write-up, with a reproduction log, in
[`reflection.md`](reflection.md).

**Fixes applied.** Game rules moved out of `app.py` into `logic_utils.py` so
they can be tested without a browser; `check_guess()` now returns a single
outcome string with hint text owned by `hint_message()`, so the outcome and the
advice cannot contradict each other; a single `reset_game()` is used by both
startup and New Game; the hint outcome is stored in session state and rendered
on every rerun; and debug output is gated behind `GLITCH_DEBUG=1`.

## 📸 Demo Walkthrough

A step-by-step trace of the fixed game, so a reader can follow the behavior
end-to-end without running it. Steps 4, 7, 9 and 10 exercise the bugs that were
repaired.

1. User starts a new game on **Normal** difficulty. The sidebar shows
   `Range: 1 to 100` and `Attempts allowed: 8`. Say the secret is **63**.
2. The page reads "Guess a number between 1 and 100. Attempts left: 8." The
   secret is not shown anywhere, because debug output is off by default.
3. User enters **40** and clicks Submit. The hint reads
   "📈 Too low - go HIGHER!". The score stays at 0, since a wrong guess costs
   5 points but the score is floored at zero.
4. User unticks **Show hint**, and the hint disappears. Ticking it again brings
   the same hint back. *(Previously the hint vanished permanently, because it
   was only drawn on the rerun that followed a Submit click.)*
5. User enters **70**. The hint reads "📉 Too high - go LOWER!" — the guess was
   above the secret, so the advice points down.
6. User enters **60**, then **65**. Hints stay consistent on every turn,
   regardless of whether the attempt number is odd or even.
7. User types **abc** and submits. The game shows "That is not a whole number."
   and the attempt counter does **not** move. Typing **999** shows "Guess must
   be between 1 and 100." *(Previously both burned a turn, and 999 was
   accepted as a legitimate guess.)*
8. User enters **63**. Balloons appear and the page shows
   "You won! The secret was 63. Final score: 60."
9. User clicks **New Game 🔁**. A fresh round starts immediately with a new
   secret, attempts back to 8 and the score reset. *(Previously the page was
   stuck on the win/lose message permanently and only a browser refresh
   cleared it.)*
10. User switches difficulty to **Hard**. The sidebar updates to
    `Range: 1 to 200`, and a new secret is drawn from inside that range.
    *(Previously "Hard" used a narrower range than "Normal", making it easier,
    and the old out-of-range secret was kept after switching.)*



## 🧪 Test Results

```
$ pytest tests/

rootdir: /Users/mikeyamo-arthur/Documents/ai110-module1show-gameglitchinvestigator-starter
collected 17 items

tests/test_game_logic.py .................                               [100%]

============================== 17 passed in 0.02s ==============================
```

17 tests: the 3 that shipped with the starter (unchanged) plus 14 added during
debugging. Each new test targets a specific bug from the reproduction log in
`reflection.md` and fails against the original code.

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
