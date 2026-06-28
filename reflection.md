# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran the game, it accepted guesses outside the allowed range and the comparison logic was broken. The app often told me to go higher even when I had guessed too high, and it allowed values below 0 and above 100. The "New Game" button also did not reliably reset the game state.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 60 with secret 50 | "Too High" and prompt to go lower | Displayed "Go HIGHER!" | none |
| 0 on Normal difficulty | Reject guess and show range error | Accepted guess and continued | none |
| 101 on Normal difficulty | Reject guess and show range error | Accepted guess and continued | none |
| 40 with secret 50 | "Too Low" and prompt to go higher | Displayed "Go HIGHER!" or no comparison | none |
| Click New Game | Restart game with new secret and reset attempts/history | Game state did not reset properly | none |

---

## 2. How did you use AI as a teammate?

I used the VS Code AI coding assistant to inspect `app.py` and identify where the game logic was broken. The AI helped me break the issue into smaller fixes: separate the logic into `logic_utils.py`, add input validation, and fix the hint comparison.

One correct AI suggestion was to move `parse_guess` and `check_guess` into `logic_utils.py` so the game logic was easier to test. I added focused pytest cases to verify the fixed behaviors; please run the tests locally to confirm (see README). Note: I could not run `pytest` from this environment.

One misleading AI suggestion was an earlier fallback that converted secret values to strings during comparison. That logic was unnecessary and made the bug harder to trace, so I removed it and verified the fix with tests.

---

## 3. Debugging and testing your fixes

I added automated tests and used manual browser testing to validate behavior. For example, there is a pytest asserting that `check_guess(60, 50)` returns `("Too High", "📉 Go LOWER!")`. Run the test suite locally to confirm the passing results, and then re-run the app to manually verify rejected out-of-range inputs and proper reset behavior.

AI helped design the tests by suggesting the specific functions to verify and the expected output for each bug case. That made the test coverage more focused and reliable.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the script from top to bottom on every interaction, but it preserves session state between reruns. That means UI components are rebuilt each time, while session state values like the secret number stay stored.

I learned that you must deliberately update session state to change the app state, and that `st.rerun()` is useful after a full reset so the UI refreshes immediately.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is writing small automated tests for each logic change before trusting the app behavior. This helped catch inverted hints and range validation problems quickly.

Next time I work with AI on code, I would ask for a specific fix and then verify the exact diff before accepting the change. That avoids accepting incorrect suggestions too quickly.

This project made me more skeptical of AI-generated code. I now expect to verify each logic change with tests and to separate UI code from core logic for easier debugging.
