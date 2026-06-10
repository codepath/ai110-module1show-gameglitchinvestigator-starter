# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  - It looked like a number guessing game in which the users can eithert enter a guess or start a new game.
  - They can choose whether to get clues on their guesses (if the number is bigger or smaller than their last guess). 
  
- List at least two concrete bugs you noticed at the start  
  - The hints are inacurrate (when the number is smaller than the target it says to aim lower, and when it is bigger it says to aim higher when hey should hint the opposite.)
  - The target number sometimes goes out of range (higher than 100 or lower than 0)
  - The history doe snot always record all guesses, some dissappear
  - Once the game is over you cannot start a new game - the button does not work
  - Attempts start at 1 even when no submission has been made

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior   | Actual Behavior  | Console Output / Error |
|-------|---------------------|------------------|------------------------|
|   -5  | "out of range"      | "go LOWER"       |    None                |
|   10  | Add to history      | number not added |    None                |
|   20  |  "go LOWER"         |  "go HIGHER"     |    None                |

---------------------------------------------------------------------------

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

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
