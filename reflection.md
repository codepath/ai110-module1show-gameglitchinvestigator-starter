# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  At first it just instructed me to guess a number, the input box was not there. only when I reloaded, the input box for guessing the number was there

Document at least 3 bugs you found. Add rows as needed.

| Input                                    | Expected Behavior | Actual Behavior | Console Output / Error |
| ---------------------------------------- | ----------------- | --------------- | ---------------------- |
| Guessed 50 when the secret number was 90 | Go Higher         | Go Lower        | None                   |

New Game Button Clicked | Game Restart | The secret number, Attemps or Score didn't Change | None

Guessed 101 | Guess Allowed | Error should be seen | None

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  -Copilot

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  A bug that restarting the game when clicking "New Game" button. The AI suggested that the core logic issue was that it reruns the app but doesn't restart the st.session_state.status so if the previous game ended as won/lost, the app immediately hits the stop condition and looks unchanged.

Copilot fully reset the game state, secret, attemps, history and score when clicking new game button. Copilot had tested with pytest -q.

I verified by running the app and making sure that when "New game" was clicked, it reloaded

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

When fixing the high/low bug, the AI just suggested that the primary reason for this error was guess > secret returns "Go Higher" when it should have been "Go lower". Whereas, guess < secret returns "Go Lower" when it should have been "Go higher".

This was correct, but it was not the only fix in the code that was needed to fix the bug.

The error was still there when I ran the app.

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  I scan through the pytest to check whether the pytest made sense.
  I ran the test and made sure that all the cases passed
  I checked through UI aswell.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  I clicked the New game button in the UI.

  I checked if the secret = (new secret), attempts = 0, history=[] and score=0 had restarted when the button was clicked.

- Did AI help you design or understand any tests? How?

---

Yes, I wasn't sure how to design a test for new game as it was a button click.
AI Helped me design the button test.

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Streamlit "reruns" literally reruns the whole page line by line everytime the user interacts with the code including clicking a button, moving a slider, typing in a box etc.

  Since you rerun everytime a user interacts, the variable also starts fresh. Forexample, it you want to count how many times a button was clicked, you would do count = 0, count +=1. But when the button is clicked, the count refreshes to 0. State acts as a memory of the variable.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
    Adding the file name and making sure that chat also verifies the bug has been fixed.

- What is one thing you would do differently next time you work with AI on a coding task?
  I would be more precise with my prompts. I want to understand where exactly the error is and what should be done.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  I stopped blindly trusting llms. I will not just state the bug but also mention where the bug is and understand why the error is occuring.
