# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  The hints are backwards when putting a number higher then the secert it tells us to go lower then putting a number below the secret it still tells us to go lower 
  the diffuclity is wrong hard gives less of a range then normal 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| | | | | if value is less or say less| invsered| if value is lower the number it says go lower 
| | | | |new game resets|  history stays the same| history from previous game 
| | | | |diffuclity changes value|value does not change| value would be greater then what the diffuclity range allows

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
cluad code
Claude code 
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
the ai suggested a correction on "Check_guess" function  by suggestiong to fix the if statement if guess>secret return to high else return too low I check this but throwing in large values of numbers that are both above and below the actual number to see if anything would brake it.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
Testing with values that could brake the program and seeing the output
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  the check guess function fix by throughing numbers way above the secret one to see if its fixed 
- Did AI help you design or understand any tests? How?
no I did not use AI to help desgin or understand any test

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
streamlit is a way of displaying a python program in the form of a website it help with checking errors and viewing the site before being fully deployed the reruns is when the user does something in the site and gets updated on strimlit  

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  the thing I would take from this project is prompting strategy as its very helpful to have the ai parse through the code to give me an idea of where the issues can lie  
- What is one thing you would do differently next time you work with AI on a coding task?
not do everything for me but tell me where my search should begin when dealing with issues
- In one or two sentences, describe how this project changed the way you think about AI generated code.
I am still not a huge fan of having AI write entire projects for me but it has helped me look in specific functions where the issues could be as well as creating boilerplate code when starting a project.
