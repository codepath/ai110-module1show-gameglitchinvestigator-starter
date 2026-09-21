# AI Interactions Log

> **Stretch features only.** Only the sections below correspond to stretch work I actually
> attempted. SF11 is included but is explicitly scoped down to a *prompt* comparison
> rather than a two-model comparison — see the note in that section for why.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make
> multi-step changes autonomously.

I used agent mode twice: once for the repair refactor, and once to build a new feature.
The second is the one this stretch feature is about, but both are recorded because the
manual corrections are the interesting part.

### Run 2 — new feature: High Score tracker + Guess History sidebar

**What task did you give the agent?**

> "Add two features to the game. (1) A high score tracker that persists across rounds for
> the session, keeps a separate record per difficulty, and is beaten by a higher score or
> by an equal score in fewer attempts. (2) A Guess History panel in the sidebar showing
> each guess with its outcome. Put all the logic in `logic_utils.py` as pure functions so
> I can unit test it, keep `app.py` as rendering only, and add pytest cases for both."

**Files modified:** `logic_utils.py` (added `update_high_scores`, `format_high_scores`),
`app.py` (added `render_sidebar_history`, `render_sidebar_high_scores`, `high_scores`
session-state init, the new-record banner, and the import block),
`tests/test_game_logic.py` (added 13 cases).

**What did the agent do?**

- Added `update_high_scores()` returning a **new** dict rather than mutating the input,
  and explained why unprompted: the mapping lives in Streamlit session state, and
  mutating it in place would make my "is this a new record?" check in `app.py` compare an
  object against itself and never fire. It also wrote the test that pins that
  (`test_update_high_scores_does_not_mutate_its_input`). Good catch — I had written the
  banner check as `!=` against the previous value and would have shipped a banner that
  never appeared.
- Added `format_high_scores()` sorting best-score-first with attempts as the tie-break.
- Wired the sidebar panels and a "Reset high scores" button.
- Correctly identified that `start_new_game()` must **not** reset `high_scores`, and left
  a comment saying so at the one place a future edit would get it wrong.

**What did you have to verify or fix manually?**

Being straight about this one: on the feature run the generated logic was correct first
time, and the thing that was wrong was **mine**.

- **My own test expectations were wrong, not the code.** For the Hot/Cold bands I wrote
  the expected labels by doing the fractions in my head, and asserted that a guess 25
  away from 50 (in a 1–100 range) was "Cold" and one 49 away was "Freezing". Two tests
  failed. Working the arithmetic properly: 25/99 = 0.253, which lands in "Warm", and
  49/99 = 0.495, which lands in "Cold". The code was right. I corrected the assertions
  and wrote the real fractions into a comment so the next reader does not repeat the
  mistake.
- **That failure exposed a real gap.** Chasing it, I realised nothing in a 1–100 game
  with a secret of 50 can ever be more than 0.495 of the span away, so "Freezing" is
  *unreachable* unless the secret sits near an edge. Added
  `test_every_band_is_reachable_for_some_guess` so no band can silently become dead code.
- **A rendering surprise worth knowing.** `st.info("🧊 Cold")` shows up in a test trace as
  just `Cold`, because Streamlit detects a leading emoji and moves it into the callout's
  icon slot. I nearly "fixed" a bug that did not exist; the emoji renders fine, and it is
  visible in the sidebar and table rows where it is part of the string rather than the
  message head.
- Verified everything with a scripted `AppTest` run: win on the first guess, confirm the
  record and the banner, click New Game, confirm the record survives, win again more
  weakly, confirm the record does *not* change, switch difficulty, confirm a separate
  record, then click Reset and confirm the table empties.

### Run 1 — the repair refactor

**What task did you give the agent?**

Claude Code in agent mode, with `app.py`, `logic_utils.py` and `tests/test_game_logic.py`
in context. The instruction was deliberately multi-step rather than a single edit:

> "Move `check_guess`, `parse_guess`, `get_range_for_difficulty` and `update_score` from
> `app.py` into `logic_utils.py`, fix the inverted high/low hint, remove the
> string-comparison fallback, and update the imports in `app.py` so the UI file has no
> game logic left in it."

**Files modified:** `logic_utils.py`, `app.py`, `tests/test_game_logic.py`, `conftest.py`.

**What did the agent do?**

- Moved all four functions into `logic_utils.py` and replaced the `NotImplementedError`
  stubs, keeping the docstrings that were already there.
- Rewrote `check_guess` to return a bare outcome constant instead of an
  `(outcome, message)` tuple, and added `hint_message(outcome)` to derive the wording — a
  design change I had not asked for, and the best idea in the session (see `reflection.md`
  section 2).
- Replaced the `attempt_limit_map` dict in `app.py` with a single `DIFFICULTIES` table in
  `logic_utils.py`, so a difficulty's range and its attempt budget can't drift apart.
- Rewrote the import block in `app.py` and removed the now-dead function bodies.
- Consolidated the state resets into one `start_new_game()` function.

**What did you have to verify or fix manually?**

- **Rejected its bug-2 approach.** Its first pass made `check_guess` silently coerce a
  stringified secret with `int(str(secret))`. That hides a type error in the logic layer —
  the same mistake as the original `except TypeError`. I kept the root fix in `app.py`
  (stop stringifying the secret) and made `_to_int()` raise loudly on non-numeric input.
- **Fixed a crash it introduced.** Its `parse_guess` rewrite caught only `ValueError`, but
  `float("1e999")` is `inf` and `int(inf)` raises `OverflowError`, which would have taken
  the page down. Added a `math.isinf` / `math.isnan` guard.
- **Corrected a false factual claim.** It documented a `.strip()` fix as being needed
  because `" 42"` failed to parse. Python's `int()` already strips whitespace, so that had
  never been broken. Corrected the comment and the test.
- **Finished a fix it only claimed.** The stale "Attempts left" banner was still stale
  after its edits, because the banner renders near the top of the script and the guess is
  processed further down. I rewrote it using an `st.empty()` slot filled at the end of the
  script.
- **Fixed a syntax error in its output.** Its `conftest.py` had an unterminated
  triple-quoted docstring; `pytest` refused to collect until I closed it.
- Reviewed every hunk of the diff before keeping it, and re-ran the full suite plus a
  scripted `AppTest` replay of the whole bug log after each change.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

Prompting note: asking for "tests for this function" produced tests that described the
code's current shape. Asking for **"pytest cases that would fail against the *old* buggy
`check_guess`"** produced tests about the *bugs*, which is what I actually wanted. Every
row below was verified by running the assertion against the original buggy implementation
— an assertion that passes against the bug it claims to cover is worthless.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Hint direction for a too-high guess | "Write a pytest case that fails against the old `check_guess`, where 60 vs secret 50 returned ('Too High', 'Go HIGHER!')" | Assert `"LOWER" in hint_message(check_guess(60, 50))` and `"HIGHER" not in` it | ✅ Passes now; **fails** against old code | Kept as written. The negative half of the assertion matters — without it, a message containing both words would slip through. |
| Lexicographic vs. numeric comparison | "The secret is sometimes a str. Generate cases where a string compare and a numeric compare disagree." | Parametrised `(9, "50") -> TOO_LOW` and `(100, "50") -> TOO_HIGH` | ✅ Passes now; **fails** against old code | Kept. These are the two exact inputs from my bug log; `"9" > "50"` and `"100" < "50"` are both true as text and both wrong as numbers. |
| Score parity bug | "Write a test showing Too High and Too Low cost the same" | `assert update_score(50, TOO_HIGH, 1) == update_score(50, TOO_LOW, 1)` | ✅ Passed — **but also passed against the buggy code** | **Rewrote.** The old code charged −5 for both at attempt 1, so this test caught nothing. The parity bug only appears on even attempts. Parametrised over attempts 1–4 and left a comment saying the parameter is load-bearing. |
| Score floor | "Can the score go negative?" | Loop four wrong guesses, assert `score >= 0` after each | ✅ Passes now; **fails** against old code (reaches −20) | Kept. Asserting inside the loop rather than only at the end tells me *which* attempt broke the invariant. |
| First-guess win value | "Is the win bonus correct?" | `assert update_score(0, WIN, 1) == 100` | ✅ Passes now; **fails** against old code (returns 80) | Kept. Exposed an off-by-two: the old formula was `100 - 10 * (attempt_number + 1)` *and* `app.py` had already incremented the counter. |
| Blank vs. whitespace-only input | "Enumerate every falsy-ish input `parse_guess` should reject" | Parametrise `["", "   ", None]`, all expecting `"Enter a guess."` | ✅ Passes now; the `"   "` case **fails** against old code | Kept. Good catch by the AI: the original only tested `raw == ""`, so `"   "` fell through to `int("   ")` and got the wrong error message. |
| Surrounding whitespace | (AI volunteered: "the original never calls `.strip()`, so `' 42'` fails") | `assert parse_guess(" 42 ") == (True, 42, None)` | ✅ Passed — **but also passed against the buggy code** | **Demoted.** The AI's premise was false: Python's `int()` already strips whitespace, so this was never a bug. Kept as an explicitly-labelled guard, not a regression test, and corrected the code comment it had talked me into writing. |
| Fractional guess | "What does `parse_guess('3.9')` do and is that right?" | Assert `"3.9"` is rejected rather than truncated | ✅ Passes now; **fails** against old code (silently returns 3) | Kept, and added the inverse case `"42.0" -> 42`, which the AI had not suggested — rejecting decimals outright would have been too blunt. |
| Full-width Unicode digits | "Any non-obvious non-numeric strings worth testing?" | Assert `"4２"` is rejected as not a number | ❌ **Failed** | **The test was wrong, not the code.** `int()` accepts any Unicode decimal digit, so `int("4２") == 42`. Rather than adding code to reject it, I inverted the assertion and kept it as `test_full_width_digits_are_accepted_because_python_int_accepts_them`, with a docstring recording the mistaken assumption. Deleting it would have erased the lesson. |
| Huge exponent input | (Mine, not the AI's) | `parse_guess("1e999")` should be rejected, not crash | ❌ **Failed** initially | Found a crash **the AI's own fix had introduced**: `float("1e999")` is `inf`, `int(inf)` raises `OverflowError`, and the function only caught `ValueError`. Added a `math.isinf` / `math.isnan` guard. |
| Every difficulty actually winnable | (Mine, prompted by the AI's `DIFFICULTIES` refactor) | — | ✅ Passes | The AI's idea of one table for range + attempts made me realise they're a single coupled decision. Wrote `test_every_difficulty_is_winnable_by_binary_search` (asserting `ceil(log2(range)) <= attempt_limit`) and `test_binary_search_actually_wins_every_secret_in_range`, which plays a full perfect game against every secret in every difficulty navigating only by `check_guess` hints. Inverted hints would make it never converge. |

Edge cases added later, alongside the stretch features:

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Proximity band boundaries | "Write tests pinning each Hot/Cold band boundary for a secret of 50 in a 1-100 range" | A list comparison of labels for guesses 50, 52, 60, 75, 99 | ❌ **Failed** | **My expectations were wrong, not the code.** I had guessed "Cold" for 25 away and "Freezing" for 49 away; the real fractions are 0.253 ("Warm") and 0.495 ("Cold"). Corrected the assertions and wrote the fractions into a comment. |
| Unreachable band | (Mine, found by chasing the failure above) | `test_every_band_is_reachable_for_some_guess` | ✅ Passes | Nothing in a 1-100 game with a secret of 50 is more than 0.495 of the span away, so "Freezing" only appears when the secret is near an edge. This test proves no band is dead code. |
| Degenerate range | "What happens if low == high?" | `proximity_label(5, 5, 5, 5)` should not raise | ✅ Passes | Good catch — the span would be 0 and the division would raise `ZeroDivisionError`. The `max(1, high - low)` guard was written because of this test. |
| Range-relative proximity | "Prove the label means the same thing at different difficulties" | Same absolute distance on Easy vs Hard yields different labels | ✅ Passes | The whole point of normalising. 9 away is "Cold" on Easy (1-20) and "Blazing hot" on Hard (1-200). |
| High-score tie-breaking | "Generate cases for equal score with fewer and with more attempts" | Two tests covering both directions of the tie | ✅ Passes | Kept both. Only testing the "fewer attempts" direction would let a `>=` comparison slip through and overwrite a better record. |
| Session-state mutation | "This dict lives in Streamlit session state — what could go wrong?" | `test_update_high_scores_does_not_mutate_its_input` | ✅ Passes | The strongest suggestion of the batch. If the function mutated in place, `app.py`'s "is this a new record?" check would compare an object against itself and the banner would never fire. |

**Outcome:** 3 starter tests kept verbatim and passing, 80 added, 83 total. 10 of 10
regression assertions confirmed to fail against the original buggy implementations.

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Run flake8, ruff and black against app.py, logic_utils.py, conftest.py and tests/.
For each violation, tell me what the rule means and whether fixing it is a real
readability improvement or just satisfying the tool. Then add Google-style docstrings
(Args/Returns) to every public function in logic_utils.py.
```

**Linting output before:**

```
$ flake8 --max-line-length=88 app.py logic_utils.py conftest.py tests/
app.py:188:1: E302 expected 2 blank lines, found 1
logic_utils.py:54:89: E501 line too long (89 > 88 characters)
logic_utils.py:65:89: E501 line too long (90 > 88 characters)
tests/test_game_logic.py:48:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:53:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:200:89: E501 line too long (91 > 88 characters)

6 violations total: 3x E501 (line too long), 3x E302 (expected 2 blank lines)
```

**Linting output after:**

```
$ flake8 --max-line-length=88 app.py logic_utils.py conftest.py tests/
(no output -- 0 violations)

$ ruff check --line-length=88 app.py logic_utils.py conftest.py tests/
All checks passed!

$ black --check --line-length=88 app.py logic_utils.py conftest.py tests/
All done! ✨ 🍰 ✨
4 files would be left unchanged.
```

Full before/after is committed at [`docs/lint_report.txt`](docs/lint_report.txt).

**Changes applied:**

| AI suggestion | Applied? | Reasoning |
|---|---|---|
| Wrap the two long `DIFFICULTIES.get(...)` lookups in `logic_utils.py` (E501) | ✅ Yes | Genuine readability win — the fallback argument is easier to see on its own line. |
| Add the missing blank line before `render_round_summary` in `app.py` (E302) | ✅ Yes | Standard PEP 8 spacing; no argument against it. |
| Add blank lines between the three **starter** tests (E302) | ✅ Yes, with a caveat | I had said I was keeping the starter tests "verbatim". Adding blank lines changes only whitespace, not a single assertion, so the claim still holds — but it is worth naming rather than quietly breaking. |
| Wrap the long `assert ... , f"..."` message in the binary-search test (E501) | ✅ Yes | Parenthesising the message is the conventional fix. |
| Run `black` over everything | ✅ Yes | It only joined two wrapped calls that fit on one line and adjusted blank lines around comment banners. Cosmetic, and being formatter-clean is worth more than my line-break preferences. |
| Add Google-style `Args:`/`Returns:` docstrings to public functions in `logic_utils.py` | ✅ Yes | Applied to all public functions. The private `_to_int` keeps a prose docstring since its contract is "coerce or raise". |
| Rename `low`/`high` to `lower_bound`/`upper_bound` throughout | ❌ **No** | Rejected. `low` and `high` are used consistently across `app.py`, `logic_utils.py` and the tests, and match the domain language ("too high", "too low"). The rename would have touched ~40 call sites to make the names longer, not clearer. |
| Add type hints to every parameter | ❌ **Partially** | Applied where the type is genuinely fixed (`low: int`, `difficulty: str`). Deliberately **not** on `guess`/`secret` in `check_guess` and `_to_int`, whose entire job is to accept a loosely-typed value and normalise it — annotating them `int` would document a contract the function intentionally does not enforce at the boundary. |

---

## Model / Prompt Comparison (SF11)

> **Scope note, stated up front:** the stretch feature asks for a comparison of two
> different *models* (e.g. GPT-4o vs Gemini). Only one model was available to me while
> doing this work, so a two-model comparison is **not** claimed here — writing down what
> I imagine Gemini would have said would make this log fiction, which defeats the point
> of keeping it. What follows is a real comparison of two *prompting strategies* issued
> to the same model on the same bug, which I did actually run. Marked incomplete in the
> README's stretch checklist.

**Task given to both prompts:** the scoring bug in `update_score` — "Too High" paid +5 on
even attempts and −5 on odd ones, and the total could go negative.

| | Prompt A (naive) | Prompt B (evidence-led) |
|-|------------------|-------------------------|
| **Prompt text** | "Fix the scoring bug in `update_score`." | "Here is a trace: four wrong guesses against secret 50 gave scores −5, −10, −15, −20, and `update_score(0,'Too High',2)` returns 5 while `update_score(0,'Too High',3)` returns −5. Explain why, then propose a fix, then write a pytest case that fails against the current code." |
| **Response summary** | Rewrote the function and clamped the score at 0. Fixed the negative-score symptom but **kept the `attempt_number % 2` branch**, so "Too High" still paid differently depending on parity. Confidently described the result as "fixed". | Identified all three defects separately: the parity branch, the missing floor, and the off-by-two in the win bonus (`100 - 10 * (attempt_number + 1)` applied to an already-incremented counter, so a first-guess win paid 80). Proposed one fix per defect and wrote a test for each. |
| **More Pythonic?** | Roughly equal — both produced clean, readable code. Prompt A's output was actually *shorter*, which is what made it deceptive. | Slightly longer but each branch is justified by a named defect. |
| **Clearer explanation?** | **No.** It asserted the fix worked without saying what had been wrong. | **Yes.** Walking from observed numbers to causes meant I could check each claim against the trace myself. |

**Which did you prefer and why?**

Prompt B, decisively — and the interesting part is that both prompts went to the *same
model*, so the difference is entirely in what I gave it. Prompt A produced code that
passed a casual look and still had the original parity bug in it; if I had accepted it I
would have "fixed" the score and shipped a game where a "Too High" on attempt 2 was worth
10 points more than the same guess on attempt 3. Prompt B found a third bug (the win
bonus off-by-two) that I had not even listed.

The lesson generalises past this assignment: the quality of what came back tracked the
quality of the *evidence* I handed over far more than the phrasing of the request.
Pasting the actual numbers, and asking for an explanation *before* a fix, was worth more
than any amount of prompt wording.

**To complete this stretch feature properly** you would run the Prompt B text above
against a second model (ChatGPT, Gemini, Copilot) and add a third column comparing its
output for Pythonic-ness and clarity.
