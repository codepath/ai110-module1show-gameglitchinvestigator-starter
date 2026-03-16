# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").
1. When I first ran the game, the UI loaded fine but the hints were completely backward
2. The count was always off by one.
3. The New Game button was broken. It never resets.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?  Copilot

**Correct suggestion:**
The AI correctly identified that the New Game button was broken because `st.session_state.status` was never reset back to `"playing"` after a win or loss. It suggested adding `st.session_state.status = "playing"` inside the new game handler. I verified this by winning a game and then clicking New Game — before the fix the screen stayed frozen with the "You already won" message, and after the fix the game restarted properly and accepted new guesses.

**Incorrect or misleading suggestion:**
The AI initially suggested fixing the hint messages only in the `try` block of `check_guess`, but left the `except TypeError` fallback path with the old backwards messages still in place. That meant on even-numbered attempts — when the secret was secretly converted to a string and triggered the `TypeError` path — the hints were still wrong. I caught this by reading the full function carefully and noticing the fallback block was untouched. The real fix was to remove the string-conversion logic entirely so the `TypeError` path could never be reached.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed only when I could see the correct behavior both in the live game and in a passing pytest test — passing the test alone wasn't enough because some bugs only show up when Streamlit reruns the whole script. For the hint bug, I added two pytest cases: one that checks `check_guess(60, 50)` returns `"Too High"` and another that verifies the message contains `"LOWER"` — before the fix that second test failed, which confirmed the bug was real and the fix was targeted. I also manually played through a full game on each difficulty after every fix to make sure nothing broke the UI. The AI helped me write the test structure and suggested unpacking the tuple return value (`outcome, _ = check_guess(...)`) which I didn't think to do at first since the original starter tests were written incorrectly comparing the tuple directly to a string.

---

## 4. What did you learn about Streamlit and state?

The secret number kept changing because Streamlit reruns the entire script from top to bottom every time the user interacts with the page, so `random.randint()` was being called again on every button click, generating a brand new secret each time. Streamlit reruns are like refreshing the page — everything resets unless you store the value in `st.session_state`, which acts like a small memory that survives between reruns. The fix was wrapping the secret generation in `if "secret" not in st.session_state:` so it only runs once at the start of a new game, not on every rerun.

---

## 5. Looking ahead: your developer habits

One habit I want to keep is writing tests that target the exact bug I just fixed, not just general passing tests — the `test_too_high_message_says_lower` test would have caught the hint bug immediately if it had existed from the start. Next time I work with AI on a coding task I would read the full function it touches before accepting the change, because the AI fixed the `try` block but left the `except` fallback broken, which I only caught by reading carefully. This project made me realize that AI-generated code can look completely correct on the surface while hiding subtle logic bugs, so I now treat AI suggestions the same way I would treat code from a teammate — useful, but always worth verifying.
