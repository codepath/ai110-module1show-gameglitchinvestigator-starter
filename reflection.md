# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, the hints were completely backwards — if I guessed 70 against a secret of 50, the game showed "Go HIGHER!" instead of "Go LOWER!" That made it impossible to converge on the answer using the clues alone. On top of that, every other attempt seemed to produce wrong comparisons (due to the secret being secretly cast to a string on even-numbered attempts), so the logic would flip even further. The score also fluctuated wildly on wrong guesses (going up by 5 on even wrong attempts, down on odd), which felt chaotic and wrong. Additionally, `logic_utils.py` raised `NotImplementedError` on all functions, so nothing actually worked if `app.py` tried to import from there.

- **Bug 1 (Inverted hints):** `check_guess` returned "📈 Go HIGHER!" when `guess > secret` — exactly backwards.
- **Bug 2 (String/int type switch):** On even attempts, `secret` was cast to `str`, making numeric comparison fail silently.
- **Bug 3 (Score on wrong guesses):** `update_score` added or subtracted 5 points on every wrong guess, not just wins.
- **Bug 4 (Hard easier than Normal):** `get_range_for_difficulty("Hard")` returned 1–50, which is a smaller range than Normal's 1–100.
- **Bug 5 (Attempts off-by-one):** `st.session_state.attempts` started at 1 instead of 0, meaning the first guess was counted as attempt #2.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess of 70, secret is 50 | "Too High — Go LOWER!" | "Too High — Go HIGHER!" (player told to go the wrong direction) | none — logic silently returned wrong message |
| Any guess on attempt #2 (even attempt) | Normal numeric comparison | Secret cast to string, e.g., `50` becomes `"50"`, string comparison `"70" > "50"` returns True but `"5" > "40"` is True lexicographically | none — silent wrong output |
| Guess 40 (wrong), score starts at 0 | Score stays 0 (no points for wrong guesses) | Score dropped to -5 (or +5 on even attempt) unpredictably | none — score visibly jumps in debug panel |
| Select "Hard" difficulty | Harder/larger range than Normal (1–100) | Range of 1–50, which is actually easier than Normal | none — debug panel showed `Range: 1 to 50` |
| First guess submitted | Attempt counter shows 1/8 | Counter showed 2/8 because attempts started at 1 | none — visible in debug panel |

---

## 2. How did you use AI as a teammate?

I used Claude (claude-sonnet-4-6) as my primary AI coding assistant throughout this project. The AI helped me identify the root cause of each bug, plan the refactor from `app.py` into `logic_utils.py`, and generate the edge-case pytest suite.

**Correct AI suggestion:** When I asked the AI to explain the string/int type switch bug on line 158–161 of `app.py`, it correctly identified that passing `secret` as a `str` on even attempts breaks numeric comparison because Python compares strings lexicographically — so `"7" > "50"` is `True` (comparing first characters "7" vs "5") even though numerically 7 < 50. I verified this by running `python3 -c "print('7' > '50')"` in the terminal, which printed `True`. The fix (always pass the integer secret) immediately resolved the erratic hints on even attempts.

**Incorrect/misleading AI suggestion:** Early in the session, the AI suggested that the score bug might be intentional — that giving +5 points for guesses on even attempts could be a "streak bonus" mechanic. I rejected this because (a) the code comment said nothing about bonuses, (b) the README explicitly lists the score as broken, and (c) the behavior was inconsistent with any coherent game design: it alternated between +5 and -5 based purely on parity of attempt number, regardless of how close the guess was. I verified the bug was real by tracing through `update_score` manually and confirming there was no design intent in the starter code.

---

## 3. Debugging and testing your fixes

To decide whether a bug was really fixed, I used two methods: running `pytest` to check the unit tests, and manually tracing the logic path in `logic_utils.py` with simple `print` statements and mental walkthroughs before running the Streamlit app.

For the inverted hints bug, I wrote `test_guess_too_high` which asserts `check_guess(60, 50) == "Too High"` and `test_guess_too_low` which asserts `check_guess(40, 50) == "Too Low"`. Before the fix, the logic returned the right *label* ("Too High") but wrong *message* ("Go HIGHER!"). After separating the outcome string from the display message (putting messages in `HINT_MESSAGES` in `app.py`), all three core tests passed immediately.

For the score bug, `test_score_only_increases_on_win` asserts that `update_score(0, "Too High", 1) == 0` — score unchanged on a wrong guess. This test failed against the original code and passed after the fix. The AI helped generate the edge cases for `parse_guess` (non-numeric strings, None, negative numbers, floats) by suggesting "what inputs could a user accidentally type?" — those prompts led to 6 additional tests that all pass.

---

## 4. What did you learn about Streamlit and state?

Streamlit rerenders the entire Python script from top to bottom every time a user interacts with the page (clicks a button, types in a box). This means any variable assigned normally (like `secret = random.randint(1, 100)`) gets re-assigned on every interaction, which is why the secret number kept changing. `st.session_state` is a persistent dictionary that survives these reruns — values stored there are only reset when you explicitly change them or the browser session ends. Think of each rerun as a fresh function call, and `session_state` as a global dictionary that persists across those calls. The key lesson: anything that should "remember" its value across user actions must live in `st.session_state`, not in a plain variable.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is writing the test *before* fully fixing the bug — once I wrote `test_guess_too_high`, I had a clear pass/fail signal that guided the fix and confirmed it worked without needing to manually click through the UI. In future projects I'll write a failing test first, then fix, then run to confirm.

For working with AI on code tasks, I'd use more specific prompts next time. Asking "explain this logic step-by-step" yielded much better results than asking "is this code correct?" — the AI's step-by-step trace immediately revealed the string comparison issue in a way that "looks fine to me" would not have.

This project changed how I think about AI-generated code: the AI can produce syntactically valid, plausibly correct-looking code that has subtle semantic bugs (like the score parity trick or the string cast) that only surface at runtime. AI code must be read critically, not trusted at face value — the bugs here weren't typos, they were logic errors that required understanding the full game flow to catch.
