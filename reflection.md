# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran it, the app loaded, but the feedback didn’t match my guesses. I expected a normal guessing game where the hints guide me and “New Game” resets cleanly. Instead, the hints were backwards and the game state/settings didn’t line up.

1) Bug: Hints were backwards.  
- Expected: Too high → “go lower”; too low → “go higher”.  
- Actual: It told me the opposite.

2) Bug: “New Game” didn’t match difficulty.  
- Expected: A new secret inside the selected range.  
- Actual: It still acted like the range was 1–100.

3) Bug: Attempts/range display felt off.  
- Expected: Attempts left + displayed range match the settings.  
- Actual: Attempts felt confusing and the main text didn’t always match the sidebar.

---

## 2. How did you use AI as a teammate?

I used Copilot and ChatGPT to understand the code and plan changes. The best help was breaking the work into small steps (move logic into `logic_utils.py`, then fix one bug at a time). One suggestion wasn’t great because it tried to rewrite too much at once, so I tested it, saw it didn’t really fix the issue, and went back to smaller edits.

---

## 3. Debugging and testing your fixes

I treated the bug as fixed only after it worked in the Streamlit app *and* the tests passed. I ran `python -m pytest` to confirm the core logic returned the right outcomes. AI helped by suggesting simple test inputs that directly matched the bugs I saw.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the whole script whenever you click something, so normal variables can “reset” a lot. Session state is how you keep important values stable across reruns (secret number, attempts, score). If you don’t manage session state, the app can feel random even if the code looks fine.

---

## 5. Looking ahead: your developer habits

I want to keep the habit of writing a small test right after I fix a bug. Next time I’ll ask AI for smaller, targeted changes and verify each one before moving on. This project reminded me AI code is a starting point — I still need to review, test, and own the final result.

---

## (Optional) Challenge 5: AI Model Comparison

For the “backwards hints” bug, one tool mostly gave me a quick code patch, and the other did a better job explaining *why* it was happening (Streamlit reruns + state). The quick patch got me moving faster, but the better explanation helped me avoid breaking things when I refactored. Overall, I trusted the fix that came with a clear reason *and* matched what I saw when I reran the app and tests.
