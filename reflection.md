# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The game looked finished the first time I ran it. There was a sidebar with difficulty settings, a guess box, Submit and New Game buttons, and a score. Nothing ever crashed, which is what made it hard: none of these bugs throw an error, they just quietly give you the wrong answer. It took two playthroughs before I noticed the hints were following a pattern instead of being random.

The bugs I found:

- The hints were backwards. It should tell you to go lower when your guess is higher than the secret number, and vice versa, but it told you the opposite.
- You can see the secret number before the game even starts, because the "Developer Debug Info" panel prints it straight onto the page.
- The game doesn't reset when it's time to play a new game. Once you win or lose, the New Game button does nothing.
- Later I also found that the score went up on some wrong guesses and down on others, and that "Hard" mode was actually easier than "Normal" because it used a smaller range of numbers.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Secret is 50, guess `60` | Hint tells me to go lower | Hint said "📈 Go HIGHER!", pointing away from the answer | none — `check_guess(60, 50)` returned `('Too High', '📈 Go HIGHER!')` |
| Secret is 50, guess `40` | Hint tells me to go higher | Hint said "📉 Go LOWER!" | none — `check_guess(40, 50)` returned `('Too Low', '📉 Go LOWER!')` |
| Lose a round, then click **New Game 🔁** | A new round starts with a new secret number | Page stayed on "Game over" and stopped responding. No indicator of it restarting. Only a browser refresh cleared it | none — `st.stop()` ends the run silently |
| Tick the **Show hint** checkbox after submitting a guess | The hint appears | Nothing happened at all | none |
| Two wrong guesses, both "Too High", on attempts 2 and 3 | Both wrong guesses cost the same | Attempt 2 **gained** +5 points, attempt 3 **lost** 5 | none — `update_score(0,'Too High',2)` → `5`, `update_score(0,'Too High',3)` → `-5` |
| Open the app before guessing anything | The secret number is hidden | The secret is printed in the Developer Debug Info panel | none |

The "Console Output / Error" column is "none" for every single row, and that turned out to be the most important thing I learned. Not one of these bugs announces itself. I confirmed each row by calling the functions directly with fixed numbers instead of trusting what the screen showed me.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used ChatGPT for my first pass on this project, to analyze the code, identify bugs, explain confusing logic, and help generate test cases. Later I went back through it with Claude Code inside VS Code, which could read the whole project instead of just a snippet I pasted in. That mattered more than I expected, because the worst bug in this codebase only makes sense if you look at `app.py`, `logic_utils.py` and the test file together.

One AI suggestion that was correct was identifying that the high and low hints were reversed inside the `check_guess()` function. The AI suggested updating the messages so that guesses above the secret number return a "Go LOWER" hint and guesses below the secret return a "Go HIGHER" hint. I verified this by running the game and confirming the hints matched the guesses, and later by adding a test that asserts the word "LOWER" appears in the hint for a "Too High" outcome.

One AI suggestion that was misleading was assuming the problem was entirely inside the hint logic. After reviewing the code more carefully, I discovered that game state and session state behavior were also causing bugs. I verified this by playing multiple games and watching how the secret number and game status behaved after restarting. The hint fix alone would have left the New Game button broken.

One suggestion I did not accept as written came up when I asked for help the second time. Before I had looked at anything myself, the assistant started rewriting `logic_utils.py` with all the fixes already applied. The code was not wrong, but I told it to stop and just get the app running instead. If I had accepted it I would have had working code and no idea what had been broken or why, and I could not have filled in the reproduction log above, because I would never have seen the bugs happen. I did the diagnosis myself and only brought the AI back in once I could describe each bug precisely.

One more thing worth saying: the starter code is itself AI-generated, and its most damaging line is the one that looks the most responsible. There is a `try/except TypeError` wrapped around the comparison in `check_guess`. It reads like careful defensive programming. What it actually does is catch a real type error and silently fall back to comparing the numbers as text, so the game gives confidently wrong answers instead of crashing. A crash would have been better, because I would have found it immediately.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I determined a bug was fixed by testing both the application and the automated test cases. After making a change I ran the Streamlit app and tried several guesses to check that the expected behavior actually happened, and I ran `pytest` to confirm the logic functions returned the right outcomes. My rule was that a bug was not fixed until I had a test that failed on the old code and passed on the new code, because a test that passes after the fix might have passed before it too.

One test I ran checked whether a guess of 60 against a secret number of 50 returned "Too High", and another verified that the hint told the player to go lower. These confirmed the hint bug was fixed. The test I found most useful, though, was `test_string_secret_is_not_compared_as_text`, which asserts that `check_guess(9, "100")` returns "Too Low". On the original code it returned "Too High", because comparing `9` to `"100"` raises a `TypeError`, the bare `except` swallows it, and the fallback compares them alphabetically, where `"9" > "100"` is true. That test taught me the bug was not in the guessing logic at all. It was a **type** bug leaking into a comparison, and it only showed up on even-numbered turns, which is why it looked random while I was playing.

The suite now has 17 tests: the 3 that came with the starter, plus 14 I added covering hint direction, the string comparison, the score changing the same amount on odd and even turns, out-of-range and decimal guesses being rejected, and "Hard" actually having a wider range than "Normal".

AI helped me understand how to write focused tests for one piece of logic at a time instead of trying to test the whole application at once, which made it much easier to verify individual fixes. But I had to supply the failing inputs myself. The assistant did not know the secret was being turned into a string on even turns until I told it, because that line lives in `app.py` while the bug shows up in `logic_utils.py`. It was good at turning a diagnosis into a test and no help at all in producing the diagnosis.

Some bugs could not be covered by pytest at all, because they live in session state rather than in a pure function. I checked those by hand: losing a round and clicking New Game now really does start a new round, toggling "Show hint" after a guess now shows the hint instead of doing nothing, and switching difficulty picks a fresh secret inside the new range.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

I learned that Streamlit reruns the entire script from top to bottom every time a user interacts with the page. Because of this, variables reset on every click unless they are stored in `st.session_state`. Session state is what allows information like the score, the attempt count and the secret number to persist between reruns. Without it the game would restart constantly and lose important data.

The part that confused me longest was buttons. A button variable is only `True` for the single rerun right after you click it, and `False` on every run after that. The hint in this game was being drawn inside `if submit:`, so when I ticked the "Show hint" checkbox, the script reran with `submit` now `False`, the whole block was skipped, and the hint silently disappeared. The checkbox looked broken, but the real problem was that the hint was being treated as something you draw once instead of something you store. Fixing it meant saving the outcome into session state and drawing the hint from there on every run.

The way I would explain it to a friend: Streamlit re-reads your whole script every time you touch anything on the page, like re-running a program from line one. Anything you want to survive that has to be put somewhere it can't reach, and `st.session_state` is that place.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

The habit I want to keep is writing down what actually happened before trying to fix it. Filling in the reproduction log felt like busywork at the start, but it was the thing that made the bugs findable. Once I had "guess 60 against secret 50 returns Too High with a GO HIGHER message" written out, the broken line was obvious. Guessing at fixes without that step is how I used to work and it is much slower.

The thing I would do differently is not letting the AI start fixing before I understand the problem. The first time I asked for help it immediately began rewriting the logic file, and if I had let it I would have ended up with working code I could not explain. Now I would ask it to explain the code first and only ask for changes once I can describe the bug myself.

This project changed how I think about AI generated code mainly because of that `try/except` block. The code looked professional, it was formatted well, it had docstrings, and it was confidently wrong in a way that never produced an error message. I used to treat code that runs without crashing as probably fine. Now I assume AI generated code is plausible rather than correct, and I look hardest at the parts that look most defensive, because that is where this one hid its worst bug.
