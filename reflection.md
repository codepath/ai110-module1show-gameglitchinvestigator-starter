# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The game ran without crashing and looked like a normal number-guessing game, but several things behaved unexpectedly:

- **New Game button doesn't reset game status:** I expected clicking "New Game 🔁" after winning or losing to start a fresh round I could actually play. Instead, `st.session_state.status` is never reset back to `"playing"`, so the app immediately shows "Game over" / "You already won" again and calls `st.stop()`, leaving the game permanently stuck.

- **Backwards hints:** I expected that guessing too high would show a hint telling me to guess lower next time, and guessing too low would tell me to guess higher. Instead, the hints are swapped: a too-high guess shows "📈 Go HIGHER!" and a too-low guess shows "📉 Go LOWER!".

- **Inconsistent scoring for "Too High" guesses:** I expected every incorrect guess to subtract 5 points from my score, the same way a "Too Low" guess always does. Instead, in `update_score`, a "Too High" guess on an even-numbered attempt (2nd, 4th, 6th, ...) actually adds 5 points to my score instead of subtracting them, while a "Too High" guess on an odd-numbered attempt correctly subtracts 5.

**Bug Reproduction Logs**

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output |
|------------|--------------------|------------------|--------------------------|
| Won or lost a game, then clicked "New Game 🔁" | A new secret is generated and I can submit guesses again | App shows "Game over. Start a new game to try again." (or "You already won...") and blocks input via st.stop() | none |
| Guessed higher than the secret (e.g., guess of 80 when secret is 40) | Hint says "Too High - Go LOWER!" | Hint shown says "📈 Go HIGHER!" | none |
| Guessed too high on an even-numbered attempt (e.g., attempt #2) | Score decreases by 5, same as any other wrong guess | Score increases by 5 | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

     I used Claude Code for this project, working in agent mode so it could read, edit, and test the code directly.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

    - When fixing the backwards hints bug, the AI suggested swapping the hint strings in `check_guess` so a "Too High" result returns "📉 Go LOWER!" and a "Too Low" result returns "📈 Go HIGHER!" (instead of the other way around). I verified this by having it write two new pytest tests, `test_too_high_hint_tells_player_to_go_lower` and `test_too_low_hint_tells_player_to_go_higher`, which both pass against the fixed code.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

    - When I ran plain `pytest` and got `ModuleNotFoundError: No module named 'logic_utils'`, the AI's first instinct was to add an empty `conftest.py` file at the project root to fix Python's import path. That turned out to be unnecessary — the real problem was that `logic_utils.py` was still just `NotImplementedError` stubs, and once that was implemented, running `python -m pytest` (instead of plain `pytest`) already adds the project root to `sys.path` with no extra files needed. I verified this by running `python -m pytest -v`, which passed all 6 tests without any new config files.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

    - For each bug, I used AI to write a pytest test that encodes the *expected, correct* behavior, then ran it against the fixed code. If the test passes — and would have failed against the original buggy code — I treat the bug as fixed.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

    - `test_too_high_always_subtracts_points` asserts `update_score(50, "Too High", attempt_number=2) == 45`. Against the original buggy code, attempt #2 (an even attempt) would have returned 55 (it added 5 instead of subtracting); against the fixed code it returns 45, confirming the scoring bug is fixed.

- Did AI help you design or understand any tests? How?

    - Yes. Claude Code wrote all three new tests in `tests/test_game_logic.py` (`test_too_high_hint_tells_player_to_go_lower`, `test_too_low_hint_tells_player_to_go_higher`, and `test_too_high_always_subtracts_points`) targeting the hint and scoring fixes, and also implemented `logic_utils.py` so the three pre-existing starter tests (`test_winning_guess`, `test_guess_too_high`, `test_guess_too_low`) could finally pass too. Final result of `python -m pytest -v`: `6 passed`.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

    - Every time you click a button or type something, Streamlit re-runs the whole script from the top, like restarting the program. That would normally wipe out all your variables. `st.session_state` is like a backpack that doesn't get emptied between reruns — anything you put in it (like the score, secret number, or attempt count) is still there next time. This clicked for me with the "New Game" bug: the game stayed stuck because `st.session_state.status` never got reset, even though everything else restarted.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

    - Writing a small pytest test for the *correct* behavior right after I find a bug, then using it to prove the fix actually works. I also liked keeping the game logic in its own file (`logic_utils.py`) so I could test it without running the whole app.

- What is one thing you would do differently next time you work with AI on a coding task?

    - Push back more on the AI's first answer and ask "why is this happening?" before accepting a fix. The `conftest.py` suggestion was a quick patch that didn't fix the real problem (the empty `logic_utils.py`), and I only caught that because I checked it with tests.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

    - AI code can run with no errors and still be wrong — the backwards hints and the scoring bug both "worked" without crashing, but did the wrong thing. This taught me that "it runs" and "it's correct" are not the same, and tests are how you actually check.
