# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  When I first ran the game, I tried to submit my guess for a number and the hint was wrong. The message for the hint kept telling me to guess a lower number, when the actual number in the Developer Debug Info was a higher number and vice versa. I've also noticed that after using up all my attempts or starting a new game that the submit button doesn't work, when you are guessing a new number. Also, I have noticed the message under 'Make a guess' does not express the correct range based on difficulty level. 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior                    | Actual Behavior                   | Console Output / Error |
|-------|--------------------------------------|-----------------------------------|------------------------|
 70     |  message supposed to say to go lower |  message suppose to say go higher |   app.py, check_guess  |
 ------------------------------------------------------------------------------------------------------------
   40   | message suppposed to say to go higher| message suppose to say to go lower|     app.py, check_guess
 ------------------------------------------------------------------------------------------------------------  
   52   |  After winning game and starting     | Submit button doesn't submit guessed |   app.py, update_score
        |  a new game, submit button submits   | number after winning and starting a  |    
        |  the guessed number                  | a new game.                          |
-------------------------------------------------------------------------------------------------------------
   20   | When selecting easy for difficulty       | When selecting easy for diffulty | app.py,  update_score
        |  level, the message under 'Make a guess' | level, the message under 'Make a |
        |  should display range from 1 to 20.      | guess' should display 1 to 100.  |
-------------------------------------------------------------------------------------------------------------
   50   | When selecting hard for difficulty       | When selecting hard for diffulty | app.py,  update_score
        |  level, the message under 'Make a guess' | level, the message under 'Make a |
        |  should display range from 1 to 50.      | guess' should display 1 to 100.  |

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used Claude as my AI tool for this project. One example of an AI suggestion that was correct was when it was fixing the high/low bug. Claude was able to change the message for hint to lower, when the guessed number was higher than the secrect number and vice versa. In my prompt, I asked AI to include #fix comments to document my work. It was not putting the comment in the right place, but I did like the description. I kept the description and move the comment to be closer to the code change. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

Whenever AI made a change, I would try to verfiy that change on the UI. I would basically replay the game to make sure it was working properly. One test I created was making sure that the text returned easy, when the range was between 1-20. It showed some more credibility for my coding so that I knew my code was working properly. Yes I did have AI design my tests by prompting it to generate tests based on the code changes I have made.   

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every time you click a button in Streamlit, it reruns the entire script from the top, so any normal variable gets reset back to its starting value. Session state is a dictionary that is not reset on rerun, so it's the only place to store values you want to keep, like the secret number and score. I saw this directly when the "New Game" button forgot to reset one value in session state, which quietly broke the Submit button on the next game.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to reuse is writing down bugs in a reproduction table before asking AI to fix anything, since it gave the AI a specific target instead of a vague "fix the game" request. Next time I work with AI on a coding task, I would ask it to run the test suite right after each fix instead of waiting until the end, so I catch regressions sooner. This project changed how I think about AI-generated code because I saw it can look complete and still hide small logic bugs, so I can't just trust that it works without reading and testing it myself.
