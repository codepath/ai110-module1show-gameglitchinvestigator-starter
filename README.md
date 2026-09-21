# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

An AI was asked to build a simple "Number Guessing Game" using Streamlit. It wrote the
code, ran away, and left behind a game that *looked* finished and was completely broken:

- You couldn't reliably win.
- The hints lied to you.
- The secret number had commitment issues.

None of it crashed on startup, which is what made it dangerous — every bug produced a
confident wrong answer instead of a stack trace. This repo is the repaired version, plus
the paper trail of how it was diagnosed.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m streamlit run app.py`
3. Run the tests: `pytest`

## 🎯 The Game's Purpose

A single-player number guessing game. The app picks a secret number inside a range
determined by the selected difficulty, and you have a limited number of guesses to find
it. After each guess the game tells you whether you were too high or too low, and awards
points for winning quickly. It's a small app on purpose — small enough that every bug in
it is a bug you can reason about completely.

| Difficulty | Range | Attempts allowed | Guesses a perfect binary search needs |
|------------|-------|------------------|----------------------------------------|
| Easy | 1–20 | 6 | 5 |
| Normal | 1–100 | 8 | 7 |
| Hard | 1–200 | 8 | 8 |

Every difficulty is winnable with perfect play — that last column is enforced by a test,
because an attempt budget that silently disagrees with its range is exactly the bug that
made the original "impossible".

## 🐛 Bugs Found

Full reproduction steps, expected-vs-actual behaviour, and console output live in
[`reflection.md`](reflection.md) section 1. Summary:

| # | Bug | Root cause |
|---|-----|------------|
| 1 | Hints were backwards — guessing 60 against a secret of 50 said "📈 Go HIGHER!" | `check_guess` returned each outcome paired with the *opposite* advice string |
| 2 | Hints were wrong in a second, sneakier way — a guess of 9 was called too high | `app.py` coerced the secret to `str()` on every even attempt; `guess > secret` raised `TypeError`, and a bare `except TypeError` "recovered" by comparing strings — `"9" > "50"` is `True` |
| 3 | Score went haywire and negative | `update_score` paid "Too High" **+5** on even attempts and **−5** on odd ones, so the reward depended on *when* you guessed; nothing clamped the total |
| 4 | "New Game" never started a new game | The handler reset `attempts` and `secret` but not `score`, `status` or `history`. With `status` still `"won"`, the next rerun hit `st.stop()` — clicking New Game was what kept the app stuck |
| 5 | Changing difficulty made the game unwinnable | The secret was generated once and never reseeded. Switching to Easy (1–20) left the old secret (87) in place. "Hard" was also *narrower* (1–50) than Normal (1–100) |
| 6 | Attempt counting was off by one and punished typos | `attempts` started at `1`, so a fresh Normal game advertised 7 of its 8 attempts; `attempts += 1` ran *before* input validation, so `abc` burned a turn |
| 7 | `pytest` could not run at all | Every function in `logic_utils.py` was a `NotImplementedError` stub, and bare `pytest` failed at collection with `ModuleNotFoundError: No module named 'logic_utils'` |

## 🔧 Fixes Applied

**Refactor first.** All four functions moved out of `app.py` into `logic_utils.py`, which
imports no Streamlit. `app.py` is now UI only: read widgets → call logic → render. That
split is what made the rest testable.

**The structural fix for bug 1.** `check_guess` used to return an `(outcome, message)`
tuple, so the rule and its wording were hand-written side by side and could disagree. It
now returns just an outcome constant (`WIN` / `TOO_HIGH` / `TOO_LOW`), and a new
`hint_message(outcome)` looks the advice up from it. "Too High" can no longer be paired
with "go HIGHER" because nobody writes that pairing by hand any more.

Everything else:

- **Bug 2** — the secret is passed through as the `int` it always was. The bare
  `except TypeError` is gone; `_to_int()` raises loudly on junk instead of falling back
  to a string comparison. A wrong hint is worse than a crash.
- **Bug 3** — both wrong outcomes cost the same fixed 5 points, the total floors at 0,
  and the win bonus is `100 − 10 × (attempts_used − 1)` with a floor of 10, so a
  first-guess win is worth the full 100 (the old formula double-counted the
  already-incremented counter and paid 80).
- **Bug 4** — one `start_new_game()` function resets secret, attempts, score, status and
  history, so no caller can forget a field.
- **Bug 5** — changing difficulty starts a fresh round in the new range. Hard is now
  1–200, genuinely wider than Normal, and two tests check every difficulty is winnable.
- **Bug 6** — `attempts` starts at 0 and is only incremented *after* `parse_guess`
  succeeds, so invalid input is free. The status banner uses the real range and is
  rendered into an `st.empty()` slot at the *end* of the script, so it reflects this
  run's guess instead of lagging a rerun behind.
- **Bug 7** — `conftest.py` and `pytest.ini` put the repo root on `sys.path`, so
  `pytest`, `pytest tests/` and `python -m pytest` all work from any directory.
- **Extra hardening** — `parse_guess` now range-checks the guess, rejects fractional
  input instead of silently truncating `"3.9"` to `3`, and no longer dies with
  `OverflowError` on `"1e999"` (a crash my own fix introduced, caught by a test).


## ✨ Features Added (beyond the repairs)

Three player-facing features were built on top of the repaired game. All of their logic
lives in `logic_utils.py` as pure functions, so each one is unit tested.

**🌡️ Hot/Cold proximity feedback** — `proximity_label()` and `proximity_trend()`, shown
under the direction hint after every guess. The direction hint says *which way* to move;
the proximity label says *how far is left*; the trend says whether the last guess was an
improvement (`warmer 🔺` / `colder 🔻` / `same ➡️`). The bands are normalised against the
width of the difficulty's range rather than being absolute distances, so "Hot" means the
same thing on Easy (1–20) as on Hard (1–200): being 10 away is most of the board on one
and a near miss on the other.

| Distance as a fraction of the range | Label |
|---|---|
| exactly 0 | 🎯 Bullseye |
| ≤ 0.05 | 🔥 Blazing hot |
| ≤ 0.15 | ♨️ Hot |
| ≤ 0.30 | 🌤️ Warm |
| ≤ 0.50 | 🧊 Cold |
| > 0.50 | ❄️ Freezing |

**📜 Guess History sidebar** — `render_sidebar_history()` in `app.py`, newest guess first,
each row showing a direction arrow, the guess, its proximity label and its outcome.

**🏆 High Score tracker** — `update_high_scores()` and `format_high_scores()`, rendered by
`render_sidebar_high_scores()`. Records persist across rounds for the whole session (a
deliberate exception to `start_new_game()`, which resets everything else), are kept
per difficulty, and are only beaten by a higher score or by an equal score in fewer
attempts. A "🏆 New *difficulty* high score!" banner fires only on a genuine improvement,
and a "Reset high scores" button is the only way to clear the table.

**📊 Round summary table** — `build_session_table()`, rendered by `render_round_summary()`
when a round ends: one row per guess with its result, how far off it was, and its
proximity label.

## 📸 Demo Walkthrough

A full game on **Normal** difficulty (range 1–100, 8 attempts, secret = 50, revealed via
the "Developer Debug Info" expander):

1. App loads. The banner reads **"Guess a number between 1 and 100. Attempts left: 8"** —
   all 8 attempts, not 7. The sidebar shows "No guesses yet this round."
2. User enters `60` → **"📉 Too high -- go LOWER!"** plus **"♨️ Hot"**. Attempts left drops
   to 7, score 0. The guess appears in the sidebar history.
3. User enters `abc` → **"That is not a number."** Attempts left stays at **7** — the typo
   is free.
4. User enters `3.9` → **"Whole numbers only -- no decimals."** Still 7 attempts left; the
   game does not quietly score it as a guess of 3.
5. User enters `500` → **"Out of range. Guess between 1 and 100."** Still 7 left.
6. User enters `9` → **"📈 Too low -- go HIGHER!"** plus **"🧊 Cold (colder than your last
   guess 🔻)"** — correct, where the original called 9 *too high* because it compared
   `"9" > "50"` as text. 6 attempts left.
7. User enters `40` → **"📈 Too low -- go HIGHER!"** plus **"♨️ Hot (warmer than your last
   guess 🔺)"**. 5 attempts left, score still 0 (wrong guesses cost 5 but the score floors
   at 0 rather than going negative).
8. User enters `50` → 🎈 balloons, **"You won in 4 attempts! The secret was 50. Final
   score: 70"**, **"🏆 New Normal high score!"**, and the 📊 Round summary table appears.
   The game ends and further guessing is blocked.
9. User clicks **New Game 🔁** → a fresh secret, attempts back to 8, **score back to 0**,
   status back to playing, history cleared — but the 🏆 high score survives. The original
   left status at `"won"` here and the app became permanently unplayable.
10. User switches difficulty to **Easy** → **"Difficulty changed to Easy. New game
    started."** and the banner becomes **"Guess a number between 1 and 20. Attempts left:
    6"** with a secret reseeded inside 1–20. The original kept the old out-of-range secret
    and still claimed the range was 1–100.
11. Playing Easy and using all 6 attempts without finding it → **"Out of attempts! The
    secret was 7. Score: 0"**, the round summary table appears, and the game stops until
    New Game is clicked.

### Recorded terminal trace of that session

Not a description — this is the actual run, driven through the Streamlit runtime with the
secret pinned, printing real `st.session_state` after every click:

```text
$ python -m streamlit run app.py      # REPAIRED CODE

### Normal difficulty, secret pinned to 50
[page load, before any guess]
    session_state: secret=50  attempts=0  score=0  status=playing
    INFO    Guess a number between 1 and 100. Attempts left: 8
[typed 60 -> Submit Guess]
    session_state: secret=50  attempts=1  score=0  status=playing
    INFO    Guess a number between 1 and 100. Attempts left: 7
    INFO    Hot
    HINT    Too high -- go LOWER!
[typed abc -> Submit Guess]
    session_state: secret=50  attempts=1  score=0  status=playing
    INFO    Guess a number between 1 and 100. Attempts left: 7
    ERROR   That is not a number.
[typed 3.9 -> Submit Guess]
    session_state: secret=50  attempts=1  score=0  status=playing
    ERROR   Whole numbers only -- no decimals.
[typed 500 -> Submit Guess]
    session_state: secret=50  attempts=1  score=0  status=playing
    ERROR   Out of range. Guess between 1 and 100.
[typed 9 -> Submit Guess]
    session_state: secret=50  attempts=2  score=0  status=playing
    INFO    Guess a number between 1 and 100. Attempts left: 6
    INFO    Cold (colder than your last guess 🔻)
    HINT    Too low -- go HIGHER!
[typed 40 -> Submit Guess]
    session_state: secret=50  attempts=3  score=0  status=playing
    INFO    Guess a number between 1 and 100. Attempts left: 5
    INFO    Hot (warmer than your last guess 🔺)
    HINT    Too low -- go HIGHER!
[typed 50 -> Submit Guess]
    session_state: secret=50  attempts=4  score=70  status=won
    INFO    Guess a number between 1 and 100. Attempts left: 4
    HINT    Correct!
    SUCCESS You won in 4 attempts! The secret was 50. Final score: 70
    SUCCESS New Normal high score!

    Round summary table:
       #  Guess   Result  Off by  Proximity
       1     60 Too High      10     ♨️ Hot
       2      9  Too Low      41     🧊 Cold
       3     40  Too Low      10     ♨️ Hot
       4     50      Win       0 🎯 Bullseye
      Difficulty  Best score  Attempts
          Normal          70         4

### Sidebar after the round
    HISTORY 🎯 **50** — 🎯 Bullseye   <small>guess 4 · Win</small>
    HISTORY ⬆️ **40** — ♨️ Hot   <small>guess 3 · Too Low</small>
    HISTORY ⬆️ **9** — 🧊 Cold   <small>guess 2 · Too Low</small>
    HISTORY ⬇️ **60** — ♨️ Hot   <small>guess 1 · Too High</small>

### Clicking New Game after a win
[clicked New Game]
    session_state: secret=96  attempts=0  score=0  status=playing
    INFO    Guess a number between 1 and 100. Attempts left: 8

### Switching difficulty mid-game (Easy is 1-20)
[switched difficulty to Easy]
    session_state: secret=12  attempts=0  score=0  status=playing
    INFO    Difficulty changed to Easy. New game started.
    INFO    Guess a number between 1 and 20. Attempts left: 6
    secret 12 is inside the Easy range 1-20  ✔
```

Two notes on reading that trace. The proximity lines show as `INFO Hot` rather than
`INFO ♨️ Hot` because `st.info` detects a leading emoji and moves it into the callout's
icon slot — the emoji is rendered, just not in the message text, which is why it *is*
visible in the sidebar and table rows. And the score reads 0 after three wrong guesses
rather than −15: wrong guesses cost 5 but the total floors at 0, then the win on attempt
4 pays 100 − 10 × 3 = 70.

Compare with the [pre-fix trace in `reflection.md`](reflection.md#1-what-was-broken-when-you-started),
recorded the same way against the same pinned secret.

## 🧪 Test Results

3 starter tests (kept verbatim) plus 80 added, 83 total. Each *regression* assertion was
also run against the **original buggy functions** to confirm it actually fails there — a
test that passes against the bug it claims to cover is worthless. 10 of 10 do.

```
$ pytest
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/user/ai110-module1show-gameglitchinvestigator-starter
configfile: pytest.ini
collected 83 items

tests/test_game_logic.py ...............................................  [100%]

============================== 83 passed in 0.11s ==============================
```

<details>
<summary><strong>Full <code>pytest -v</code> output (83 tests)</strong></summary>

```
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.0.2, pluggy-1.6.0 -- /root/.local/share/uv/tools/pytest/bin/python
cachedir: .pytest_cache
rootdir: /home/user/ai110-module1show-gameglitchinvestigator-starter
configfile: pytest.ini
testpaths: tests
collecting ... collected 83 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  1%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [  2%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [  3%]
tests/test_game_logic.py::test_too_high_hint_tells_the_player_to_go_lower PASSED [  4%]
tests/test_game_logic.py::test_too_low_hint_tells_the_player_to_go_higher PASSED [  6%]
tests/test_game_logic.py::test_win_hint_is_congratulations_not_a_direction PASSED [  7%]
tests/test_game_logic.py::test_comparison_is_numeric_not_lexicographic[9-50-Too Low0] PASSED [  8%]
tests/test_game_logic.py::test_comparison_is_numeric_not_lexicographic[100-50-Too High0] PASSED [  9%]
tests/test_game_logic.py::test_comparison_is_numeric_not_lexicographic[9-50-Too Low1] PASSED [ 10%]
tests/test_game_logic.py::test_comparison_is_numeric_not_lexicographic[100-50-Too High1] PASSED [ 12%]
tests/test_game_logic.py::test_win_is_detected_even_when_the_secret_arrives_as_a_string PASSED [ 13%]
tests/test_game_logic.py::test_non_numeric_input_raises_instead_of_guessing PASSED [ 14%]
tests/test_game_logic.py::test_wrong_guesses_score_the_same_regardless_of_attempt_parity PASSED [ 15%]
tests/test_game_logic.py::test_too_high_and_too_low_cost_the_same[1] PASSED [ 16%]
tests/test_game_logic.py::test_too_high_and_too_low_cost_the_same[2] PASSED [ 18%]
tests/test_game_logic.py::test_too_high_and_too_low_cost_the_same[3] PASSED [ 19%]
tests/test_game_logic.py::test_too_high_and_too_low_cost_the_same[4] PASSED [ 20%]
tests/test_game_logic.py::test_wrong_guesses_never_push_the_score_negative PASSED [ 21%]
tests/test_game_logic.py::test_a_first_guess_win_is_worth_full_points PASSED [ 22%]
tests/test_game_logic.py::test_win_points_decay_with_each_attempt_used PASSED [ 24%]
tests/test_game_logic.py::test_unknown_outcome_leaves_the_score_untouched PASSED [ 25%]
tests/test_game_logic.py::test_harder_difficulty_means_a_wider_range PASSED [ 26%]
tests/test_game_logic.py::test_unknown_difficulty_falls_back_to_normal_instead_of_crashing PASSED [ 27%]
tests/test_game_logic.py::test_every_difficulty_is_winnable_by_binary_search[Easy] PASSED [ 28%]
tests/test_game_logic.py::test_every_difficulty_is_winnable_by_binary_search[Hard] PASSED [ 30%]
tests/test_game_logic.py::test_every_difficulty_is_winnable_by_binary_search[Normal] PASSED [ 31%]
tests/test_game_logic.py::test_binary_search_actually_wins_every_secret_in_range[Easy] PASSED [ 32%]
tests/test_game_logic.py::test_binary_search_actually_wins_every_secret_in_range[Hard] PASSED [ 33%]
tests/test_game_logic.py::test_binary_search_actually_wins_every_secret_in_range[Normal] PASSED [ 34%]
tests/test_game_logic.py::test_blank_input_is_rejected[] PASSED          [ 36%]
tests/test_game_logic.py::test_blank_input_is_rejected[   ] PASSED       [ 37%]
tests/test_game_logic.py::test_blank_input_is_rejected[None] PASSED      [ 38%]
tests/test_game_logic.py::test_non_numeric_input_is_rejected[abc] PASSED [ 39%]
tests/test_game_logic.py::test_non_numeric_input_is_rejected[fifty] PASSED [ 40%]
tests/test_game_logic.py::test_non_numeric_input_is_rejected[0x1f] PASSED [ 42%]
tests/test_game_logic.py::test_non_numeric_input_is_rejected[--7] PASSED [ 43%]
tests/test_game_logic.py::test_non_numeric_input_is_rejected[1,000] PASSED [ 44%]
tests/test_game_logic.py::test_non_numeric_input_is_rejected[nan] PASSED [ 45%]
tests/test_game_logic.py::test_full_width_digits_are_accepted_because_python_int_accepts_them PASSED [ 46%]
tests/test_game_logic.py::test_absurdly_large_input_is_rejected_without_crashing[1e999] PASSED [ 48%]
tests/test_game_logic.py::test_absurdly_large_input_is_rejected_without_crashing[-1e999] PASSED [ 49%]
tests/test_game_logic.py::test_surrounding_whitespace_is_tolerated PASSED [ 50%]
tests/test_game_logic.py::test_whitespace_only_input_asks_for_a_guess_rather_than_scolding PASSED [ 51%]
tests/test_game_logic.py::test_fractional_guess_is_rejected_not_silently_truncated PASSED [ 53%]
tests/test_game_logic.py::test_whole_number_written_as_a_decimal_is_accepted PASSED [ 54%]
tests/test_game_logic.py::test_negative_guess_is_accepted_when_no_range_is_supplied PASSED [ 55%]
tests/test_game_logic.py::test_out_of_range_guesses_are_rejected_when_a_range_is_supplied[0] PASSED [ 56%]
tests/test_game_logic.py::test_out_of_range_guesses_are_rejected_when_a_range_is_supplied[101] PASSED [ 57%]
tests/test_game_logic.py::test_out_of_range_guesses_are_rejected_when_a_range_is_supplied[-5] PASSED [ 59%]
tests/test_game_logic.py::test_out_of_range_guesses_are_rejected_when_a_range_is_supplied[999] PASSED [ 60%]
tests/test_game_logic.py::test_guesses_on_and_inside_the_range_boundaries_are_accepted[1] PASSED [ 61%]
tests/test_game_logic.py::test_guesses_on_and_inside_the_range_boundaries_are_accepted[50] PASSED [ 62%]
tests/test_game_logic.py::test_guesses_on_and_inside_the_range_boundaries_are_accepted[100] PASSED [ 63%]
tests/test_game_logic.py::test_minimum_attempts_needed[1-1-1] PASSED     [ 65%]
tests/test_game_logic.py::test_minimum_attempts_needed[1-2-1] PASSED     [ 66%]
tests/test_game_logic.py::test_minimum_attempts_needed[1-8-3] PASSED     [ 67%]
tests/test_game_logic.py::test_minimum_attempts_needed[1-20-5] PASSED    [ 68%]
tests/test_game_logic.py::test_minimum_attempts_needed[1-100-7] PASSED   [ 69%]
tests/test_game_logic.py::test_minimum_attempts_needed[1-200-8] PASSED   [ 71%]
tests/test_game_logic.py::test_minimum_attempts_matches_log2_for_every_difficulty PASSED [ 72%]
tests/test_game_logic.py::test_exact_guess_is_a_bullseye PASSED          [ 73%]
tests/test_game_logic.py::test_proximity_gets_colder_as_the_guess_moves_away PASSED [ 74%]
tests/test_game_logic.py::test_the_coldest_band_is_reachable PASSED      [ 75%]
tests/test_game_logic.py::test_every_band_is_reachable_for_some_guess PASSED [ 77%]
tests/test_game_logic.py::test_proximity_is_symmetric_above_and_below_the_secret PASSED [ 78%]
tests/test_game_logic.py::test_proximity_is_relative_to_the_difficulty_range PASSED [ 79%]
tests/test_game_logic.py::test_proximity_does_not_divide_by_zero_on_a_degenerate_range PASSED [ 80%]
tests/test_game_logic.py::test_proximity_trend[None-40-] PASSED          [ 81%]
tests/test_game_logic.py::test_proximity_trend[20-40-warmer] PASSED      [ 83%]
tests/test_game_logic.py::test_proximity_trend[45-20-colder] PASSED      [ 84%]
tests/test_game_logic.py::test_proximity_trend[40-60-same] PASSED        [ 85%]
tests/test_game_logic.py::test_session_table_has_one_row_per_guess_in_play_order PASSED [ 86%]
tests/test_game_logic.py::test_session_table_is_empty_for_a_round_with_no_guesses PASSED [ 87%]
tests/test_game_logic.py::test_first_result_always_sets_the_record PASSED [ 89%]
tests/test_game_logic.py::test_a_higher_score_replaces_the_record PASSED [ 90%]
tests/test_game_logic.py::test_a_lower_score_does_not_replace_the_record PASSED [ 91%]
tests/test_game_logic.py::test_an_equal_score_in_fewer_attempts_wins_the_tie PASSED [ 92%]
tests/test_game_logic.py::test_an_equal_score_in_more_attempts_does_not_win_the_tie PASSED [ 93%]
tests/test_game_logic.py::test_each_difficulty_keeps_its_own_record PASSED [ 95%]
tests/test_game_logic.py::test_update_high_scores_does_not_mutate_its_input PASSED [ 96%]
tests/test_game_logic.py::test_update_high_scores_tolerates_none PASSED  [ 97%]
tests/test_game_logic.py::test_high_scores_are_formatted_best_first PASSED [ 98%]
tests/test_game_logic.py::test_formatting_an_empty_high_score_table_gives_no_rows PASSED [100%]

============================== 83 passed in 0.08s ==============================
```

</details>

The two tests worth singling out are
`test_binary_search_actually_wins_every_secret_in_range` and
`test_every_difficulty_is_winnable_by_binary_search`. The first plays a complete perfect
game against *every* possible secret in *every* difficulty, navigating only by the hints
`check_guess` returns — if the hints were inverted, the search would never converge. The
second asserts no difficulty can advertise fewer attempts than `ceil(log2(range))`.
Between them they make "the game is impossible" a test failure rather than a bug report.

## 🧹 Code Style

`flake8`, `ruff` and `black --check` all pass clean on every file. Full before/after
output is committed in [`docs/lint_report.txt`](docs/lint_report.txt).

```
$ flake8 --max-line-length=88 app.py logic_utils.py conftest.py tests/
(no output -- 0 violations)

$ ruff check --line-length=88 app.py logic_utils.py conftest.py tests/
All checks passed!

$ black --check --line-length=88 app.py logic_utils.py conftest.py tests/
All done! ✨ 🍰 ✨
4 files would be left unchanged.
```

Every function in `logic_utils.py` carries a docstring; the public ones use Google-style
`Args:`/`Returns:` sections.

## 📝 Document Your Experience

- [x] **Describe the game's purpose.** See [The Game's Purpose](#-the-games-purpose).
- [x] **Detail which bugs you found.** See [Bugs Found](#-bugs-found), with a recorded
      pre-fix terminal trace and an 11-row reproduction log in
      [`reflection.md`](reflection.md) section 1.
- [x] **Explain what fixes you applied.** See [Fixes Applied](#-fixes-applied); every fix
      also carries a `# FIX:` comment at its location in the code.

## 🗂️ Project Layout

```
app.py                     Streamlit UI only -- widgets, session state, rendering
logic_utils.py             All game rules. No Streamlit import, so it is unit testable
conftest.py                Puts the repo root on sys.path so `pytest` can import logic_utils
pytest.ini                 Anchors pytest's rootdir
tests/test_game_logic.py   3 starter tests + 80 added
docs/lint_report.txt       flake8 / ruff / black output, before and after
reflection.md              Pre-fix terminal trace, bug reproduction log, AI write-up
ai_interactions.md         Stretch-feature log (agent workflow, test generation, linting)
```

## 🚀 Stretch Features

- [x] **Challenge 1: Advanced Edge-Case Testing** — the suite covers blank and
      whitespace-only input, non-numeric input, fractional and decimal-but-whole guesses,
      negative numbers, range boundaries (1 / 50 / 100 accepted; 0 / 101 / −5 / 999
      rejected), `"1e999"` overflow, full-width Unicode digits, unknown difficulties,
      unknown score outcomes, proximity-band boundaries, high-score tie-breaking and
      input immutability, plus an exhaustive binary-search playthrough of every secret in
      every difficulty. Terminal output is in [Test Results](#-test-results);
      per-case prompts and rationale are in [`ai_interactions.md`](ai_interactions.md)
      (SF7).
- [x] **Challenge 2: Feature Expansion via Agent Mode** — 🏆 High Score tracker and
      📜 Guess History sidebar, both fully functional and unit tested. See
      [Features Added](#-features-added-beyond-the-repairs); the agent workflow, files
      modified and manual corrections are documented in
      [`ai_interactions.md`](ai_interactions.md) (SF8).
- [x] **Challenge 3: Professional Documentation and Style** — docstrings on every
      function in `logic_utils.py`, and `flake8` / `ruff` / `black --check` all clean.
      See [Code Style](#-code-style), evidence in
      [`docs/lint_report.txt`](docs/lint_report.txt), prompts and applied changes in
      [`ai_interactions.md`](ai_interactions.md) (SF9).
- [x] **Challenge 4: Enhanced Game UI and Formatting** — 🌡️ Hot/Cold proximity labels with
      a warmer/colder trend, emoji-coded history rows, and a 📊 round summary table. See
      [Features Added](#-features-added-beyond-the-repairs) for the functions involved
      (`proximity_label`, `proximity_trend`, `build_session_table`,
      `render_sidebar_history`, `render_round_summary`).
- [ ] **Challenge 5: AI Model or Prompt Comparison** — [`ai_interactions.md`](ai_interactions.md)
      (SF11) records a genuine comparison of two *prompting strategies* run against the
      same model. A true two-**model** comparison is not claimed here, because only one
      model was available during this work and inventing another model's output would
      make the log fiction.
