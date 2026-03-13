# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

- It ran well without difficulty, all features seemed to function correctly at  
first glance
- The range for normal mode is higher than the range for hard mode which defeats the purpose of it being 'hard'.
- The game does not reset when user starts a new game
- Hints are incorrect, telling the user to pick a lower number even tho it is already lower than the secret number, and vice versa for higher numbers.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- I used Claude

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- it suggested to reduced the range for normal and increase the range for hard, which is correct.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
- none
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
we ran test cases and then i tried them on the app itself. 
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- I ran test_string_secret_type_mismatch_too_low, calling check_guess(9, "10"). It exposed that the original fallback used str(guess), so 9 became "9", and string comparison makes "9" > "10" true — flipping the result to "Too High" when it should be "Too Low." This showed me that type bugs can silently corrupt logic in a way you'd never catch just by playing the game. Claude helped design the test by identifying the exact input that would trigger the edge case.

- Did AI help you design or understand any tests? How?
- Yes
- I described the bugs — you told me the hints were backwards and the game behaved inconsistently depending on the attempt number.

Claude read the code — I analyzed check_guess in app.py and identified two specific failure modes:
The hint messages ("📉 Go LOWER!" / "📈 Go HIGHER!") were assigned to the wrong branches
The TypeError fallback used str(guess) instead of int(guess), which causes Python to compare strings lexicographically instead of numerically

Claude picked targeted inputs — for the type bug, I chose check_guess(9, "10") specifically because "9" > "10" is True as strings (first character '9' > '1'), which would flip the result from "Too Low" to "Too High". That's the exact case that would pass silently without a test but fail in a confusing way during gameplay.

The tests were written to be regression tests — meaning they document the wrong behavior so if someone reintroduces the bug, the test fails immediately instead of you having to play the game to notice it again.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
-- Every time i clicked "Submit", Streamlit re-ran the entire app.py script from top to bottom. The line secret = random.randint(low, high) was outside of any session state guard, so it generated a brand new number on every rerun — making it impossible to ever match your guess.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- Imagine every button click refreshes the whole page from scratch, like hitting F5 — all your variables reset. `st.session_state` is like a sticky notepad that survives those refreshes. Anything you save to it stays put between reruns, so the game remembers the secret number, your score, and attempt count without losing them on every click.
- What change did you make that finally gave the game a stable secret number?
- Wrapping the secret generation in a session state check: `if "secret" not in st.session_state: st.session_state.secret = random.randint(low, high)`. This ensures the number is only picked once at the start, and every rerun after that just reads the already-saved value instead of rolling a new one.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
