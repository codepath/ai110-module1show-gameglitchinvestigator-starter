# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  I noticed the hints were incorrect

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  The hints lied to me
  The scoring system was confusing and not properly implemented
  New game isn't working as intended
  Attempts left could be wrong

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
| Guess of 10 | "Go HIGHER" hint | "Go LOWER" hint shown | None |
| Guess of 5 | "Go HIGHER" hint |  "Go LOWER" hint shown | None |
| Guess of 5 | "Go HIGHER" hint |  "Go HIGHER" hint shown | None |
| Guess of 20 | "Go HIGHER" hint |  "Go LOWER" hint shown | None |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
* Claude Code

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
* The hint functionality properly implemented "Too High - Go LOWER, Too Low - Go Higher". It was verified by testing the functionality in the app

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
* I told it to review and point out the bug in the check_guess function. After reviewing, it recommended more lines of code and complex logic implementation

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
* The check_guess function bug was fixed by testing both manually and using pytest

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  * Guess above the secret -> "Too High", and the hint should point LOWER

- Did AI help you design or understand any tests? How?
  * I told it to design a pytest testing all possible conditions that the function should expect me

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
