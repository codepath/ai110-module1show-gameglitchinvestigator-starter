# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran `python -m streamlit run app.py` the game *looked* finished. The
sidebar had a difficulty picker, the main panel had a guess box, a Submit button, a New
Game button, and a "Developer Debug Info" expander. Nothing crashed on load, which is
exactly what made it dangerous — every bug was a wrong *answer*, not a stack trace. I
opened the debug expander so I could see the secret number, then played on purpose
against a known secret so I could tell the difference between bad luck and bad code.

Six concrete bugs I found:

1. **The hints are backwards.** With the secret at 50, guessing 60 told me
   "📈 Go HIGHER!" and guessing 40 told me "📉 Go LOWER!" In `check_guess`, the branch
   that correctly detects `guess > secret` and labels it `"Too High"` is paired with the
   *"Go HIGHER!"* message, and vice versa. The classification was right; the advice
   attached to it was swapped.
2. **The secret changes type on every other guess.** `app.py` does
   `if st.session_state.attempts % 2 == 0: secret = str(st.session_state.secret)`. On
   even attempts the secret becomes a string, so `guess > secret` raises a `TypeError`,
   which a bare `except TypeError` swallows and "recovers" from by comparing
   `str(guess) > secret` — a *lexicographic* comparison. That is why guessing 9 against a
   secret of 50 was called too high ("9" sorts after "50") and guessing 100 was called too
   low ("100" sorts before "50"). Two bugs stacked: the wrong comparison, then the wrong
   message.
3. **The score goes haywire and goes negative.** `update_score` subtracts 5 for every
   "Too Low" but for "Too High" it adds 5 on even attempts and subtracts 5 on odd ones —
   so the reward depends on *when* you guessed, not *what* you guessed. Four honest
   wrong guesses left me at a score of −15.
4. **"New Game" does not start a new game.** The handler resets `attempts` and `secret`
   but never resets `score`, `status`, or `history`. Because `status` is still `"won"`,
   the very next rerun hits `st.stop()` and prints "You already won. Start a new game to
   play again." — clicking the only button that could fix it. After one win the app is
   permanently unplayable. It also reseeds with a hardcoded `random.randint(1, 100)`,
   ignoring the difficulty range entirely.
5. **Changing difficulty makes the game unwinnable.** The secret is only generated once,
   inside `if "secret" not in st.session_state`. Switching from Normal to Easy narrows the
   range to 1–20 but leaves the old secret (87 in my run) in place, so no legal guess can
   ever match. The info banner is also hardcoded to "between 1 and 100" no matter which
   difficulty is selected — the game lies about its own rules.
6. **Attempt counting is off by one and punishes typos.** `attempts` is initialised to
   `1` instead of `0`, so a fresh Normal game advertises "Attempts left: 7" out of 8
   before you have guessed anything. `attempts += 1` also runs *before* `parse_guess`, so
   typing `abc` burns a turn. And because the banner is rendered earlier in the script
   than the increment, the number shown is always one rerun stale.

On top of that, the starter `pytest` suite failed 3/3: every function in `logic_utils.py`
was a `raise NotImplementedError` stub, and all the real logic lived in `app.py` where no
test could import it without booting Streamlit.

**Terminal trace of the broken game**

This is the actual recorded run of the **original, pre-fix** `app.py`, driven through the
Streamlit runtime with the secret pinned so the same inputs reproduce every time. Each
block prints the real `st.session_state` after the click plus whatever the page rendered.
Nothing below is paraphrased — this is what the broken game did.

```text
$ python -m streamlit run app.py      # ORIGINAL, PRE-FIX CODE

### Session A -- Normal difficulty, secret pinned to 50 via Developer Debug Info
[page load, before any guess]
    session_state: secret=50 (int)  attempts=1  score=0  status=playing
    INFO    Guess a number between 1 and 100. Attempts left: 7
[typed 60 -> Submit Guess]
    session_state: secret=50 (int)  attempts=2  score=5  status=playing
    INFO    Guess a number between 1 and 100. Attempts left: 7
    HINT    Go HIGHER!
[typed 40 -> Submit Guess]
    session_state: secret=50 (int)  attempts=3  score=0  status=playing
    INFO    Guess a number between 1 and 100. Attempts left: 6
    HINT    Go LOWER!

### Session B -- the same secret, but landing on an EVEN attempt
[typed 9 -> Submit Guess  (attempt 2, even)]
    session_state: secret=50 (int)  attempts=2  score=5  status=playing
    HINT    Go HIGHER!
[typed 100 -> Submit Guess  (attempt 2, even)]
    session_state: secret=50 (int)  attempts=2  score=0  status=playing
    HINT    Go LOWER!

### Session C -- four honest wrong guesses, watching the score
    guess  40 -> score=-5
    guess  30 -> score=-10
    guess  20 -> score=-15
    guess  10 -> score=-20

### Session D -- win, then click New Game
[typed abc (not a number) -> Submit Guess]
    session_state: secret=50 (int)  attempts=2  score=0  status=playing
    ERROR   That is not a number.
[typed 50 -> Submit Guess]
    session_state: secret=50 (int)  attempts=3  score=60  status=won
    SUCCESS You won! The secret was 50. Final score: 60
[clicked New Game]
    session_state: secret=15 (int)  attempts=0  score=60  status=won
    SUCCESS You already won. Start a new game to play again.

### Session E -- switch difficulty mid-game (Normal secret 87 -> Easy, range 1-20)
[switched difficulty to Easy]
    session_state: secret=87 (int)  attempts=1  score=0  status=playing
    INFO    Guess a number between 1 and 100. Attempts left: 5
[typed 10 -> Submit Guess]
    session_state: secret=87 (int)  attempts=2  score=-5  status=playing
    HINT    Go LOWER!
[typed 20 -> Submit Guess]
    session_state: secret=87 (int)  attempts=3  score=-10  status=playing
    HINT    Go LOWER!
[typed 5 -> Submit Guess]
    session_state: secret=87 (int)  attempts=4  score=-15  status=playing
    HINT    Go LOWER!
```

Reading that trace, in order: the page opens claiming 7 of 8 attempts before I have
touched anything (`attempts=1`). Guessing **60** against 50 is told to go **HIGHER**.
Guessing **9** against 50 is *also* told to go HIGHER, and guessing **100** is told to go
LOWER — both backwards, and note `secret` is still an `int` in session state, so the
string coercion is happening inside the submit handler, not to the stored value. Four
wrong guesses drive the score to **−20**. Typing `abc` moves `attempts` from 1 to 2, so
the typo cost a turn. And after winning, **New Game** hands back `score=60 status=won`
and the page answers with "You already won" — the reset button is what jams the app.
Session E is the killer: `secret=87` while the Easy range is 1–20, so no legal guess can
ever match, and the banner still insists the range is 1 to 100.

And the starter test suite, before any of my changes:

```text
$ python -m pytest tests/    # ORIGINAL, PRE-FIX CODE
E       NotImplementedError: Refactor this function from app.py into logic_utils.py

logic_utils.py:21: NotImplementedError
=========================== short test summary info ============================
FAILED tests/test_game_logic.py::test_winning_guess - NotImplementedError: Re...
FAILED tests/test_game_logic.py::test_guess_too_high - NotImplementedError: R...
FAILED tests/test_game_logic.py::test_guess_too_low - NotImplementedError: Re...
============================== 3 failed in 0.03s ===============================
```

**Bug Reproduction Log**

Reproduced against a pinned secret of **50** on Normal difficulty (secret pinned via the
Developer Debug Info panel / `st.session_state.secret`) unless noted otherwise.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess of `60`, secret `50` (attempt 1) | Hint "Too High" → advice to go **lower** | Hint shown was "📈 Go HIGHER!" | none (silent wrong answer). Direct call: `check_guess(60, 50) -> ('Too High', '📈 Go HIGHER!')` |
| Guess of `40`, secret `50` (attempt 2) | Hint "Too Low" → advice to go **higher** | Hint shown was "📉 Go LOWER!" | none. Direct call: `check_guess(40, 50) -> ('Too Low', '📉 Go LOWER!')` |
| Guess of `9`, secret `50`, on an **even** attempt | "Too Low" → go higher | "📈 Go HIGHER!" — 9 was classified as *too high* | none, because `except TypeError` hides it. Raw comparison: `TypeError: '>' not supported between instances of 'int' and 'str'`; then `"9" > "50" -> True` |
| Guess of `100`, secret `50`, on an **even** attempt | "Too High" → go lower | "📉 Go LOWER!" — 100 was classified as *too low* | none. `"100" > "50" -> False` (lexicographic) |
| Four wrong guesses `40, 30, 20, 10` against secret `50` | Score never drops below 0 | Score ran `-5, -10, -15, -20` | none. `update_score(0,"Too Low",1) -> -5` |
| Guess of `60` (Too High) on attempt 2, then on attempt 3 | Same outcome scores the same either way | `+5` on attempt 2, `-5` on attempt 3 | none. `update_score(0,"Too High",2) -> 5` vs `update_score(0,"Too High",3) -> -5` |
| Win, then click **New Game 🔁** | Fresh game: score 0, attempts 0, playable | `score` stayed `60`, `status` stayed `"won"`; page showed "You already won. Start a new game to play again." and `st.stop()` fired — app permanently stuck | none |
| Start on Normal (secret `87`), switch difficulty to **Easy** (range 1–20), guess `10`, `20`, `5` | Secret reseeded into 1–20; game winnable | Secret stayed `87`; every guess returned "📉 Go LOWER!"; banner still read "Guess a number between 1 and 100" | none |
| Page load, Normal difficulty, before any guess | "Attempts left: 8" | "Attempts left: 7" | none (`attempts` initialised to `1`) |
| Guess of `abc` | Error message, attempt **not** consumed | "That is not a number." shown, but `attempts` advanced `1 → 2` | `That is not a number.` (handled, no traceback) |
| `python -m pytest tests/` on the starter code | 3 passed | 3 failed | `NotImplementedError: Refactor this function from app.py into logic_utils.py` |

---

## 2. How did you use AI as a teammate?

**Tool used:** Claude Code (agent mode) in the terminal, with `app.py`, `logic_utils.py`
and `tests/test_game_logic.py` in context so it could see how the UI file and the logic
file related to each other. I worked one bug per chat session so the context stayed
focused, and I deliberately gave it multi-step instructions ("move `check_guess` into
`logic_utils.py`, fix the high/low bug, update the import in `app.py`") rather than
asking for one edit at a time.

The single most useful thing I did was **not** ask "fix this file".

### The AI's explanation of the bug

I highlighted the `except TypeError` block in `check_guess` and asked:

> **My prompt:** "Explain this logic step-by-step. Why is there a `try`/`except TypeError`
> around a comparison of two numbers, and what does the code inside the `except` branch
> actually do? Walk me through what happens with `check_guess(9, "50")`."

Its reply, quoted:

> **Claude Code:** "This `try`/`except` is not defending against anything hypothetical —
> it is load-bearing, and it is hiding a bug in the caller.
>
> 1. `app.py` passes `secret` as a `str` on every even-numbered attempt
>    (`secret = str(st.session_state.secret)`). So on those attempts `check_guess`
>    receives `guess=9` (an `int`) and `secret="50"` (a `str`).
> 2. The first line, `if guess == secret`, is `9 == "50"`. In Python that is not a type
>    error — it is simply `False`. An `int` is never equal to a `str`. So an exact
>    match on an even attempt silently fails to register as a win.
> 3. `if guess > secret` then raises `TypeError: '>' not supported between instances of
>    'int' and 'str'`. This is the interpreter correctly telling you the caller is wrong.
> 4. The `except TypeError` swallows that signal and retries as `str(guess) > secret` —
>    `"9" > "50"`. That is a **lexicographic** comparison: Python compares `"9"` against
>    `"5"` character by character, and `"9"` sorts after `"5"`, so the result is `True`.
>    The function concludes the guess is too high.
>
> So a guess of 9 against a secret of 50 is reported as *too high*. The error handler
> converts a loud, correct type error into a quiet, confident wrong answer. Note this is
> separate from the fact that the outcome/message pairs are also swapped — you have two
> independent bugs producing wrong hints, and fixing only one will leave the other."

That last sentence is the part I would have missed. I had already spotted the swapped
message strings and would have "fixed the hints", declared victory, and shipped a game
that still lied on every even guess. Its explanation is what told me the bug was two bugs
stacked on top of each other, and I confirmed every step of it in a REPL before trusting
it — `9 == "50"` really is `False`, and `"9" > "50"` really is `True`.

### An AI suggestion that was correct

**What it suggested:** rather than just swapping the two message strings, restructure
`check_guess` so it returns *only* an outcome constant (`WIN` / `TOO_HIGH` / `TOO_LOW`)
and add a separate `hint_message(outcome)` that looks the player-facing wording up from
that outcome. Its argument was that the bug was possible in the first place because the
rule and its wording were hand-written next to each other, so a typo in either one
produced a confident wrong answer with nothing to catch it.

**Why it was right, and how I verified it:** this is a structural fix, not a patch — once
the advice is derived from the outcome, "Too High" *cannot* be paired with "go HIGHER"
because nobody writes that pairing by hand any more. I verified it three ways:

1. The three starter tests in `tests/test_game_logic.py` assert
   `check_guess(60, 50) == "Too High"` — a bare string, not a tuple. They had been failing
   3/3 against the `NotImplementedError` stubs, and they pass now **unmodified**, which
   told me the starter tests had been written against this design all along.
2. I wrote `test_too_high_hint_tells_the_player_to_go_lower`, which asserts `"LOWER" in`
   the hint and `"HIGHER" not in` it.
3. In the running app, secret 50 with a guess of 60 now shows "📉 Too high -- go LOWER!".

### An AI suggestion I did not accept as written

There were several. The most interesting one was a suggestion I *liked* and still had to
reject; the most embarrassing one was a factual claim I believed for about ten minutes.

**The rejected design.** Its first pass at bug 2 was to make `check_guess` quietly coerce
whatever it received — `int(str(secret))` — so that a stringified secret would "just
work". That does make the symptom disappear, and it's tempting because it's a one-line
change. I rejected it because it is the *same mistake as the original bug*: it hides a
type error inside the logic layer instead of surfacing it. The real defect was in `app.py`
stringifying the secret at all, and silently tolerating it would have left a booby trap
for the next person who passed in something genuinely wrong. What I kept instead: the root
fix in `app.py` (stop stringifying), plus a `_to_int()` helper in `logic_utils.py` that
coerces *numeric* input but **raises `TypeError` loudly** on anything else.
`test_non_numeric_input_raises_instead_of_guessing` pins that, and the comment I left in
the code says why: a wrong hint is worse than a crash.

I also rejected the minimal version of the bug-1 fix — just swapping the two message
strings in place and keeping the `(outcome, message)` tuple. It's two characters of diff
and it works, but it leaves the rule and the wording adjacent so they can drift apart
again, and it would have left the starter tests failing, since they assert a bare string.

**The claim that was simply wrong.** While fixing `parse_guess`, the AI told me the
original never called `.strip()`, so an input of `" 42"` failed with "That is not a
number." I wrote that into a code comment and into a test called
`test_surrounding_whitespace_is_tolerated`. Then I ran the assertion against the
*original* function and it **passed** — meaning the test caught nothing. Python's built-in
`int()` has always stripped surrounding whitespace, so `int(" 42 ")` was fine and `" 42"`
had never been broken. I corrected the comment in `logic_utils.py`, downgraded that test
to a guard with a note saying it is not a regression test, and found the *real* whitespace
bug while I was in there: the original only compared `raw == ""`, so whitespace-only input
fell through to `int("   ")` and got told "That is not a number." instead of "Enter a
guess." That is now `test_whitespace_only_input_asks_for_a_guess_rather_than_scolding`.

Two smaller ones, for the record, because they show the same pattern:

- It suggested a test asserting that `"4２"` (an ASCII 4 and a full-width 2) should be
  rejected as non-numeric. It is not: `int()` understands any Unicode decimal digit, so
  `int("4２") == 42`. The test failed, and the *test* was wrong, not the code. I kept it
  as `test_full_width_digits_are_accepted_because_python_int_accepts_them` with a docstring
  explaining the mistake, because deleting it would have erased the lesson.
- Its rewrite of `parse_guess` introduced a **new** crash: `float("1e999")` is `inf`, and
  `int(inf)` raises `OverflowError`, which the function only caught `ValueError` for. That
  would have taken the whole page down on a silly input. My own edge-case test found it and
  I added the `math.isinf` / `math.isnan` guard.

The pattern across all of these: the AI was reliably good at *structure* and reliably
unreliable about *specific runtime facts*. Its refactor advice was better than mine. Its
claims about what Python actually does needed to be executed before I believed them.

---

## 3. Debugging and testing your fixes

**How I decided a bug was really fixed.** A passing test was not enough, because a test
written *after* the fix will happily pass without ever having been capable of failing. So
for every regression test I added, I copied the original buggy `check_guess`,
`update_score` and `parse_guess` into a scratch file and ran the new assertions against
**those**. The rule I used: if an assertion does not fail against the old code, it is not
a regression test and I do not get to claim it covers that bug.

That check paid for itself immediately — it caught two worthless tests:

1. `test_too_high_and_too_low_cost_the_same` originally only compared the two outcomes at
   attempt 1. The old buggy code charged −5 for both at attempt 1, so my test passed
   against the bug it was supposed to catch. The parity bug only shows up on *even*
   attempts (+5 for Too High, −5 for Too Low). I parametrised the test over attempts 1–4,
   and left a comment in the test explaining why the parameter is load-bearing.
2. The whitespace test described in section 2, which was testing a bug that had never
   existed.

Final result: **10 of 10** of my regression assertions fail against the original code and
pass against the repaired code.

**A test that taught me something about my own code.** The one I'm most glad I wrote is
`test_binary_search_actually_wins_every_secret_in_range`. Instead of checking one guess in
isolation, it plays a *complete* perfect game against every possible secret in every
difficulty, narrowing the range using nothing but the outcomes `check_guess` hands back:

```python
guess = (lo + hi) // 2
outcome = check_guess(guess, secret)
if outcome == TOO_HIGH: hi = guess - 1
else:                   lo = guess + 1
```

If the hints were inverted, this loop would walk *away* from the answer and never
converge. That makes "the hints lie" a test failure rather than something you have to
notice by playing. Writing it also forced me to realise the attempt limits and the ranges
were a single coupled decision, not two independent settings — which is how I caught that
"Hard" (1–50) was narrower than "Normal" (1–100), i.e. the hardest setting was the
easiest. That turned into `minimum_attempts_needed()` and
`test_every_difficulty_is_winnable_by_binary_search`, which asserts no difficulty can ever
advertise fewer attempts than `ceil(log2(range))`. The original "impossible game" bug is
now impossible to reintroduce without a red test.

**Manual verification too.** Unit tests can't see a Streamlit state bug, so I also scripted
a replay of every row of my Bug Reproduction Log through the real Streamlit runtime using
`AppTest`, asserting on `st.session_state` after each click: score never negative, invalid
input never consuming an attempt, New Game genuinely resetting score/status/history,
switching difficulty reseeding the secret inside the new range. That replay is what caught
a fix I had *claimed* but not actually made: I wrote in my commit notes that the
"Attempts left" banner was no longer stale, but the replay showed it still reading
"Attempts left: 8" immediately after the first guess. The banner was being rendered near
the top of the script, before the guess further down had been processed. I fixed it
properly with an `st.empty()` slot filled at the end of the script, and re-ran the replay
to confirm it now counts 7, 6, 5. Then I booted `streamlit run app.py` for real and
confirmed a clean startup with no exceptions in the server log.

**Did AI help with the tests?** Yes, and unevenly in a way that's worth being precise
about. It was genuinely good at *enumerating* edge cases I hadn't considered — empty
string vs. whitespace-only vs. `None`, range boundaries, unknown difficulty, unknown score
outcome, decimal-but-whole input like `"42.0"`. Prompting it with "generate pytest cases
that would fail against the *old* `check_guess`" produced a much better list than "write
tests for this function", because it forced the tests to be about the bugs rather than
about the code's current shape. But its actual assertions were wrong often enough that I
rewrote most of them — see the full-width digit case in section 2, where the AI's expected
value was simply not what Python does. I used it for coverage ideas and wrote the
assertions myself.

One more habit that mattered: `pytest` didn't run at all in the starter layout, and not
for the reason the assignment implies. Even with `logic_utils.py` implemented, bare
`pytest` — the exact command the instructions give — died at collection with
`ModuleNotFoundError: No module named 'logic_utils'`, because `logic_utils.py` is in the
repo root and pytest only puts the *test* file's directory on `sys.path`. It only appeared
to work if you typed `python -m pytest` from the repo root, which adds the current
directory for you. I added `conftest.py` and `pytest.ini` so all four invocation forms
work from any directory. I would never have found that if I'd only ever run the tests one
way.

---

## 4. What did you learn about Streamlit and state?

Here's how I'd explain it to a friend who's never touched Streamlit.

Most UI frameworks work like a house: you build it once, and when someone flips a switch
you go change that one light. Streamlit works like a **whiteboard you redraw from
scratch**. Every time you click a button, move a slider, or type in a box, Streamlit
throws away the whole page and **re-runs your entire Python file from line 1 to the last
line**. Your script isn't a program that sits there waiting for events — it's a recipe
that gets re-cooked, start to finish, on every single interaction.

That explains the thing that confuses everyone first: *every ordinary variable is wiped
every time.* If you write `secret = random.randint(1, 100)` at the top of the file, you
haven't picked a secret number — you've picked a new one on every click, forever. The
number is unguessable not because the logic is wrong but because the script restarted.

`st.session_state` is the sticky note you leave on the desk *next to* the whiteboard. It's
the one thing that survives a rerun. So the pattern is: "if I haven't written this note
yet, write it; otherwise read the note I left last time."

```python
if "secret" not in st.session_state:          # only on the very first run
    st.session_state.secret = random.randint(low, high)
```

The three things that actually bit me in this project, none of which I'd have predicted:

1. **`if "x" not in session_state` means "only ever once".** That guard is how you stop a
   value being regenerated — but it's *also* why the secret never updated when I changed
   difficulty. Initialisation-once and never-reinitialise are the same line of code, so
   "set this once at startup" and "this can never respond to a setting change" are the
   same decision. I needed a second, explicit trigger (`if stored_difficulty != current`)
   to re-seed it.
2. **Order in the file is order in time.** Because the script runs top to bottom, anything
   you print *above* your event handler is printed using the state from *before* this
   click was handled. That's the whole story of my stale "Attempts left" banner: the code
   was correct, it just ran too early. The fix isn't better logic, it's reserving the spot
   with `st.empty()` and filling it at the bottom once the guess has been counted. "Where
   it appears on screen" and "when it's computed" are separate concerns in Streamlit, and
   `st.empty()` is how you separate them.
3. **`st.stop()` plus unreset state is a trap door.** The starter's New Game button reset
   `attempts` and `secret` but left `status = "won"`. On the next rerun the status check
   ran *before* anything else and called `st.stop()`, so the app halted early every single
   time — the button that was supposed to rescue you was what kept you stuck. Forgetting
   *one* key in a multi-key reset broke the app permanently. That's why I moved the reset
   into a single `start_new_game()` function: with a rerun model, partially-updated state
   isn't a cosmetic glitch, it's a locked door.

The bigger lesson: in Streamlit, a whole class of bug isn't in your logic at all. It's in
*when* your correct logic ran relative to the rerun. My unit tests couldn't see any of
these three — `logic_utils.py` was 60/60 green while the app was still visibly wrong —
which is exactly why I scripted the `AppTest` replay as well.

---

## 5. Looking ahead: your developer habits

**The habit I'm keeping: run the new test against the old code before I trust it.**

This is the one thing from this project I'd take into any codebase. When you write a test
after fixing a bug, the test has never once been capable of failing — you've only proved
it agrees with the code you just wrote. Actually running it against the broken version
takes two minutes and it is the only thing that proves the test *covers* anything. It
caught two dead tests for me here, one of which was guarding a bug that had never existed
in the first place. From now on, when I fix a bug, the order is: reproduce it, write the
test, watch the test **fail**, then fix it.

The second habit, which is really the same instinct: **reproduce before you read**. My
first move was to pin the secret number via the debug panel and play against a known
value, so I could tell "the code is wrong" apart from "I got unlucky". Every row in my Bug
Reproduction Log has a concrete input and a concrete observed output, which meant that
when I asked the AI for help I could hand it evidence rather than a vibe. "Guessing 9
against a secret of 50 reports Too High" got me a root cause in one exchange. "The hints
seem broken" would not have.

On Git: committing in phases (log the bugs → apply the fixes → write the docs) turned out
to be worth more than tidiness. The bug-log commit is a snapshot of the broken behaviour
with the `FIXME` markers still in place, so the diff of the next commit reads as "here is
exactly what each marker turned into". The history explains the reasoning, not just the
result.

**What I'd do differently: stop asking the AI what Python does.**

I lost time believing a confident, specific, wrong factual claim — that `int(" 42")`
fails. It sounded plausible, it was delivered with no hedging, and it was easy to check in
a one-line REPL call that I didn't make. Next time I'll split my prompts by what the model
is actually good at: ask it for *structure* ("how should I separate this rule from its
presentation?", "what edge cases am I not thinking of?") where it was consistently better
than me, and never accept a claim about runtime behaviour without executing it first. A
model's confidence carries no information about whether it's right, and the only reason I
caught the wrong ones here is that I was running things.

I'd also front-load asking "explain this step by step" before asking for any edit. The
`except TypeError` explanation is what turned one bug into two, and I nearly skipped
straight to "fix it" — which would have produced working code and left me not
understanding why it had ever been broken.

**How this changed how I think about AI-generated code.**

I used to read AI code looking for the places it would crash. The real risk is the
opposite: this app never crashed once, and that's precisely what made it dangerous — every
bug was a *confident wrong answer* with no traceback, and a bare `except TypeError` that
turned a genuine error into a plausible-looking lie. AI-generated code fails silently and
looks finished, so "it runs" now means nothing to me; the only thing I'll trust is a test
I've watched fail.
