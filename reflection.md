# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| | | | |
| | | | |
| | | | |

**Answer:** When I first ran the game, it appeared functional but had several critical bugs. **Bug 1: Reversed hints** — When my guess was too high (e.g., 60 vs secret 50), the game said "Go HIGHER!" instead of "Go LOWER!". When my guess was too low (e.g., 40 vs 50), it said "Go LOWER!" instead of "Go HIGHER!". **Bug 2: Wrong hints on even-numbered attempts** — The code alternated between passing the secret as an int and as a string. On even attempts, comparing int guess to string secret caused TypeError, and the fallback used string comparison (e.g., "9" > "50" is True lexicographically), giving incorrect "Too High" for a guess of 9 when the secret was 50. **Bug 3: New Game ignored difficulty** — Clicking "New Game" always used range 1–100, even on Easy (1–20) or Hard (1–50). The info message also always said "1 and 100" regardless of difficulty.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

**Answer:** I used Cursor's AI assistant (Composer) to investigate and fix the bugs. **Correct suggestion:** The AI correctly identified that the hint messages in `check_guess` were reversed — when `guess > secret`, the message should say "Go LOWER!" not "Go HIGHER!". I verified by running `check_guess(60, 50)` and confirming it returned "Too High" with "Go LOWER!". **Incorrect/misleading suggestion:** When first analyzing the int/string bug, the AI initially suggested only fixing the hint text. The real fix was to always pass the secret as an int (removing the `attempts % 2` alternation) and to normalize types inside `check_guess`. I verified by adding a test `check_guess(9, "50")` — the wrong fix would still fail; the correct fix passes.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

**Answer:** I used both automated tests and manual play to verify fixes. I added pytest cases in `test_game_logic.py` for `check_guess`, `parse_guess`, and `get_range_for_difficulty`. The test `test_guess_too_high_with_string_secret` specifically targets the int/string bug: `check_guess(9, "50")` must return "Too Low" because 9 < 50. Before the fix, this returned "Too High" due to string comparison. After normalizing types in `check_guess`, the test passes. I also ran the Streamlit app manually and confirmed hints were correct and the game was winnable. The AI helped design the edge-case test for the string secret scenario.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

**Answer:** The secret didn't actually change on every rerun — it was stored in `st.session_state.secret` and persisted. The *perception* of a changing secret came from the int/string bug: on even attempts, wrong hints made it seem like the secret had changed. **Streamlit reruns:** Every time you interact (click, type, change a widget), Streamlit reruns the entire script from top to bottom. Variables are recreated unless stored in `st.session_state`, which persists across reruns. **Stable secret:** The secret was already stable via session state. The fix was to always pass `st.session_state.secret` (an int) to `check_guess` instead of alternating with `str(secret)` on even attempts, so hints became consistent and the game felt stable.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

**Answer:** **Reusable habit:** Writing a targeted pytest for each bug *before* or *right after* fixing it. The `test_guess_too_high_with_string_secret` test locks in the fix and prevents regression. **Do differently:** I would ask the AI to explain the *root cause* before suggesting fixes. The first suggestion (fix hint text only) missed the type-comparison bug; asking "why does this happen on even attempts?" led to the real fix. **AI-generated code:** This project showed that AI can produce code that looks correct but has subtle logic and type bugs. Human review, testing, and understanding the flow are essential — AI is a helpful pair programmer, not a replacement for careful verification.
