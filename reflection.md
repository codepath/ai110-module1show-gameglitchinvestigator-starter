# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it? sidebar caption Attempts allowed and the st info Attempts left are inconsistent, 8 and 7 respectively and at first run should be 8 and 8.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards"). 
  1. sidebar "Range MIN to MAX" and the info "Guess a number between" are out of sync when the user changes difficulty in sidebar  
  2.accepts out of range guess or does not show an appropriate messsage if the input is out of range.
  3.new game btn doesnt rest after win

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| select easy difficulty | Text updates as Guess a number between 1 and 20 | Text does not update and continues to display Guess a number between 1 and 100| Guess a number between 1 and 100 |
| 200 | checking guess and return "Guess is Out of Range | checks guess and returns Go LOWER! | Go LOWER! |
| Click New Game btn | Console page looks the way when user first runs it | Fails silently | Returns You already won. Start a new game to play again. |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude
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
