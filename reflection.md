# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess `60` when secret is `50` (odd attempt) | Hint should say "Go LOWER" | Hint said "📈 Go HIGHER!" (backwards) | None — silent logic bug |
| Guess the exact secret on an even-numbered attempt | "🎉 Correct!" / win | Marked wrong; Higher/Lower hint random | `int > str` comparison swallowed by `try/except TypeError`, falls back to string compare |
| Click "New Game 🔁" after losing | Fresh playable game | Game stays locked ("Game over"), score/history not cleared | None — `status` never reset, `st.stop()` fires |
| Open game on Easy (range 1–20) | Info shows "between 1 and 20" | Info always shows "between 1 and 100" | None |
| Make several wrong guesses | Score stays flat or drops | Score sometimes *rises* on a wrong guess | None — `update_score` adds +5 on even "Too High" |

---

## 2. How did you use AI as a teammate?

I used an AI coding assistant (Claude) as a pair programmer to locate the bugs,
refactor the logic into `logic_utils.py`, and generate the pytest cases. I drove
the process — choosing which bugs to fix first and reviewing every diff before
accepting it.

- **A correct suggestion:** The AI proposed having `check_guess` return only the
  outcome string (`"Win"`/`"Too High"`/`"Too Low"`) and moving the hint text into
  a separate `hint_for_outcome` helper. I verified this by running the starter
  tests, which assert `check_guess(60, 50) == "Too High"` — they only pass with
  a single-string return, so the split was clearly right.
- **A misleading suggestion:** An early suggestion was to "fix" the even-attempt
  branch by also casting the *guess* to a string so the types matched. That makes
  the comparison run without error but compares numbers lexicographically
  (`"9" > "100"` is `True`), so it doesn't actually fix anything. I rejected it
  and instead deleted the str-cast entirely so the comparison stays numeric,
  then added `test_string_comparison_regression` to prove `check_guess(9, 100)`
  returns "Too Low".

---

## 3. Debugging and testing your fixes

- I decided a bug was fixed only when (a) I could reproduce the old behavior, (b)
  a focused test failed on the old code and passed on the new code, and (c) the
  live Streamlit app behaved correctly.
- Concrete test: `test_string_comparison_regression` checks `check_guess(9, 100)
  == "Too Low"`. On the original code the even-attempt str-cast would have made
  this lexicographic ("9" > "100" → "Too High"), so the test pins down exactly
  the bug I removed. Running `pytest` went from 3 failing (NotImplementedError
  stubs) to 15 passing.
- AI helped me brainstorm edge cases I hadn't thought of — negative numbers,
  decimals, and very large values — which became the Challenge 1 test suite.

---

## 4. What did you learn about Streamlit and state?

Streamlit re-runs the *entire* script top-to-bottom on every interaction (every
button click or text entry). So any normal variable is recreated from scratch
each time — which is exactly why the secret number seemed to "change": calling
`random.randint` on a plain variable would re-roll it on every rerun. The fix is
`st.session_state`, a dictionary that survives reruns. I'd explain it to a friend
like this: the script is a recipe Streamlit re-cooks from the top every time you
touch anything, and `session_state` is the fridge where you stash things you want
to still be there next time.

---

## 5. Looking ahead: your developer habits

- **Habit to reuse:** writing a small failing test that reproduces a bug *before*
  fixing it, then watching it go green. It turns "I think it works" into proof.
- **Do differently:** I'd be more skeptical of AI fixes that make an error
  *disappear* without addressing the root cause (like the cast-the-guess-too
  suggestion) — running, not just reading, is what caught it.
- This project made me treat AI-generated code as a confident first draft, not a
  finished product: helpful for speed, but it needs a human to verify the logic
  and the edge cases.
