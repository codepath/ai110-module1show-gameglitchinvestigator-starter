# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

|          Input            | Expected Behavior | Actual Behavior       | Console Output / Error |
|---------------------------|-------------------|-----------------------|
|          New Game         | New game starts   |   Nothing happens     |
|       Range is wrong      | Range: 1-100      |     any number        |
|   Difficulty is wrong     | Hard is difficult |  Hard is easier       |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used Claude as a tool to fix the issues of the program. One of the main issues was that "New Game" was not working after the game was finished. The AI was correct on its suggestions. One thing I will check about AI next time is how all fixes were automatically accepted, so I will specify more on next prompts.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

The way to check this was to test them myself through running the game. So, I ran the streamlit command again, and tried all bugs, which were succesfully fixed along with other bugs I didn't see yet.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

--- Streamlit works as a refresher that runs the script again , while session state remembers things between reruns.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

Next time, I will modify my prompts to have more control over changes, put more comments on where I want modifications, and decide before important changes to avoid losing control over improvements. 