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
| Guess 60 when the secret is 50 | Show a "Too High" hint | The app shows "Go HIGHER!" instead, which is backwards | none |
| Guess 40 when the secret is 50 | Show a "Too Low" hint | The app shows "Go LOWER!" instead, which is backwards | none |
| Open the app, then click "New Game" and inspect attempts | Attempts should reset consistently to a fresh starting value | The initial attempts value and the reset value do not match, so the attempts-left count is inconsistent | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Copilot during the refactor and debugging steps, and I also used it to help explain the Streamlit state bug and the guessing logic. One correct suggestion was to move the game logic into `logic_utils.py` and keep the Streamlit UI in `app.py`; I verified that by importing the helpers back into the app and confirming that `pytest` passed. Another correct suggestion was to use session state for the secret number and reset it in one place, which I verified by checking that the secret and attempts stayed consistent after reruns.

One misleading suggestion was the original idea that the hint logic was just a display issue. That was not enough by itself, because the deeper problem was that the app mixed UI code and game logic and also had inconsistent state resets. I verified that by running the tests and by manually checking the debug info while clicking Submit and New Game.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was really fixed when both the app behavior and the tests matched the intended logic. For example, I checked that a guess above the secret showed the lower hint, a guess below the secret showed the higher hint, and the score changed in a predictable way. I also ran `pytest tests/test_game_logic.py` and confirmed the helper logic passed all three tests.

The most useful test was the `check_guess` test file, because it made the hint bug obvious and forced the comparison logic to be simple and direct. AI helped by suggesting that the logic should be separated into small functions so each piece could be tested on its own instead of only through the Streamlit UI.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

I learned that Streamlit reruns the script from top to bottom every time the user interacts with a widget, so regular variables do not automatically persist. Session state is how you keep important values, like the secret number, score, and attempt count, alive across reruns. I would explain it as: Streamlit rebuilds the page on every click, and session state is the notebook where you store what should survive that rebuild.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to reuse is breaking a problem into small helpers and testing those helpers before trusting the full UI. That made it easier to isolate the bug in the guessing logic and confirm the fix with `pytest`. I also want to keep writing down reproducible bugs early, because the bug table made it much easier to stay organized.

Next time, I would ask AI for a more targeted plan sooner instead of accepting broad suggestions at face value. I would also verify each change with a test or manual check before moving on to the next issue.

This project made me think of AI generated code as a rough first draft, not a finished solution. It can help move quickly, but I still need to inspect the logic, test the behavior, and decide which parts are actually correct.
