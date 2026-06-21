# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

The game looked good when I first ran it, but after I started playing, I noticed several problems. The hint system kept telling me to guess a lower number every time I entered a guess. Eventually, I reached 0, but the game still said "lower," even though the instructions said the secret number should be between 0 and 100. This made it impossible to find the correct answer.

Two other bugs I noticed were related to restarting the game and the attempts counter. The **New Game** button did not work properly because the game would not fully reset after the first round. The secret number seemed to stay the same until I refreshed the page. I also noticed that the attempts counter went into negative numbers, such as **-3**, on both Easy and Hard difficulty levels. In addition, the **Show Hint** checkbox did not appear to do anything because hints were shown whether the option was checked or not.

## Bug Reproduction Log

| Input / Action                                 | Expected Behavior                                                           | Actual Behavior                                             | Console Output / Error |
| ---------------------------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------- | ---------------------- |
| Keep guessing numbers until reaching 0         | The game should provide correct hints and stop when no valid guesses remain | The hint continued saying "Lower" even when the guess was 0 | No error shown         |
| Click **New Game** after finishing a round     | The game should reset with a new secret number                              | The game did not fully reset until the page was refreshed   | No error shown         |
| Select Easy or Hard mode and continue guessing | Attempts should decrease to 0 and stop                                      | Attempts continued into negative values (for example, -3)   | No error shown         |
| Check and uncheck the **Show Hint** option     | Hints should only appear when enabled                                       | Hints appeared regardless of the checkbox state             | No error shown         |


## 2. How did you use AI as a teammate?

I used Cloud as my AI coding assistant to help understand the bugs in the guessing game. I attached the project files, especially `app.py` and `logic_utils.py`, so the AI could explain the logic and help me identify why the game was not behaving correctly.

One correct AI suggestion was that the higher/lower hint logic was reversed. The game was telling the player to go lower or higher at the wrong time, so I fixed `check_guess()` in `logic_utils.py`. I verified this by testing guesses below, above, and equal to the secret number.

One AI suggestion that I still had to review carefully was related to moving logic into `logic_utils.py`. I had to make sure the functions were not duplicated incorrectly in `app.py` and that the app was still using the correct imported functions.

---
## 3. Debugging and testing your fixes

I ran the starter pytest tests included with the project to verify the core logic. The tests checked that a guess higher than the secret says to go lower, a guess lower than the secret says to go higher, and a correct guess returns a win.

The tests passed after I fixed the `check_guess()` function in `logic_utils.py`. This confirmed that the high/low hint logic worked correctly.


---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the script from top to bottom every time the user interacts with the app, such as clicking a button or entering text. This means normal variables can reset unless they are saved in `st.session_state`.

I learned that session state is important for games because it keeps track of values like the secret number, attempts, score, status, and history between user actions.

## 5. Looking ahead: your developer habits

One habit I want to reuse in future projects is writing down bugs in a clear reproduction table before fixing them. This makes it easier to understand what is wrong and verify whether the fix actually worked.

Next time I work with AI on a coding task, I would ask for smaller explanations and test each suggestion before changing too much code at once.

This project changed the way I think about AI-generated code because I learned that AI code can look correct but still have hidden logic problems. I should always run, test, and review the code instead of trusting it immediately.
