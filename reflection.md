# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

  At first look it was normal, even though the developer debug info section caught me off gaurd because it was open to the player to see. Other than that I noticed that when you press enter for what I suppose is submiting your answer it doesn't and the hints are broken. I also tried to generate a new game  but it did not work so I had to refresh the page every time I won and the range of difficulty is also broken. 

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  -- The hints are backwards
  -- Accepts negative numbers
  -- The difficulty attemps available is wrong, having easy being more difficult than normal, meaning less attemps available
  -- Ranges of difficulty might be inverted with normal havng a bigger range than hard

  Other bugs found after asking AI about code:
  -- The message "Guess a number between 1 and 100" always stays the same even after chaging the difficulty mode
  -- New game does not respect the difficulty so the secret number is always chosen between 1-100


## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  I used a mix of the Copilot Chat in VS Code and Claude on my web browser. I mostly worked with the Copilot Chat to help with bug fixes and the refactoring. On the other hand, I used Claude fro any problem I faced with running the program and installing dependencies. 

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result). 

A correct AI suggestion would be when I asked it to help with refactoring and update the inputs. It changed thing correctly and I double checked for any mistakes or redundant information. For another bug fix the AI did changes correctly and updated the tests and code depending on the changes I suggested like how to handle negative numbers and cero.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).


A misleading AI suggestion was when I asked to create the test to verify if the hints were working right it created another file and a new test that were redundant. I verified the result by double checking the code and asking the AI if the new test was necesary along with the new file. After the AI deemed it unnecesary it deleted them. Another incorrect suggestions was that the AI suggested to delet part of a code that was still needed and broke the program but I catched the error and fixed it.


## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  To decide whether a bug was fixed or not I would run i ton pytest to verify if it passed the tests created and manually check the game. Most times I would doubel check manually because the tests were mostly created by AI. After many tries and confirmation that the code was working, plus brainstorming for possible errors that could happen, I considered a bug fixed if it passed the tests created and worked manually.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

  Most of the tests I validated manually but while doind so I found some minor issues. For instance, the game accepted negative numbers and cero so I changed that logic with Copilot Agent. This way when the players input is a negative number o zero the game will not accept that input and instead will show a message sayeing "Guess must be a positive number greater than zero". 

- Did AI help you design or understand any tests? How?

  The pytests where mostly designed by Copilot Agents because I'm more of a munual tester. However, I was having problems understanding the logic behind the scores and AI helped me understand both the tests it created and the logic of how it owrked. This way I was able to provide options and possible suggestions to changes in logic.


## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  I would explain Streamlit reruns like a robot witout memory because one you ask you get an answer an then they forget all about it or change. Then I would explain the session states like the memory of the robot because a session state remembers the information while you are using the app. This way the both work together, one runs the program and the other makes sure to remember what happened.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

  I think one strategy I want to reuse in being methodic and organized with finding bugs and 'marking the crime scene". I believe this helpend me a lot when fixing the bugs this way I don't have to constantly memorize what to do next because it's already there. I found this strategy more effective and less time consuming.

- What is one thing you would do differently next time you work with AI on a coding task?

  I think one thing I would do differently is test handeling. I want to try to create the tests on my own first and then double check with AI this way I don't feel like I can't handle testing well. Overall, for next time I want to use AI as a backup for testing instead of heavily rely on it.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

  I found AI generated code to be effective when given the right amount of information. I also consider that it helped me learn more about effcient ways to handle testing and avoid redundant code.  