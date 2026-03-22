# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

 The game looked fine, and there was no error when I ran the game initially. After testing the program, I found out that the level logic is broken. For example for level "easy" the program should only suggest numbers between 1 - 20, "Normal" 1 -50 and "Hard" 1 -100. The second bug I noticed was with the feedback logic where The secret is larger than the guess and the feedback should be to go higher, but it says go lower or vice versa. The third bug is with scoring system. 
---

## 2. How did you use AI as a teammate?

Copilot: I wanted to fix the feed back message "GO Higher" or "GO LOWER". And AI was suggesting that if guess > secret I should tell the player to "GO Higher" which is worng it should be "GO LOWER". So, I fixed to say the other way around. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
Yes, I asked the AI to write some test cases for the features updated. for each part of the program, and I checked the result they returned. I also played the game and tested each feature input, output.
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
