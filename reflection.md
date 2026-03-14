# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

It was a guessing game 

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
I initially entered 50 and it told me to go lower. The correct number was 90.
It also prompts you to press enter to submit your number but it doesn't work. 
New Game button does not work when you reach the end of the game. 
I entered 90 and it told me to go higher, so the logic must be backwards.  
  (for example: "the hints were backwards").

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Copilot in VSCode for this project 
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
I didn't ask for any suggestions I noticed what was wrong and asked the chatbot to fix it. 
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I manually tested the feature on the app
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  I manually tested the app to make sure that I was able to press enter and the counter went down by one. 
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
The function logic was not correct 
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
The core mechanism by which the application updates its state and display. 
- What change did you make that finally gave the game a stable secret number?
I changed the logic for the function that controlled the secret number. 
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
writing prompts that fix the logic with the initial prompt. 
- This could be a testing habit, a prompting strategy, or a way you used Git.
In the future I will have the chatbot create tests. 
- What is one thing you would do differently next time you work with AI on a coding task?
In the future I will have the chatbot create tests. 

- In one or two sentences, describe how this project changed the way you think about AI generated code.
I see the benefit of using AI to help you debug and understand code that I didn't
write. 