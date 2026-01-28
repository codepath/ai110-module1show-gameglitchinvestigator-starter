# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
 The game started off inoperable, being unable to allow the user to get any result but "Go Lower", the issue was that the logic in the original code for displaying the go higher or lower was backwards.  Another big issue was that the user was essentially unable to start a new game after that bug was fixed, if you won the guessing game the game would be unable to run any further even if you changed the difficulty or pressed the new game button.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion you accepted and why.
- Give one example of an AI suggestion you changed or rejected and why.
The AI Tool is used is Claude Haiku 4.5.  One of the changes that it suggested was to modify the difficulty range, the reason why this is a problem is that even on some of the other difficulties, it would display Guess a Number without going into detail as to what the dificulty range is.  It suggested that there was an issue with the scoring system and thats when I found out that the user would get bonus points if they got Too High on even attempts which is a balancing issue so from that suggestion I was able to fix the logic.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
The way I apporach debugging is by slowly testing out features in the app and then making adjustments to the code as I see the errors within the application. Everything is done manually so I can visualize the issue then search for the line of code where the issue is present. One of the issues I found from testing the application manually was that you could not proceed after winning. AI did not help me design any the tests I tested solely manually.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?
The secret number kept changing likely because there was an issue with the codes state where it would randomly generate a secret number.  I would describe Streamlit as a visual way to view how your code is working with your app development with the reruns happening live as you continue coding.  I made a change with the st.session_state where if the secret number is not equal to the variable the secret for the session that the player is currently playing is a random intiger in a low to high range that changes depending on difficulty making a safe guard and guarenteeing that a secret number is only generated once.


---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
I think the manual testing is very helpful, being able to see whats going on and problem solving by yourself is not only gratifying but fun. I'll definitely be using this experience as a reference point for all other projects in the future. I wouldn't change anything with how I used AI as it really helped with ironing out logstical errors within the code and aided in making the player experience the best it could be.