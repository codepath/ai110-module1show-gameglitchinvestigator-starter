# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
When I first ran Game Glitch Investigator, the interface looked like a standard guessing game, but the logic under the hood was completely broken. The game gave the wrong instructions to the player, and the counters didn't match the actual gameplay.
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  **Defect 1:** Inverted & Unstable Hint Logic
  * Expected: If the guess is lower than the secret number, the hint should say "Higher." If the same number is submitted again, the hint should remain "Higher."
  * Actual: The hints are reversed (telling the user to go lower when they should go higher). Additionally, submitting the same number repeatedly causes the hint to toggle back and forth between "Higher" and "Lower."
  **Defect 2:** Broken "New Game" Button
  * Expected: Clicking "New Game" should reset the score, attempts, and generate a new secret number.
  * Actual: The button is non-functional. The user is forced to refresh the browser tab to start a new session.
  **Defect 3:** Desynchronized Attempt Counter
  * Expected: The counter should show the full amount of allowed attempts and decrement immediately after the first guess.
  * Actual: The counter starts at $N-1$ and stays "stuck" on that number after the first guess, only counting down from the second guess onward.
  **Defect 4:** Incorrect Difficulty Scaling
  * Expected: "Easy" mode should provide the most attempts, and "Hard" mode the fewest.
  * Actual: "Normal" mode provides 8 attempts while "Easy" only provides 6, making the middle difficulty easier than the beginner level.
  **Defect 5:** Flawed Scoring System
  * Expected: A perfect guess should result in a score of 100, and a lost game should result in a score of 0.
  * Actual: A perfect guess yields a score of 70, and the score continues to drop into negative numbers if the player exhausts all attempts.
  **Defect 6:** Dead "Enter" Key Functionality
  * Expected: Since the placeholder says "Press Enter to aopp," pressing the Enter key should submit the guess.
  * Actual: The Enter key does nothing; the user must manually click the "Submit" button.
  **Defect 7:** Missing Input Validation (Edge Cases)
  * Expected: The game should reject or warn the user if they enter a number outside the 1–100 range.
  * Actual: The game accepts any number (e.g., -5 or 500) and processes it as a valid guess.
  **Defect 8:** Inaccurate Developer Debug History
  * Expected: The debug window should show a correct chronological history of the guesses and the secret number.
  * Actual: The debug history is inaccurate and does not sync with the current game session.
  (for example: "the hints were backwards").

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  On this project, I utilized a multi-tool approach to handle both documentation and technical implementation:
  * Gemini: Used for initial defect analysis, brainstorming, and drafting professional bug reports from my raw observations.
  * Claude Code (in Visual Studio Code): Used as an agentic AI tool to analyze the codebase, refactor logic into separate modules (like logic_utils.py), and apply functional fixes directly to the files.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  * The Suggestion: When analyzing Defect 1 (Inverted Hint Logic), the AI correctly identified that the issue was twofold: first, the mathematical comparison operators ($<$ and $>$) were swapped, and second, the logic lacked a stable state check, causing the hint to "toggle" when the same number was guessed repeatedly. It suggested a clean if/elif/else block that strictly compared the guess to the secret number.
  * Verification: I verified this by using the Developer Debug mode to see the secret number. I then entered a number lower than the secret, verified the "Higher" prompt appeared, and clicked "Submit" multiple times to ensure the message remained stable and did not flip-flop.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  * The Suggestion: I asked the AI to fix Defect 4 (Difficulty Scaling) so that Easy mode would have more attempts than Hard mode. While the AI successfully re-ordered the attempts (giving Easy 10 and Hard 4), it also "hallucinated" a change to the game range. It updated the code to only allow numbers between 1 and 20, even though the rest of the game was still set up for 1–100.
  * Verification: I caught this during manual testing. I tried to guess "50" (which should be a valid guess), but the game kept telling me it was out of range. I checked the code and found the AI had narrowed the game’s boundaries without being asked, making the game impossible to play with the original rules.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  I used a "Dual-Verification" approach to confirm each fix. First, I performed Manual Validation to ensure the user experience in the browser was smooth and logical. Second, I relied on Automated Regression Testing using the 47 pytest cases I developed. A bug was only considered "Resolved" when the manual behavior matched the expected outcome and the corresponding automated test script returned a PASSED status.
- Describe at least one test you ran (manual or using pytest)  
  I ran a targeted pytest script to validate Defect 1 — Issue 2 (int/str type toggle in app.py).
  * The Test: The script simulated a user inputting a number (string) and checked if the backend correctly cast it to an integer before passing it to the check_guess function.
  * What it showed: Initially, the test failed because the code was attempting to compare a string to an integer, which caused the "toggle" glitch you'd see in the UI. Once the fix was applied, the test confirmed that the data types were consistent, ensuring the hint message remained stable across multiple submissions.
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
  Yes, Claude was instrumental in bridging the gap between my manual observations and formal automation.
  * Documentation & Mapping: I used Claude to help document and label the 47 test cases so they mapped directly to the defects listed in my reflection.md. This ensured that every issue—from the "Swapped Hints" in logic_utils.py to the "Stale Debug History"—had a dedicated test.
  * Test Case Generation: Claude assisted in writing the pytest syntax for complex scenarios, such as the Defect 5 (Scoring System) logic, by suggesting boundary tests to ensure the score never dropped below 0 or exceeded 100. This allowed me to focus on the high-level logic while the AI handled the repetitive structure of the test scripts.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  The secret number kept changing because of how Streamlit is built. Every time you do anything in the app—like typing a number or clicking "Submit"—Streamlit re-runs the entire Python script from the very first line to the last.
  In the original code, the line that generated the random number was just sitting there in the open. So, every single time I made a guess, the app would hit that line again and pick a brand-new number. It was essentially like playing a game where the goalpost moves every time you try to kick the ball.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  Think of Streamlit as a script that executes from top to bottom every single time a user interacts with a widget. It doesn’t stay "open" and wait for events; it literally restarts the entire process. This is the rerun.
  Session State is a dictionary-like object that persists across those reruns. It’s the only way to store variables in the server's memory so they don't get reset to their default values every time the script executes. Without it, your variables are local and temporary; with it, they become "sticky" for that specific user's session.
- What change did you make that finally gave the game a stable secret number?
  To keep the secret number from changing, I used Session State to store it.
  I updated the code to check if a secret number already existed in the session before creating a new one. By wrapping the random number generator in a simple if 'secret_number' not in st.session_state: block, I ensured the app would only pick a number once. Now, when the script reruns, it just pulls the same value from memory instead of generating a new one.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  I want to keep using the "Identify then Refactor" strategy. Breaking the project into two distinct phases—first documenting the bugs in a reflection file and then using Agent Mode to move logic into logic_utils.py—made the actual fixing much more organized. It’s a lot easier to fix code once the "spaghetti" logic is separated from the UI.
- What is one thing you would do differently next time you work with AI on a coding task?
Next time, I will avoid running parallel chat sessions for related defects. I learned that when I split Defect 3 and Defect 4 into different windows, the AI lost the shared context and gave me an incomplete fix. Keeping related logic in one conversation helps the AI "see" how one change affects the rest of the system.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
This project showed me that AI is an incredible "co-pilot" for refactoring and testing, but it can still be confidently wrong about simple logic. I now see AI code as a draft that requires a test case, rather than a finished product I can just trust blindly.
