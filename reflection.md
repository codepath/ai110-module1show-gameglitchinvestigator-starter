# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").

When I first ran the game, it looked like a normal Streamlit guessing game but was completely unplayable. The hints were backwards: when my guess was too high it said "Go HIGHER!" and when it was too low it said "Go LOWER!", which led me in the wrong direction every time. The "New Game" button didn't actually reset the game — after winning or losing, clicking it still showed the old game-over message because the status was never reset to "playing". Additionally, the secret number on Hard difficulty could be generated outside the 1-50 range (e.g., 72) because the random number generator was hardcoded to use 1-100. On even-numbered attempts, the secret was converted to a string, causing unpredictable comparison behavior between integers and strings.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude Code (Claude Opus 4.6) as my AI teammate for this project. One correct suggestion was identifying that the hint messages in `check_guess` were swapped — Claude immediately spotted that `guess > secret` returned "Go HIGHER!" instead of "Go LOWER!" and fixed it. I verified this by running the game and checking that guessing 94 against a secret of 50 now correctly said "Go LOWER!". One initially incomplete suggestion was the New Game fix — Claude first only reset `attempts` to 0 and added `status = "playing"`, but missed that attempts should initialize to 1 (matching the rest of the code's convention) and that history also needed clearing. I caught this by testing the New Game button and noticing the attempt counter was off by one.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed by both running the Streamlit app manually and writing automated pytest tests. For example, I wrote `test_high_guess_says_go_lower()` which calls `check_guess(75, 50)` and asserts that "LOWER" appears in the message — this directly targets the swapped-hints bug and confirms the fix works. I also wrote `test_validate_negative()` to ensure guesses like -5 are rejected when the range is 1-100. Claude helped generate the test structure and suggested testing edge cases like empty strings, non-numeric input, and out-of-range values. All 15 tests pass, covering `check_guess`, `parse_guess`, `validate_range`, `get_range_for_difficulty`, and `update_score`.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret number could behave inconsistently because on even-numbered attempts, the code converted it to a string (`secret = str(st.session_state.secret)`), causing type-mismatch issues in comparisons. Streamlit reruns the entire script from top to bottom every time a user interacts with a widget (clicks a button, types in an input). Without `st.session_state`, any variable you set would be lost on the next rerun. `session_state` is like a persistent dictionary that survives across reruns. The fix was to always use `st.session_state.secret` as an integer (removing the string conversion), and to regenerate the secret when the difficulty changes so it stays within the correct range.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to keep is writing targeted pytest cases for each specific bug before considering it fixed — it forces me to think about what "correct" actually means and catches regressions. Next time, I would give the AI more context upfront about the full codebase structure rather than reporting bugs one at a time, which would let it spot related issues (like the New Game button using a hardcoded range) in one pass. This project taught me that AI-generated code can look clean and complete but still contain subtle logic errors — you should always play-test and write tests rather than trusting that code "looks right."
