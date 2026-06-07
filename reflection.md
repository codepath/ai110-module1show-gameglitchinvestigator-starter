# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

<!-- - What did the game look like the first time you ran it? -->
<!-- - List at least two concrete bugs you noticed at the start   -->
  <!-- (for example: "the hints were backwards"). -->

After loading the application, I immediately noticed several issues. 

1. Although the settings panel stated that normal mode allowed 8 attempts, the game screen explained that I only had 7 attempts left. The debug info panel also confirmed that 1 attempt was used purely from loading the game. I expected the application to load with attempts at 0 with 8 guesses remaining as I hadn't guessed yet.

2. After changing the game's difficulty, which should adjust the range of numbers allowed, the "secret" number was never reset or adjusted. I found myself in situations where a normal mode game would load with a value like 78, and switching the hard mode would maintain the non-allowed secret number of 78. I expected the game to automatically be reset (i.e. new secret number, reset attempt count, clear history) once the game mode changed.

3. The "new game" button would reset the attempt count but leave the guess history. This limited my guesses as once I reached the game mode's max count in the history panel, I was given the "Game Over" banner. The game did not take my attempt account into considering. I expected the "new game" button to clear the history along with the rest of the game data.

4. Submitting a blank guess only correctly prevents submission the first time. For all subsequent submissions, the attempts counter increases and the submission is added as "" to the history log. At all times, the "Enter a guess" warning is present. I expected all blank submissions to be ignored and for the banner to be displayed.

5. The hints are reveresed. Any guess lower than "secret" is guided lower while any guess higher is guided higher. I expected the hints to be accurate and guide me towards the target value.

6. The "new game" button would reselect a secret value in the 1 to 100 range regardless of the range configured by the game's supposed difficulty.

**Bug Reproduction Log**

<!-- Document at least 3 bugs you found. Add rows as needed. -->

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Leave the guess blank and click "Submit Guess" twice | The "Enter a guess" banner is displayed and the game does not progress for any submission. | The game progresses on the 2nd submission (for any submission after the first). | No console error.|
| Change the game's difficulty setting from Normal to Easy. | A new game should be started with a secret value in the appropriate range. | The current game continues with only total attempts changed. | No console error.|
| Set the game difficult to "Easy" and click "New Game" until a number larger than 20 appears (usually less than 5 times). | The game's difficult range should dictate the range allowed for the secret value. | The secret value always exists in the 1 to 100 range. | No console error.|
| Load the application. | The game should load with attempts as 0. | The game loads initially with 1 attempt already having been completed. | No console error. |

---

## 2. How did you use AI as a teammate?

> Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Anthropic's Claude Code for the code updates and Google's Gemini to answer some of my markdown questions.

> Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

One of the main problems I fixed was around the game hints offered to users based on their guess. 
Claude suggested swapping the returned help text such that the "higher" was when the guess was too low and the "lower" was when the guess was too high.
This suggestion was both helpful and correct.
I verified the change a couple of ways. 
First, I carefully read the suggestion, verifying what it was doing. 
Second, I asked for tests of the various cases which I also verified were correct. 
Finally, I ran the generated tests and the application.

> Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

Another problem I fixed was around the state management.
While Claude's code suggestion was correct, the tests it suggested were not.
The tests it wrote didn't actually test anything useful.
Each test would mock an object, set the values directly on the mocked object, and verify the values.
None of this relied on any of the production code, offering no safegaurds or quality assurance.
I ultimately removed these tests as they provided no value.

---

## 3. Debugging and testing your fixes

> How did you decide whether a bug was really fixed?

I relied on the `pytest` automation to verify if a bug was really fixed. 
I did also run the application, but that was only after the automation was passing.

> Describe at least one test you ran (manual or using pytest) and what it showed you about your code.


The simplest manual test I ran was loading the application.
Since I fixed the state initialization around the attempt number, it was immediately apparent if this was resolved or not.
This test demonstrated that my fix had been correct.

One step further, I verified the rest of the state management changes by adjusting the difficulty setting and checking that the history and attempts were cleared.

> Did AI help you design or understand any tests? How?

Yes! Claude designed and wrote all the automation.
It also updated the test configuration so that it would seamlessly work with the `pytest` command as that was originally causing failures.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
