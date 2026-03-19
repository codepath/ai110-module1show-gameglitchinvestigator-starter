# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
When I first ran the game, it was unplayable. The hints were backwards — when my guess was too high, it told me to go higher, which pushed me further away from the answer. The game also had a secret type corruption bug where on every even-numbered attempt the secret was secretly converted to a string. On top of that, clicking "New Game" after winning still showed "You already won" immediately because the game status was never reset. 
## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude Code (Anthropic) as my AI teammate throughout this project. One correct suggestion was using a counter variable (`input_counter`) as part of the text input's key to reset the field on new game — instead of directly writing to session state after the widget was already rendered. I verified it worked by restarting the app and confirming the input cleared after clicking "New Game" with no errors. One suggestion that caused an error was directly setting `st.session_state[f"guess_input_{difficulty}"] = ""` to clear the input — the AI initially suggested this but Streamlit raised a `StreamlitAPIException` because we cannot modify a widget's session state key after it has already been instantiated on the page.

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed by both running `pytest` and manually testing the behavior in the browser. For automated testing, I ran `pytest tests/test_game_logic.py -v` which checks three cases: a winning guess, a guess that is too high, and a guess that is too low. All three failed before the refactor because `logic_utils.py` only raised `NotImplementedError`. After moving the fixed logic into `logic_utils.py` and correcting the return type of `check_guess` to return a plain string instead of a tuple, all three tests passed. 

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit reruns the entire Python script from top to bottom every single time the user interacts with the page — clicking a button, typing in a box, or changing a dropdown all trigger a full rerun. Because of this, any regular variable we set would be lost between interactions. `st.session_state` is a special dictionary that persists across reruns, which is how the game remembers the secret number, the attempt count, and the score.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.   

One habit I want to carry forward is running `pytest` early and often — having the three tests in `test_game_logic.py` gave me a concrete pass/fail signal that confirmed the core logic was correct before I even touched the UI. Next time I work with AI on a coding task, I would ask it to explain *why* a fix works before applying it, not just what to change, so I can catch cases where the suggestion might conflict with a framework's rules (like the Streamlit session state write restriction). This project changed the way I think about AI-generated code because it showed me that AI can produce code that looks completely correct and runs without syntax errors, but still contains subtle logical bugs — like inverted hints or type corruption — that only reveal themselves when you actually play the game.

