# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

### What did the game look like the first time you ran it?
The game looked like an ordinary Streamlit program, with the primary elements being the sidebar on the left-hand side and the center console all having similar fonts. There were several buttons with supposedly different functionalities. Lastly, there were a couple dropdowns and input fields in the center console.


### List at least two concrete bugs you noticed at the start  
- One of the primary bugs I noticed was how useless the hints were ("Go Higher!"), as they didn't legitimately help.
- The "New Game" button would not actually function (I had to refresh the page in order to play again).

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
  *clicked "New Game"*, Refresh the page with a new game, Nothing, Game over. Start a new game to try again.

  50, Too High, Go Higher, N/A
  25, Too High, Go Higher, N/A
  75, Too High, Go Higher, N/A
  87, Too High, Go Higher, N/A
  94, Too High, Go Higher, N/A
  97, Too High, Error, Out of attempts! The secret was 20. Score: 5
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I am utilizing Codex (ChatGPT) for this project.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
Codex suggested reworking the check_guess function and place it into the logic_utils.py file to properly run the project. I verified this worked by making sure all of my manual test cases worked, and being prepared to undo any agentic changes.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
An example of the AI suggesting something I did not accept was during the creation of the test file. While making the test file, the agent did not account for importing certain functions and libraries, which resulted in the program not being to run at all. As a result, I obviously rejected the change, and clarified additional boundaries to assist in the proper generation of a test file.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I would decide the bug was really fixed when the subproblem that I was focused on would no longer exist, even if it meant that it resulted in a new bug. In other words, as long as the original problem I was trying to solve doesn't exist anymore, I considered it solved/fixed. At a grander scale, this is not the ideal solution, but by viewing it in this manner, I am able to mentally capture it as multiple mini-problems rather than one large issue.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
One test that I ran was through the pytest. It would iterate through a range of values, and based off of that, it would provide the respective result (whether it passed or failed). By changing the ranges and other factors, I was abel to verify that the pytest actually worked (after a bit of debugging).

- Did AI help you design or understand any tests? How?
The AI did help me design and understand the tests. There were some aspects where the implementation would confuse me, specifically why a certain loop was called. By asking the agent, I was able to fully deduce what was going on step-by-step.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
From what I'm aware, Streamlit will rerun the entire file whenever someone interacts with the project. On the other hand, the session state will store values across reruns for a user's session, making it slightly different from reruns. Overall, it is a simple Python framework that speeds up the process by avoiding any web development components.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
I think one stratgey from this project that I want to reuse in the future is the ability to be extremely specific. I think providing the general files and applications is easy, but the more specific I am, it simply represents how knowledgeable I am of the problem. If I am able to thoroughly able to explain the problem, then I am essentially halfway to finding a solution with the help of the agent.

- What is one thing you would do differently next time you work with AI on a coding task?
I think one thing I will do differently next time I work with AI on a coding task is to initially summarize the entire codebase to fully understand the purpose and location of every aspect. By understanding the location and the meaning of all the functions in the project, I think that would assist in understanding where bugs may exist, as well as the expected outcome. This would also streamline my work process.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
I think this project was a simple test to see how I interact with the agent at a surface level. It is helping me emphasize the efficiency of working alongside an agent, rather relying on it. I believe my work in the future will be significantly more efficient with AI.