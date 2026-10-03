# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The first time I ran it, the game looked like a normal number-guessing app —
it asked for a guess, showed a hint, and tracked a score — but playing a few
rounds showed it was nearly unwinnable. The hints were backwards (a guess
that was too high said "Go HIGHER!" instead of "Go LOWER!"), the secret
number sometimes got compared as a string instead of a number every other
attempt (making "Too High"/"Too Low" results flip unpredictably), the score
for a first-try win was 10 points short of what it should be, and wrong
guesses sometimes added points instead of subtracting them. On top of the
logic bugs, the "Attempts left" counter started one attempt short because
`attempts` was initialized to 1 instead of 0.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess of 60 when secret is 50 | "Too High" hint telling you to go lower | Hint said "📈 Go HIGHER!" instead of "📉 Go LOWER!" | none |
| Guess of 9 when secret is 10, submitted on an even-numbered attempt | "Too Low" outcome (9 < 10) | "Too High" outcome — secret was silently converted to a string, so `"9" > "10"` compared as text instead of numbers | none |
| Win on the very first attempt | Score +90 (`100 - 10*1`) | Score +80, because the formula used `100 - 10*(attempt_number + 1)` | none |
| Wrong guess ("Too High") on attempt #2 | Score -5 | Score +5 — the code rewarded a wrong guess on even attempt numbers instead of always deducting | none |
| Submit a guess, then edit the box and submit again | Second guess is read and scored | Text box went empty and showed "Enter a guess." — the widget's key changed mid-script, orphaning what was typed | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used GitHub Copilot (Claude Sonnet 5) in agent mode inside VS Code for the whole
investigation, from finding bugs to refactoring and writing tests.

**Correct suggestion:** I asked it to fix the scoring bugs in `update_score`.
It correctly identified that the win formula `100 - 10 * (attempt_number + 1)`
had an extra `+ 1` that under-scored every win by 10 points, and that the
`"Too High"` branch gave a +5 bonus on even attempt numbers instead of always
deducting 5. It changed the formula to `100 - 10 * attempt_number` and made
`"Too High"` always return `current_score - 5`. I verified this by writing
regression tests (`test_win_on_first_attempt_scores_90_not_80` and
`test_too_high_always_deducts_even_on_even_attempt`) and running `pytest`,
which passed, confirming the new values matched what the game should actually
award.

**Suggestion I changed:** when I reported that the guess box went empty and
asked for input a second time after editing a guess, Copilot's first fix was
to keep the `text_input` key stable and clear it through a `handle_submit()`
function passed as the button's `on_click` callback. That wasn't a "wrong"
idea on its face — `on_click` callbacks are a real, documented Streamlit
pattern for this exact problem — but when I actually tested it in the running
app I still had to click "Submit Guess" twice before it registered: the
callback could fire before the text box's latest edit was committed to
`session_state`, so it sometimes read a stale value. I didn't just accept
that it "should" work because the code looked reasonable; I rejected that
version once I saw it fail in practice, and had it replace the manual
callback with `st.form(clear_on_submit=...)`, which batches the text input
and the submit button together so the value is only read once, atomically,
when the form is submitted. I verified the fix by running the Streamlit app
again and submitting several guesses in a row without the double-click or
empty-box behavior returning. That back-and-forth is the clearest example from
this project of me staying in the loop instead of trusting a plausible-looking
diff: the first version compiled fine and read fine, and the only way I caught
the problem was by clicking through the actual app myself.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I considered a bug fixed only when two things lined up: a `pytest` run showed
the right assertion passing, and manually playing the Streamlit app (via
`streamlit run app.py`) matched that expectation in the actual UI. For
example, after moving the logic into `logic_utils.py`, I ran
`pytest tests/ -v` and got `5 passed` — the three original tests
(`test_winning_guess`, `test_guess_too_high`, `test_guess_too_low`) confirmed
`check_guess` returns the right outcome in each direction (catching the
reversed-hint bug), and the two regression tests I added afterward
(`test_win_on_first_attempt_scores_90_not_80`,
`test_too_high_always_deducts_even_on_even_attempt`) pinned down the exact
`update_score` values so the off-by-one and parity bugs couldn't silently
come back. For the input-clearing/double-click bug there was no good way to
unit test Streamlit's rerun behavior, so I verified it manually by running
the app, typing a guess, submitting, editing the box, and submitting again to
confirm it registered on the first click. AI helped directly with test
design: when I asked it to add a test for "the bug you just fixed," it wrote
the two `update_score` regression tests above and explained what each
input/assertion was checking against — which attempt number to use and
what score the old buggy formula would have produced versus the fixed one —
so I could see exactly why each assertion value was correct instead of just
trusting the number.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

I'd explain that a Streamlit script isn't like a normal program that keeps
running in the background — it re-executes from top to bottom every single
time something happens on the page, like clicking a button or typing into a
box. Because of that, any plain Python variable resets to its initial value
on every rerun, which is exactly why this game needed `st.session_state`: it's
a dictionary that survives across reruns, so things like the secret number,
attempt count, and score don't get wiped out every time you interact with the
page. The trickiest part to internalize was that widgets are tied to this
same rerun cycle through their `key` — if a widget's key changes between
reruns, Streamlit treats it as a brand-new widget and throws away whatever
value it held, which is exactly the bug I hit when I keyed the guess box off
of `attempts`.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

The habit I want to keep is writing a regression test for every bug the
moment I understand its root cause, instead of just patching the code and
moving on — it's what caught that the scoring fix actually matched the
intended formula, not just "a" formula. Next time I work with AI on a coding
task, I'd push back sooner on UI/state fixes by actually running the app
before accepting them, since the `on_click` callback bug only surfaced once I
clicked through the real Streamlit app, not from reading the diff. This
project changed how I think about AI-generated code mainly by showing that
plausible-looking fixes (like the callback approach) can still have subtle
timing bugs, so I can't just trust that code compiles or looks reasonable —
I have to actually exercise it and verify the specific behavior it's supposed
to fix.
