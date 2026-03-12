# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  We found that the guessing logic was swapped and we litetally never win . 
      1. Swapped logic 

      the difficulty levels were swapped . Hard (1-50) is easier than Normal (1-100) , when Hard should have the highest range

      2. Penalty for all guesses ( even correct ones)
        2.1 even guesses get a +5 boost even if they're wrong 
        2.2 odd guesses get -5 deductible always

      3. Level Attempts were also swapped . Normal had more attempts than easy which is weird


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Claude Code and Copoilot while attaching app.py . Copoilit was slower than Claude Code and it was giving me suggestions that were sort of not that related to the bug I had

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  Claude correctly identified that the `try/except TypeError` block in `check_guess` was masking a deeper bug — the caller was intentionally converting the secret to a string on even attempts, which caused broken lexicographic comparisons like `"9" > "10"` being True. Claude suggested removing the type confusion entirely and always passing the secret as an int. I verified this by running pytest and checking that `check_guess(9, 10)` returned "Too Low" as expected.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

  Copilot suggested fixing the hint messages by only changing the text strings but leaving the `try/except` block in place, which would have still caused wrong results on even-numbered attempts due to string comparison. I caught this by manually testing with the secret visible in the debug panel and noticing the direction was still sometimes wrong on attempt 2.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I ran the new code in localhost and played the game again to see if the bugs I saw were fixed or not

- Describe at least one test you ran (manual or using pytest)and what it showed you about your code.

I looked at the aecret number and put it the first , basically winning from the first attempt to see if I still got deducted points or not

- Did AI help you design or understand any tests? How?

  Yes — Claude generated the full pytest suite in `tests/test_game_logic.py`. It also implemented `logic_utils.py` so the functions could be tested independently from the Streamlit UI. Each test was directly tied to a specific bug we fixed, for example `test_too_high_says_go_lower` to catch the swapped hint messages, and `test_win_on_first_attempt_scores_100` to catch the off-by-one in the scoring formula. This helped me understand that tests should be written around the exact wrong behavior, not just the expected correct one.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

  Streamlit reruns the entire Python script from top to bottom every time the user interacts with anything — clicking a button, typing, anything. Without the `if "secret" not in st.session_state` guard, `random.randint()` would be called on every rerun and generate a new number each time. Even with the guard, the new game button was regenerating the secret using the hardcoded range `(1, 100)` instead of the difficulty-based range, so switching difficulty mid-game would give a secret outside the displayed range.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Imagine every time you click a button on a webpage, the entire page code runs again from scratch — variables reset, everything starts over. That's Streamlit. Session state is like a small notepad that survives those reruns. If you want the game to remember the secret number between clicks, you store it in session state, otherwise it disappears and gets replaced every time the page refreshes.

- What change did you make that finally gave the game a stable secret number?

  The key fix was initializing `st.session_state.attempts` to `0` instead of `1`, and making sure the new game button reset `status`, `history`, and `last_hint` alongside the secret. This prevented stale state from carrying over and making the game behave as if it was still in a previous session.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

  Writing pytest cases tied directly to specific bugs — not just "does this work" but "does this reproduce the exact wrong behavior we saw." It made it much easier to confirm a fix was real and not just masking the problem. I also want to keep committing in small, meaningful chunks with descriptive messages the way we did throughout this project.

- What is one thing you would do differently next time you work with AI on a coding task?

  I would describe the bug in terms of what I actually observed in the running app, not just show the code. When I told Claude "the hints are backwards" and "we never win," it found the root causes much faster than when I just pasted code without context. Being specific about the symptom saves a lot of back and forth.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

  AI-generated code can look correct and even run without errors while still having subtle logic bugs that only show up during gameplay — like swapped messages or an off-by-one in a formula. This project taught me that reviewing AI output critically, running it, and testing edge cases is not optional, it's the whole job.
