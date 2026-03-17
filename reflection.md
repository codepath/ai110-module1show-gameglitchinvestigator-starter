# Reflection: Game Glitch Investigator

1. What was broken when you started?

- What did the game look like the first time you ran it?
  - The application looks like a simple game, the ui isn't as caputring as it could be and there are definitly major bugs that affect the gameplay of the application.
- List at least two concrete bugs you noticed at the start(for example: "the hints were backwards").
  - Invalid inputs are counted against attempts, depending on the requirements this could be the intended function of the application (image 000)
  - The game does not allow you to get a perfect score, with the first guess always being counted against the final score.
  - We need deductions to only for wrong answers and not correct answers. (fix) For the first guess being a correct answer we should assign that the maximal score and the lowest score should be capped at a minimum of zero and not negative values which can be seen in other screen shots
  - We accept the decimal eq. of the integer of the secret/win value (image 001)
  - Once you win the game does not allow you to refresh the right rather than pressing new game
  - The history of a previous game's state is saved
  - Even when we try to change the game difficulty the previous (firsts) game's states is still visible (image 002)
  - Contradicotry hints are offered, when your guess is too low it will suggest you to go lower, and vice versa if your guess is too large (image 003)
  - The application allows for decimal value in which if the value were to be floored, it would be the secret value (image 004)

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used claude code in the terminal and antigravity. Antigravity was for tangental questions about random whys, for example setting up a python env to run the project in with the neccary libraires, etc and claude code was for generating thorughouput with understanding the codebase as well as understanding bugs that I had encountered and those that I hadn't seen. I was able to cross refrence my findings from the runs of the game i had with its knowldge of the codebase and for the stem for various issues
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - Invalid inputs counted against attempts (app.py:148) st.session_state.attempts += 1 runs before parse_guess is called. So even if the input is blank or non-numeric, the attempt counter already incremented. I was able to use my reasonings and following the surroding codeblocks and compntents of that line to conclude that was the case
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - Rather than inccorrect it seems like the agent honed in to closely to the issue and forgot to suggest the overarching design of the function parse_guess(). This function could be written in a more conccise and straignt for fashion one for future developers but also debugging there is a lot unneccary filler code which doesn't inherlty add to our applicaiotn

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)and what it showed you about your code.
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
