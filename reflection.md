# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The game was is dark mode and it looked like a page that gave me a box to submit a number in to guess a number between 1 to 100 with the number of attempts I'm allowed
- List at least two concrete bugs you noticed at the start  
1. I was getting inconsistent hints, they would tell me to go higher when I was already above the target number, I was expecting it to tell me a proper estimate. 2. Another thing I noticed was when I pressed enter nothing would happen even though I was expecting it to tell me if I need to go higher and lower and update the page with the number of attempts left

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

|    Input   | Expected Behavior | Actual Behavior | Console Output / Error |
|------------|-------------------|-----------------|------------------------|
| guessed 60 | too high hint     | too low hint    | the hint is incorrect
| guessed -10 and pressed enter | a hint| nothing happened | the program didn't run when I pressed enter |
| guess -1000| updated history | history updated after clicking twice | history didn't update immediately|

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Claude in my VSCode
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
An example of an AI suggestion that was correct was the wrong hint being used when the number was greater or lower
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
The AI noted that upon form resubmission that the guess turns into a string; because I wasn't aware of the full logic it suggested I changed more than I needed to when I could've just converted it into an int before comparing it but it knew that as well

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
