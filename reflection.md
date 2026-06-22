# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game it appeared to work on the surface — I could type a guess and submit it — but the feedback was completely unreliable. The hints told me to go in the wrong direction, so guessing the right answer felt impossible. I also noticed that after winning or losing, clicking "New Game" did nothing and the game stayed frozen on the end screen. When I switched difficulty the range shown in the sidebar updated, but the secret number and the hint text at the top still said "1 to 100", so it was clear the difficulty setting wasn't actually being respected.

Concrete bugs noticed at the start:
- Hints were backwards ("Too High" told me to go higher, "Too Low" told me to go lower)
- Clicking "New Game" after the game ended did not restart the game

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guessed 80, secret was 50 | Hint: "Go LOWER!" | Hint: "📈 Go HIGHER!" | No error — wrong logic |
| Guessed 10, secret was 50 | Hint: "Go HIGHER!" | Hint: "📉 Go LOWER!" | No error — wrong logic |
| Won the game, then clicked "New Game" | Game resets to playing state | Screen stayed frozen on "You already won" | No error — `status` was never reset |
| Changed difficulty from Normal to Easy mid-game | New secret between 1–20, hint updates | Secret unchanged, hint still showed "1 to 100" | No error — difficulty not tracked in session state |
| Submitted guess on attempt 2 (even attempt) | Normal integer comparison | Secret temporarily converted to string, causing wrong comparisons | No error — silent logic bug |

---

## 2. How did you use AI as a teammate?

I used Claude Code (Anthropic's AI coding assistant built into VS Code) as my main AI tool on this project. I described the symptoms I was seeing — wrong hints, broken restart, difficulty not updating — and Claude identified the root causes in the source code and suggested specific line-level fixes. One example where the AI suggestion was correct: Claude pointed out that on every even-numbered attempt, `app.py` was converting the secret number to a string before passing it to `check_guess`. This caused Python's string comparison (`"5" > "100"` is `True` because `"5" > "1"`) to produce wrong results silently. I verified this was real by checking lines 158–161 in `app.py` and confirming the `% 2 == 0` condition was there exactly as described.

One example where I had to verify carefully: Claude noted the hint messages in `check_guess` were swapped. Before accepting that, I traced through the logic manually — if `guess > secret` that means the guess is too high, so "Go LOWER!" is correct, but the code said "Go HIGHER!". Reading it myself confirmed the swap was real and not just an AI misread.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed by reproducing the exact input that triggered it before the fix, then confirming the correct behavior after. For the hint bug, I ran the game, guessed a number I knew was lower than the secret, and verified the hint now said "Go HIGHER!" instead of "Go LOWER!". For the restart bug, I played until I won, then clicked "New Game" and confirmed the board reset and I could submit guesses again. For the difficulty bug, I switched from Normal to Easy and checked that the info banner updated to "1 to 20" and the debug panel showed a new secret within that range.

For the even-attempt string comparison bug, I manually tested by making exactly two guesses in a row on a known secret. Before the fix, the second guess sometimes returned a wrong hint even when my guess was clearly in the right direction. After removing the string conversion, both guesses gave consistent, correct feedback. Claude helped me understand that Python compares strings lexicographically, which is why `"5" > "100"` returns `True` — that framing made it easy to design a test case that would expose the bug reliably.

---

## 4. What did you learn about Streamlit and state?

Streamlit works differently from most code you write: every time a user interacts with the page (clicks a button, changes a dropdown, types in a box), Streamlit re-runs your entire Python script from top to bottom. That sounds chaotic, but `st.session_state` is a dictionary that persists across those reruns — anything you store in it survives. Think of the script itself as the "frame renderer" and `session_state` as the "save file." The restart bug in this project was a perfect example of why this matters: the `if new_game:` block reset `attempts` and `secret` but never touched `st.session_state.status`, so on the very next rerun Streamlit still saw `status == "won"` and stopped the game immediately. Understanding reruns also explained the difficulty bug — `low` and `high` were calculated fresh each rerun from the selected difficulty, but the secret was guarded by `if "secret" not in st.session_state`, so it never regenerated when the difficulty changed.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is **describing the symptom first, not the fix**. When I told Claude "the hints are wrong and the game won't restart," it found root causes I hadn't spotted yet (like the string conversion on even attempts). If I had just asked "fix the check_guess function," I might have missed that hidden bug entirely. That prompting strategy — describe what you observe, not what you think the solution is — gave me a more complete picture.

One thing I would do differently next time: before accepting any AI fix, I would read every changed line myself and trace through at least one example input by hand. On this project I did that for the hint swap and it built real confidence that the fix was correct. For more complex changes I was tempted to just run it and see, but manual tracing catches logic errors that passing tests can miss.

This project changed how I think about AI-generated code by showing me that AI can produce code that looks completely reasonable and runs without errors, but still has subtle logic bugs baked in — like backwards hints or a broken restart — that only show up when you actually play the game. AI is a fast first draft, not a finished product.

