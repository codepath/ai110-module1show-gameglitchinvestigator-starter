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
  - I used Claude agent in VS Code and asked clarifying questions of code details/errors and functions to ChatGPT
  
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - ChatGPT suggested to use ValueError instead of Exception on the parse_guess() function, since I am aiming to not allow the system to accept inputs that are not already whole numbers - or string inputs that are directly parsed as int. 
  - It did not suggest any code specific edits since I was simply sharing m,y thought process on while debating if it was viable or not. However, claude did change the code by adding ValueError instead of Exception
  
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - When I was looking at the update_score function, I noticed it originally only checked for two of the four possible messages, hence updating the score poorly. After sharing this issue with the AI agent it told me that anothger "error", +5 were added ONLY when the attempt number was even, which I verified as untrue information while re-reading the code section, for it appears to follow a logic: when the attempt number is even it adds 5, when it is odd, it subtracts 5.  


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I tried it in the website as well as checked teh tests and if it made sense 
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
