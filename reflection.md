# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  It looked like a normal guessing game, but there were alot of bugs. For example, when the guess was too high it would say go higher even if you had to go lower and the opposite was true for the opposite. The new game button also didn't work and the hint doesn't show. 

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
---

I gave it a list of the bugs I caught, and then asked it if I missed any. I then put all the bugs in bugs.txt for it to fix. I used claude code to do all of this. 
It didn't catch all the bugs. It shows attempt left = 1 but the game is over. So I had to make sure it did everything correct. 

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---
I used ai to make test cases and and then I ran them. I also quickly walked through the app to make sure. I understood the tests by reading the code because I'm used to reading test cases. 

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---
Streamlit re-runs the script every time there is an interaction and the secret number was at the top so it changed every time there was an interaction

we added 
  if "secret" not in st.session_state:
      st.session_state["secret"] = random.randint(low, high)
to make it work. 

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

I want to use AI to make more test cases. It's something that I don't really do. I also want to use it to find the bugs more and document the bugs. Next time I work with AI, I will double check the outputs are correct as well as make it explain why it does something. 
It didn't really change the way I thought about AI generated code. I have been coding with Ai for a while now. 
