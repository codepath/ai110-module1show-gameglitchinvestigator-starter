# 💭 Reflection: Game Glitch Investigator

 Everything looked normal and working at first glance. 
However after my first few guesses I noticed something felt off — I typed 
a number 100 I knew was too high (I could see the secret in the Developer Debug 
Info panel) and the game told me to go HIGHER instead of LOWER. The score 
also jumped up by 5 points after that wrong guess instead of going down, 
which made no sense. It was only after playing two full rounds and paying 
close attention that I realized the bugs were not random crashes but silent 
logic errors that made the game behave incorrectly in specific situations.

## 1. What was broken when you started?

Here's the updated Section 1 with your two additional bugs added:

```markdown
## 1. What was broken when you started?

When I first ran the game using `python -m streamlit run app.py`, the UI 
loaded cleanly in my browser with a sidebar showing difficulty settings, 
a text input box for guesses, and three buttons — Submit, New Game, and 
a Show Hint checkbox. Everything looked normal and working at first glance. 
However after my first few guesses I noticed something felt off — I typed 
a number I knew was too high (I could see the secret in the Developer Debug 
Info panel) and the game told me to go HIGHER instead of LOWER. The score 
also jumped up by 5 points after that wrong guess instead of going down, 
which made no sense. It was only after playing two full rounds that I 
realized the bugs were silent logic errors happening in specific situations.

Concrete bugs I noticed at the start:
- The hints were backwards: On every second guess, guessing too high 
  showed "📈 Go HIGHER!" instead of "📉 Go LOWER!"
-Hard mode was easier than Normal: Selecting Hard difficulty showed 
  a range of 1–50 which is actually smaller and easier than Normal's 1–100
-Attempts counter was wrong: The game showed one fewer attempt than 
  expected right from the first guess — because the counter started at 1 
  instead of 0 and then got incremented again on submit, making the first 
  guess count as attempt 2
- **Submit button required two clicks**: The first click on Submit did not 
  register the guess — I had to click it twice before the game actually 
  processed my input and showed a hint


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| | | | |
| | | | |
| | | | |

---]
Guess `60` when secret is `40` on attempt 2 (even attempt) | " Go LOWER!" hint shown | " Go HIGHER!" hint shown incorrectly | none — silent logic error |
| Select "Hard" difficulty in sidebar | Hardest mode should have largest number range | Range shows 1–50, smaller than Normal's 1–100 | none — silent logic error |
| Click Submit button once with a valid guess | Guess is processed and hint appears immediately | Nothing happens on first click, requires second click to register | none — Streamlit rerun timing issue |
| First guess on a fresh Normal difficulty game | "8 attempts left" shown | "7 attempts left" shown because counter initialized to 1 not 0 | none — off-by-one error |
| Wrong guess on even attempt number | Score should decrease by 5 points | Score increases by 5 points instead | none — silent logic error |


## 2. How did you use AI as a teammate?


I used Claude as my primary AI coding assistant throughout this project, 
accessed through the Claude extension in VS Code. I attached both `app.py` 
and `logic_utils.py` directly in the chat to give Claude full context of 
the codebase before asking any questions. I used it to explain suspicious 
lines of code step by step, identify bugs, refactor functions into 
`logic_utils.py`, and generate pytest test cases.

**Correct AI suggestion**: Claude correctly identified that the backwards 
hints bug was caused by `str(st.session_state.secret)` on even attempts — 
converting the secret to a string so Python used lexicographic comparison 
instead of numeric comparison. I verified this by opening a Python terminal 
and running `"60" > "7"` which returned `False`, confirming that string 
comparison would give the wrong hint when the secret was a single digit 
like 7.

**Incorrect/misleading AI suggestion**: When I first asked Claude to list 
all the bugs at once, it missed the double-click Submit button issue 
entirely and did not flag it as a bug. I only discovered it myself by 
actually playing the game and noticing my first click never registered a 
guess. This showed me that AI can miss UI interaction bugs that only 
appear when you physically use the app — it can only reason about what 
it sees in the code, not what it experiences as a user

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed only when I could reproduce the exact scenario that triggered it before my fix and see the correct behavior every single time afterward — not just once. For the backwards hints bug specifically, I ran the game after fixing it and made guesses on both odd and even attempt numbers repeatedly, checking each time that the hint 
matched what the Developer Debug Info panel showed as the actual secret. Only when the hint was correct on every attempt, not just odd ones, did 
I consider it truly fixed.

**Test I ran**: I ran `pytest -v` after writing my tests and the most 
revealing one was `test_check_guess_always_int_comparison` which called 
`check_guess(60, 7)` and asserted the result was `"Too High"`. Before 
the fix this would have returned `"Too Low"` because Python's string 
comparison makes `"60" > "7"` evaluate to `False`. After the fix it 
correctly returned `"Too High"` because 60 is greater than 7 as integers. 
Seeing that specific test pass confirmed the root cause was fully resolved.

**AI help with tests**: Claude helped me understand what to test by 
explaining the string comparison bug clearly, which pointed me toward 
writing that specific integer comparison test case. It also suggested 
edge cases I would not have thought to test myself — like negative numbers, 
decimal inputs, and very large values — which became my Challenge 1 
advanced test suite. Without Claude's suggestions my tests would have 
only covered the happy path and missed these boundary cases entirel

---

## 4. What did you learn about Streamlit and state?
Streamlit works by re-running your entire Python script from top to 
bottom every single time a user interacts with the page — clicking a 
button, changing a dropdown, or typing in a box all trigger a full 
rerun. This means normal Python variables get completely reset to their 
starting values on every interaction, which would make it impossible to 
remember things like the secret number, attempt count, or score between 
guesses.

If I were explaining this to a friend who has never used Streamlit I 
would say: imagine you are playing a guessing game on a whiteboard, but 
every time you make a guess someone erases the entire whiteboard and 
redraws it from scratch. You would lose track of everything — what you 
guessed before, how many attempts you have left, and what your score is. 
`st.session_state` is like a sticky note taped to the corner of that 
whiteboard that never gets erased — anything you write on the sticky note 
survives every redraw.


---

## 5. Looking ahead: your developer habits

One habit I want to reuse in every future project is writing pytest tests  immediately after fixing a bug, not as an afterthought at the end. This  project showed me that having a specific test like 'test_check_guess_always_int_comparison` gives you permanent proof that a bug is fixed — if that bug ever comes back for any reason, the test will catch it instantly instead of me having to rediscover it by playing the game manually. I also want to keep using the Developer Debug Info panel technique in future Streamlit projects, since being able to see all 
internal state at a glance saved me a lot of time during debugging.

One thing I would do differently next time is ask Claude to explain every suspicious line of code before I even run the app, rather than discovering bugs through confusing gameplay first. Reading through the code with AI before testing would have surfaced the `str(secret)` cast bug in the first five minutes instead of me spending time confused about why hints were sometimes correct and sometimes wrong depending on which attempt number I was on.

This project changed the way I think about AI generated code because I used to assume that if code looked clean and professional it was probably correct — but the bugs in this project were completely invisible on a quick visual read and only showed up in specific situations during actual gameplay. I now treat all AI generated code with the same skepticism I would give any untested code, no matter how confident it looks.  It makes coding testing and maintainenance of the application easy as you just need to understand the functionality rather than writing the 1000's of lines of code and debugging it line by line.