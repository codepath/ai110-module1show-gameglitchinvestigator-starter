# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  ### 1. The Guess hint message is misleading. 
  While testing the guessing feature, I noticed the message below the input says, “Guess a number between 1 and 100.” I decided to test whether the program would accept values outside this range by entering negative numbers. The application accepted -1 and generated the hint “Go LOWER!”, which seemed misleading since the guess was already outside the stated range. I also tested -100 and received the same hint, and when I entered 199, the game responded with “Go HIGHER!”. This suggests the hint logic may not be validating whether the users guess is within the intended range before generating guidance.

  ### 2. Score? (Not a bug)
  So it seems like the score after I attempted all 8 attempts is -30. Still need to further envistage this. 
    **UPDATE**: After reviewing the scoring logic, the score can become negative because incorrect guesses reduce the score over multiple attempts. A "Too Low" result always subtracts 5 points, and "Too High" may also subtract 5 points on odd-numbered attempts. Because of these repeated deductions, the total score can drop below zero after several incorrect guesses. 

  ### 3. New Game generator button
  After using all eight attempts, the game displayed the message “Game over. Start a new game to try again.” I clicked the New Game generator button expecting it to start a new guessing session. However, it did not appear to reset the game or allow me to begin another round. From my testing, the button seems to work while a session is still active but not after all attempts have been exhausted. Ideally, the button should allow users to start a new game both during and after a completed session.

  ### 4. No Session Renewal after switching from Difficulty levels
  I navigated to the settings sidebar where users can choose the difficulty level for the guessing game. After finishing a session in Easy mode, I selected Normal difficulty to start another game. However, the application did not allow me to submit a guess and instead displayed a message asking me to start a new game. This behavior appears related to the issue where the New Game button does not properly reset the session. It seems possible that switching difficulty levels is not creating a new game session.

  ### 5.  Range per Difficulty level is not updated in hint message
  While switching between difficulty levels, I noticed that each level displays a different range for the numbers. For example, when I selected Easy, the range shown below the difficulty selector was “Range: 1 to 20.” However, the hint message below the guess input still said “Guess a number between 1 and 100. Attempts left: 4.” This suggests the hint message is not updating to reflect the range associated with the selected difficulty level. I did notice that the number of attempts does update correctly when the difficulty changes.

  ### 6. Attempts mismatch between difficutly level selector and Hint message
  While testing different difficulty levels, I noticed a mismatch in the number of attempts displayed. For example, the Hard difficulty indicates “Attempts allowed: 5,” but the hint message below the input shows “Attempts left: 4” before any guess is submitted. The same behavior appears with other difficulty levels as well. For instance, Normal shows “Attempts allowed: 8,” while the hint message displays “Attempts left: 7” immediately when the game starts. This suggests the hint message may be decrementing the attempt counter before the user submits the first guess..

  ### 7. Guess History Input Delay
   I also noticed the guess history displayed in the debug panel did not record my first guess immediately. The first input only appeared in the history after I submitted a second guess, suggesting the guess tracking may be delayed or not updating on the first entry. 

  ### 8. Possible Difficulty Range Incosistency 
  While exploring the difficulty levels, I noticed that Easy uses a range of 1 to 20, Normal uses 1 to 100, and Hard uses 1 to 50. This ordering seemed unusual because the ranges do not progressively increase with difficulty. I initially expected something like Easy: 1–20, Normal: 1–50, and Hard: 1–100 so that the guessing range becomes larger as the difficulty increases. Because of this, I was unsure whether the current configuration is intentional or if the ranges may be incorrectly assigned. This may not necessarily be a bug, but it stood out while testing the different difficulty settings.

      Bugs Fixed: 7 (#5, #1, #3, #4, #6, #8, #7)
  ---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  I used Claude Code. 
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  I used Claude Code as an AI teammate while fixing the misleading guess hint bug I documented earlier. While reviewing the check_guess function, I noticed that when guess > secret the function returned "Too High", "Go High", which seemed incorrect because a guess that is too high should instruct the user to go lower, so I updated the return values and tested the app. 
  
  During testing I guessed a number close to the secret but lower than it, yet the app still told me to go lower, which led me to investigate further and notice an except TypeError block that converted the guess to a string. 
  
  I asked AI why that conversion existed when another function in logic_utils already converts input strings to integers, and it pointed out that app.py was converting the secret value into a string, forcing the workaround. 
  
  After confirming this behavior, I fixed the root issue in app.py and removed the unnecessary workaround from logic_utils.py, which AI also explained was an example of a classic code smell where a bug is masked rather than properly fixed.



- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

  One AI suggestion that I realized was misleading involved using Python’s `eval()` to process user input in the project. At first it seemed like a convenient way to evaluate expressions, but after looking into it more I learned that `eval()` can execute any Python code, which could be dangerous if the input isn’t trusted. I verified this by checking Python documentation and other programming resources, which confirmed that using `eval()` with user input is generally considered unsafe.


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

    So for each bug, I first examined the program’s initial behavior and identified how it differed from the expected outcome. I documented the issue and clarified what the function should do if it were implemented correctly.

    I then wrote targeted test cases designed to reproduce the bug and isolate the problematic logic. By running these tests, I could confirm that the function was failing under specific conditions. After identifying the root cause, I modified the implementation and reran the tests to ensure they passed.

    Finally, I validated the fix within the actual game application by testing multiple edge cases and gameplay scenarios where the bug could potentially occur. If the program behaved correctly across these different situations, I considered the bug to be resolved.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
    One particular test that stood out to me involved the check_guess function, specifically test_guess_too_high(), test_guess_too_low(), test_too_high_hint(), and test_too_low_hint(). While running these tests, I noticed that test_too_high_hint() was failing due to a peculiar design in check_guess() that included an except TypeError block. The exception handler converted the user’s guess to a string, even though another function already ensured that user input was parsed into integers.

    After investigating further, I discovered that app.py sometimes converted the secret number to a string before passing it to check_guess, which explained why the workaround existed. This test revealed a violation in single responsability principle, where check_guess was handling inconsistent data types instead of relying on the dedicated input parsing function.

- Did AI help you design or understand any tests? How?

    AI helped me understand and design tests for the `update_score` function in `logic_utils`. I initially did not fully understand the point system criteria, so I asked AI to explain how the scoring logic worked. It clarified how points are awarded for a win using the formula `100 - 10 * (attempt_number + 1)` with a minimum of 10 points, and how incorrect guesses adjust the score depending on the outcome and attempt number. This explanation helped me design tests that verify winning scenarios, even and odd `"Too High"` attempts, and the constant deduction for `"Too Low"` guesses.


---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  In Streamlit, the entire script reruns from top to bottom every time a user interacts with the app, like typing inpt a text input or selecting an option from a dropdown. Because of this, normal variables reset each time unless their values are stored somewhere persistent, which is why Streamlit provides st.session_state to keep values across reruns. I like to think of it like a video game where the level reloads whenever you press a button, but session_state works like your saved inventory that stays even when the level restarts.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

  One habit I want to continue reusing in projects is applying a test-driven development approach by thinking about test scenarios first and allowing tests to fail before implementing or revising functions. I had previously learned about TDD concepts in another course, so it was exciting to revisit and apply them again in this project. This process helped me better understand expected behavior and document the intended logic before writing the solution, while also encouraging me to inspect the code for potential bugs that tests might not immediately catch. 

    One habit I've carried and applied here is committing changes frequently in Git so I can easily revert to earlier versions if needed while keeping my changes focused and organized, which I thought was worth sharing. 

- What is one thing you would do differently next time you work with AI on a coding task?

    This project reinforced that AI-generated code should be treated as a reference or starting point rather than something to accept blindly. It reminded me that developers still need to understand the logic, verify behavior, and ensure the solution does not introduce unnecessary complexity or tightly coupled code.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

    This project helped me see that AI-generated code should be treated as a starting point rather than a final solution. It reinforced the importance of carefully reviewing the logic, writing tests, and verifying behavior to ensure the code works as intended.
