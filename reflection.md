# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

  When I first ran the game it looked very simple to play. Each button was detailed and the play area is clearly defined. It was great to see that the Developer Debug I played a few games and noticed the following bugs

  1. When a user guesses with the "Show hint" option selected, the display "Go LOWER/HIGHER!" does not work properly. It repeats what the first message displayed throughout the game. I expected the appropriate message to display for the appropriate guess. 

  2. The "Range" for difficulty is not set properly. Normal should be 1 to 50 while Hard should be 1 to 100 and Easy should be 1 to 20. It is expected that the ranges should be match the difficulty setting.

  3. User history does not display properly. It seems that the first attempted is not recoreded but the remaining history is recorded. It is expected that all guesses are recorded properly.

  4. The number of guesses displayed is 8 but only 7 are allowed and recorded. It is expected for all 8 attempts should be given to the user.  

  5. The "New Game" button does not reset the history or allow the user to play the game again. It is expected that the user history and attempts are reset and the user is allowed to play again. 

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
