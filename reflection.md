# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The game looked fine upon first glance. I did not notice any bugs when I first ran the game. 

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  
The first bug i notoiced when I ran the game was that no matter what number I put in the hint stayed the same. Additionally, even if i put i a number beyond the guessing range the hint remained the same.

The second bug I noticed was that the new game button does not work. Once you run out of attempts the banner telling you that you ran out of attempts pops up and says to start a new game, however when trying to start a new game your attempts do not reset and you can not start a new game. 

The start new game banner remains even after starting a new game. 

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

-I used copilot in vscode. 
-One suggestion I accepted from Copilot was to correct the hint comparison logic in the guessing game. The original logic caused the same hint to display regardless of the user’s input. Copilot suggested fixing the comparison and ensuring the secret number and guess were treated as numeric values, which allowed the hints to update correctly based on the user’s guess.
-One suggestion I modified was related to resetting the game when starting a new round. Copilot initially suggested resetting the game with a fixed number range, but I adjusted it so the secret number resets according to the current difficulty level instead. This kept the game behavior consistent with how difficulty is handled in the rest of the project.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I re-ran the app to test if the errors were fixed. I tested the game by playing it first entering 1 to see if it would accuratly hint to go higher, then by entering 200 to see if it would accuratly suggest going lower. When those two tests worked i continued guessing till i ran out of guesses. 
To test the other erros of the baner and new game button not working I ran out of guesses and clicked new game. This time a new game started and the banner went away meaning the bugs were resolved. 
The copilot ai helped to resolve the identify the errors i described as well as explaining what was causing the errors and suggesting a way to resolve the error. 

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret number kept changing in the original app because Streamlit reruns the entire script every time the user interacts with it, like clicking a button or submitting a guess. Since the secret number was being generated at the top of the script, it was recreated on every rerun instead of staying the same. Streamlit reruns mean the app refreshes its logic, but session state is how you keep important values saved between those reruns. I learned that storing the secret number in st.session_state is necessary so it doesn’t reset every time the app updates. Once I moved the secret number into session state and only created it when a new game starts, the game behaved correctly.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to reuse is testing features step by step instead of assuming fixes work, like manually testing edge cases and expected behavior after every change. In the future, I would be more intentional about questioning AI suggestions, especially when they introduce hard-coded values that don’t match my project’s design. This project helped me realize that AI-generated code isn’t always correct or complete, but it’s very useful for debugging and explaining why something is broken. I now see AI more as a teammate that helps me think through problems rather than something that just gives me the final answer.