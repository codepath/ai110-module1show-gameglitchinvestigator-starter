# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

When I first ran the game, the interface looked normal and allowed me to enter guesses. However, while playing I quickly noticed some bugs. The higher/lower hints were backwards, so when my guess was too high it told me to go higher instead of lower. The New Game button also didn’t reset the game properly because it created the new secret number in a fixed range instead of the selected difficulty range. I also noticed the attempt counter felt inconsistent with when the game actually ended.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used ChatGPT and Copilot to help understand and debug parts of the code. One correct suggestion from AI was identifying that the hint logic inside check_guess() was reversed and needed to return the opposite direction message. I verified this by updating the logic and running the game again to confirm the hints matched my guesses. One misleading suggestion was that the New Game bug was only related to session state, but after checking the code I realized the secret number was being regenerated using a fixed range instead of the difficulty range. That helped me understand the problem more clearly and fix it properly.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

To confirm bugs were fixed, I tested the game manually by playing several rounds and checking if the hints and attempt counts behaved correctly. I also ran pytest to verify that the guessing logic returned the correct outcomes for high, low, and winning guesses. For example, I tested that guessing 60 when the secret was 50 correctly returned "Too High". The test results helped confirm the logic was working as expected. AI also helped explain what the tests were checking and how they validated the game logic.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

I learned that Streamlit reruns the entire script every time a user interacts with the app, such as pressing a button or entering input. Because of this behavior, variables can reset unless they are stored in st.session_state. Session state allows the app to remember important values like the secret number, score, and attempts between reruns. Without session state, the game would restart every time the user clicks something. Understanding this helped me see why managing state correctly is important in Streamlit apps.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to reuse is testing small parts of my code while debugging instead of trying to fix everything at once. Running tests and manually checking behavior helped me confirm that each fix actually worked. Next time I work with AI on a coding task, I will verify suggestions more carefully instead of assuming they are always correct. This project helped me realize that AI-generated code can still contain logical mistakes. It showed me that developers need to review, test, and reason through AI code just like any other code.