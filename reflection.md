# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
    The game looked very basic and simple, it didnt seem to complicated.
    I would like the UI to be more engaging but for learning purposes, I think
    the UI is built like this so the programmer can have a simple screen to test
    the game and the bugs.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
    1. When I entered a number like 2 I and pressed 'Submit Guess' I was prompted
    with 'Go Lower.' So with that I changed my number to 1, and I got the same response. This is a bug due to the fact we are only able to from 1-100, we are unable to go lower. I can not go any lower than 1.

    2. The secret number is revealed to the user

    3. When I won the game and pressed 'New Game', it didnt clear my previous guess and did not allow me to win again because I won previously. I got the message "You already won. Start a new game to play again.", in which is untrue because I have already attempted to press 'new game' to play again.

    4. When you go between the levels they each have their range of values a user can input. Easy (1-20), Normal (1-100), and Difficult (1-50), however when I choose to attempt the easy level the secret number was 67. But that is impossible because the user can only guess from 1-20.



**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|   2   |      Go Higher    |     Go Lower    |       No Error         |
|   1   |     Go Higher     |     Go Lower    |       No Error         |
|   60  |    To Win.        |     Won.        |You won! The secret was 60  |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
    I used Claude

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
    The AI informed me the function get_range_for_difficulty values were a bit off. I did notice that too, I havent altered the code but I have a note in my mind to look at that and see what I can do to fix that issue.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
    I was having troubling running pytest in the terminal so the AI suggested I use python -m pytest, where I got an error basically stating I dont have python. The issue was I have python3 not python so the command was not correct.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
    When I tested it during running the game. I altered the ranges for difficulty levels and I seen that what I changed matched with the app. There are still changes to be made with the logic of the same but that was a simple and quick one for the time being

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
    I ran a test to check whether a guess was too low, too high or the winning guess. It showed me consistent failure so I had to look into the function check_guess and see why it was not allowing those test to pass.

- Did AI help you design or understand any tests? How?
    Yes, AI told me that the try/except was the issue and why then stated to fix the logic in logic_utils.py and when I did, I reran the code and the tests passed.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
