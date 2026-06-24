# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it? 
The game is about guessing a number between this certain range as I ran the game on normal difficulty, so I had to guess a number in 8 attempts or I'll lose. I did toggle the developer debug info button to find any problems with the game as I entered my attempts to find the secret number. Thus, I went through all my attempts and couldn't guess the secret number, which resulted in receiving a game over message from the game.  

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  (1) Hints were given incorrectly.
  (2) The game doesn't restart.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|

| Guess of 55 | "Go HIGHER"! hint shown | "Go LOWER!" hint shown ! "None" 
| New Game | Game restarts with new secret number | Game doesn't restart | "None"
| Change from Normal to Easy | Can only make guesses in range 1-20 | The range doesn't go into effect | "None" |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

Answer: My only primary AI tool used on this project was Claude. I utilized Claude Code and the AI assistant's chat. 

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

Answer: During the project, a bug I was trying to fix was the game giving incorrect hints to the player trying to guess the secret number. For instance, the secret number is 65, the player guesses 70, and the hint provided by the game is their guess should be higher. Thus, the AI suggested to coerce the secret variable into an integer before comparing as the hints were given using lexicopgraphic string comparisons. Then, I verified the results by playing through the game where I had to guess the secret number of 64, and I guessed the number 10 to be given the appropriate hint, which is to go higher, to confirm the AI suggestion being correct. 

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

Answer: During the project, a bug I wanted to fix was adjusting the game's difficulty to provide the correct range of numbers for the player to guess. Claude suggested to make changes to the function where I needed to ensure the ranges reflect the chosen difficulty for the game. For instance, I changed the range to be wider whenever the player sets the game's difficulty to Hard so that the player is guessing a number from 1 through 200. However, the AI's suggestion to fix the bug was misleading because the AI's intentions were to make the ranges wider as the game increases in difficulty, but the difficulty options, primarily Easy and Hard, weren't working as intended. In addition, I can verify the AI's suggestion was misleading because I played two games where I had the difficulty as Normal and Easy, and the game with its difficulty set to Easy had a secret number, such as 40, that wasn't in the range of 1 through 20. 
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

Answer: I decided a bug was really fixed whenever the change is reflected in the guessing game, such as an aspect of the game working as intended like the higher and lower hints. 

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

Answer: I ran a test for the game hint bug fix by generating a pytest case to know whether the hints were being given correctly based on the player's guess. The pytest cases failed because the guesses for the test were emitting the hints incorrectly despite the coerce change made to the secret variable. Therefore, the tests confirmed my uncertainity for the check_guess function when I realized the issue with the code in this function, and that was to manually change a comparison sign to get the hints working as intended.  

- Did AI help you design or understand any tests? How?

Answer: AI did help me design in a way where it provides me with a plan in finding bugs to execute and verify my quick fixes for more cleaner, competent code. Claude was providing design plans for each bug fix by generating test cases that failed to confirm the fixes needed in certain parts of the code for the final product to work as intended. 

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Answer: I explained to a friend that Streamlit "reruns" and session state is comparing the experience of using a search engine whenever your curiosity peaks for learning a new topic, or reviewing a older topic. For instance, you can constantly open the Google app on your phone throughout the day and notice something that remains the same, which is your search history. In addition, you can search something about soccer on Google, close the Google app to open it again, and you'll realize you can search the same soccer topic again as a means of having an application remember what had happened previously, which is my friend searching a soccer topic.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

Answer: I want to use the prompting strategy utilized for this project in future work because my prompting strategy showcased how important example scenarios to my AI tool to communicate what would be the most efficient fixes to repair any bug or problem to get the same results found in the test cases and the example scenarios.

- What is one thing you would do differently next time you work with AI on a coding task?

Answer: I need to provide better context and specific details the next time that I work with AI on a coding task so that I avoid being mislead to a stop in my thought process or faced with a bigger problem. Thus, I need to make adjustments to acquire a more efficient prompting strategy when utilzing an AI tool for a coding task. 

- In one or two sentences, describe how this project changed the way you think about AI generated code.

Answer: This project did change my perspective on AI generated code with how organized and clean it looks, but it's the user's responsibility to ensure AI generated code is getting the bare minimum done with any changes made if necessary. 