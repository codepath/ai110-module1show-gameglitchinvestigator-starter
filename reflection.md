# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The game looked great when I first ran it
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  It kept saying guess higher when I already guessed 100
  It kept saying guess lower when I already guessed 1
  It told me to go higher when I needed to go lower
  It told me to go lower when I needed to go higher 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 3| Go higher| Go lower| none|
| 23|Go lower | Go higher| none|
| 15| Go lower| Go higher|none |
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

IT suggested to change the comparisons wehn checking greater or lower than the secret word and to change the hint output after each guess. AFter fixing that, the output was correct. I veroified th result by testing it a few more times along with edge cases as well. 

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

the AI suggested that there was an error with show hint button when teh player won teh game as well, but I checked the game and it was not actually an error. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I tested it multiple times with different types of input eachtime, along with edge cases like 1 and 100/

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

One manual test I did was when teh secret number was 18, I tried entering numbers lower an dhigher than that to see if it was givign the correct hint. And it did. This showed that the code is workign now. 

- Did AI help you design or understand any tests? How?
Yes, AI helped me design all the test cases to make sure all the fixes we made were working.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
