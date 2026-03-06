# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
Answer: The first time I ran it, it seems normal, the hints were there, and I was guessing normally. 
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
+ The hints were useless and it was backwards, so it was impossible to guess the correct numbers.
+ I couldn't reset the game using the button at all, so I had to manually reset the website.
+ If the user input nothing and press guess, it was still considred as a guess, and the number of attemps goes to negative.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- I use Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- For the reversed hint bug, the AI suggested that I should reverse the order of the too high-too low code, and after that the AI shows the edit it would make. I review carefully to understand what the result would be, and then once it is vertified, I accept the edit.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
- For the bug where the check_guess was still comparing the value when the user input a string, the AI decided to edit the test_logic_game function instead of editing the actual function itself. Notice this, I revert the AI's attention to the actual bug to fix.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- 2 ways, either let AI create test cases and run it, or manually go to the website and check the edge cases myself.
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
- I had a bug where the new game button did not work. After fixing the code, instead of letting the AI build two different functions to check the session state of the game, I just manually press the new game button and check it myself
- Did AI help you design or understand any tests? How?
- Yes it did, since it added comments that explain how the tests case should work and act.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- There is a specific function in the code that allow the secret number to ba randomly choosen in a certain range. 
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- The Streamlit has its own variable that help store the session state of the game. If the user finish the game, for instance, the session state should reset so that the new game can happen.
- What change did you make that finally gave the game a stable secret number?
- Adjusting the range of the secret number to be stable

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
- Answer: Aiming precisely at one single bug and then handle it, as well as creating test cases to handle the bug
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- Consider more edge cases and implementing test cases
- In one or two sentences, describe how this project changed the way you think about AI generated code.
- Sometime the AI generated code can be off-track, and it is the coder's responsibility to revert it back to the main issue