# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

No module named streamlit issue.
Fix : python3 && python3 --version && pip3 install streamlit 2>&1 | tail -5

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

Bug1 : win the game,the new game button dosen't work
Bug2 : fail the game, then new game button dosen't work
Problem3 : if choose no hint, each submittion has no notification to user, which is very user-unfriendly

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

Claude

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

Bug 1 & 2: Added st.session_state.status = "playing" (plus score and history reset) so New Game fully resets the game state.
Problem 3: Added an else branch that shows the attempt count when hint is hidden.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
None, all suggestions are correct
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I tried the web funcitons again, and problems disappear

- Describe at least one test you ran (manual or using pytest)  and what it showed you about your code.

I ran `python3 -m pytest tests/test_game_logic.py -v` and all 9 tests passed. The test `test_new_game_state_reset` was especially revealing — it simulated a session state dict after winning, applied the new-game reset logic, and confirmed that `status`, `score`, and `history` all returned to their initial values. Without that test it would have been easy to miss resetting `history` or `score` and only fix `status`.

- Did AI help you design or understand any tests? How?

Yes. I asked Claude to generate pytest cases specifically targeting the three bugs. Claude grouped the tests into sections (Bug1 & Bug2, Problem3) and explained the reasoning behind each test in comments — for example, why `test_win_outcome_triggers_status_won` matters: if `check_guess` never returns `"Win"`, the broken state is never entered and the bug can't be reproduced. That explanation helped me understand what each test was actually verifying, not just that it passed.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every time a user clicks a button or changes any input, Streamlit reruns the entire Python script from top to bottom — like refreshing a page.
Normal variables reset to their default values on every rerun, so Streamlit provides `st.session_state`, a dictionary that persists across reruns. Think of it like a notepad that survives each page refresh: you write values to it, and the next time the script runs it can read them back. The bug in this project was a perfect example of why this matters — forgetting to reset `st.session_state.status` in the New Game handler meant the old "won" value survived into the next rerun and broke the game.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

Writing tests that target specific bugs, not just general correctness. Before this project I would have written a test like "check_guess(50, 50) returns Win" and called it done. 
Now I also write tests that simulate the exact scenario that caused the bug — like building a fake session state dict in the "won" state and verifying the reset logic clears every field. Those bug-reproduction tests catch regressions that happy-path tests miss.

- What is one thing you would do differently next time you work with AI on a coding task?

I would read and understand each AI-suggested change before accepting it, rather than applying fixes and moving on. In this project the fixes were correct, but I noticed I couldn't always explain *why* the fix worked until I looked at the code more carefully. Next time I'll ask the AI to explain the root cause first, then propose a fix, so I build understanding alongside working code.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

AI can generate plausible-looking code very quickly, but "it looks right" and "it is right" are different things — this game shipped with three real bugs despite being described as "production-ready." I now treat AI-generated code the way I would treat code from a new teammate: read it, question it, and always verify with tests before trusting it.
