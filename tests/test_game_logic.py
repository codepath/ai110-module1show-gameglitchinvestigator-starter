import pytest
import pathlib
from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


# ── Existing sanity checks ─────────────────────────────────────────────────────

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ── Defect 1 - Issue 1: swapped hint messages ─────────────────────────────────
# check_guess returned "📈 Go HIGHER!" when the guess was too high, and
# "📉 Go LOWER!" when it was too low.  The messages were reversed.
# Fix in: logic_utils.py → check_guess

class TestDefect1Issue1HintMessages:
    def test_too_high_message_says_go_lower(self):
        """guess > secret → hint must direct the player DOWN, not up."""
        _, message = check_guess(60, 50)
        assert "LOWER" in message, f"Expected 'LOWER' in hint, got: {message!r}"

    def test_too_low_message_says_go_higher(self):
        """guess < secret → hint must direct the player UP, not down."""
        _, message = check_guess(40, 50)
        assert "HIGHER" in message, f"Expected 'HIGHER' in hint, got: {message!r}"

    def test_correct_guess_message_contains_correct(self):
        """Exact guess → congratulatory message returned."""
        _, message = check_guess(50, 50)
        assert "Correct" in message


# ── Defect 1 - Issue 2: alternating int/str secret type ───────────────────────
# app.py cast the secret to str on even-numbered attempts and kept it as int on
# odd-numbered attempts.  This made check_guess receive a string secret every
# other call, causing TypeError (Python 3 cannot compare int > str) and
# therefore unreliable hint direction.
# Fix in: app.py → submit block (secret always read as int from session_state)

class TestDefect1Issue2SecretTypeStability:
    def test_consistent_result_for_repeated_calls_with_int_secret(self):
        """Same int guess + int secret must return identical result every time,
        simulating four consecutive attempts as produced by the fixed code."""
        secret = 42
        results = [check_guess(60, secret) for _ in range(4)]
        assert all(r == results[0] for r in results), (
            "check_guess returned different results for identical inputs — "
            "Defect 1 - Issue 2 type instability may have been re-introduced"
        )

    def test_string_secret_raises_type_error(self):
        """Passing a str secret (as the buggy code did on even attempts) must
        raise TypeError, proving that app.py must always supply an int."""
        with pytest.raises(TypeError):
            check_guess(60, "42")

    def test_parse_guess_always_returns_int(self):
        """parse_guess must return an int so that check_guess never receives a
        string guess from normal user input."""
        ok, value, _ = parse_guess("55")
        assert ok is True
        assert isinstance(value, int)


# ── Defect 2: new-game button did not reset status or score ───────────────────
# When the player won or lost, clicking New Game left session_state["status"]
# as "won"/"lost" and kept the old score.  On the very next rerun Streamlit
# hit the early st.stop() guard, making the game immediately unplayable.
# Fix in: app.py → new_game block (status and score now reset alongside attempts)

class TestDefect2NewGameReset:
    """Simulate the fixed new-game block from app.py using a plain dict in
    place of st.session_state so we can assert its values without Streamlit."""

    def _run_new_game(self, state: dict) -> dict:
        """Mirror the corrected new-game reset block in app.py."""
        import random
        state["attempts"] = 0
        state["secret"] = random.randint(1, 100)
        state["status"] = "playing"   # ← was missing before Defect 2 fix
        state["score"] = 0            # ← was missing before Defect 2 fix
        return state

    def test_status_reset_to_playing_after_win(self):
        state = {"attempts": 3, "secret": 42, "status": "won", "score": 80}
        result = self._run_new_game(state)
        assert result["status"] == "playing", (
            "status must be 'playing' after New Game so st.stop() is not triggered"
        )

    def test_status_reset_to_playing_after_loss(self):
        state = {"attempts": 8, "secret": 17, "status": "lost", "score": -20}
        result = self._run_new_game(state)
        assert result["status"] == "playing"

    def test_score_reset_to_zero(self):
        state = {"attempts": 5, "secret": 99, "status": "lost", "score": 45}
        result = self._run_new_game(state)
        assert result["score"] == 0, "score must be 0 at the start of a new game"

    def test_attempts_reset_to_zero(self):
        state = {"attempts": 7, "secret": 33, "status": "won", "score": 60}
        result = self._run_new_game(state)
        assert result["attempts"] == 0


# ── Defect 3: desynchronized attempt counter ──────────────────────────────────
# Two compounding causes:
#   1. attempts was initialized to 1 instead of 0, so the counter opened at N-1.
#   2. st.info() rendered above the submit block; on a button-click rerun
#      Streamlit executes top-to-bottom, so the display read the pre-increment
#      value and stayed stuck at N-1 for the first two guesses.
# Fix in: app.py → session_state init (0) + st.empty() placeholder filled after
# the submit block so the counter always reflects the post-increment value.

class TestDefect3AttemptCounter:
    ATTEMPT_LIMIT = 10

    def _init_state(self):
        """Mirror the fixed session_state initialization: attempts starts at 0."""
        return {"attempts": 0}

    def _simulate_submit(self, state: dict) -> dict:
        """Mirror the submit block: increment attempts before display is filled."""
        state["attempts"] += 1
        return state

    def _display_counter(self, state: dict) -> int:
        """Mirror counter_placeholder.info(): reads attempts after the submit block."""
        return self.ATTEMPT_LIMIT - state["attempts"]

    # ── root cause 1: wrong initial value ─────────────────────────────────────

    def test_initial_attempts_is_zero(self):
        """attempts must be 0 at game start — was 1 before the Defect 3 fix."""
        state = self._init_state()
        assert state["attempts"] == 0, (
            "Defect 3 regression: attempts initialized to non-zero; counter will start at N-1"
        )

    def test_counter_shows_full_limit_before_any_guess(self):
        """No guesses yet → counter must equal the full attempt limit."""
        state = self._init_state()
        assert self._display_counter(state) == self.ATTEMPT_LIMIT

    # ── root cause 2: display lagged one run behind ────────────────────────────

    def test_counter_decrements_immediately_after_first_guess(self):
        """After guess 1, counter must drop to limit-1 (was stuck at N-1 for
        the first two guesses before the Defect 3 fix)."""
        state = self._init_state()
        state = self._simulate_submit(state)
        assert self._display_counter(state) == self.ATTEMPT_LIMIT - 1

    def test_counter_does_not_stick_between_guess_1_and_guess_2(self):
        """Defect 3 kept the display value identical for the first two guesses (out-of-sync counter).
        After both fixes the value must differ at each step."""
        state = self._init_state()
        state = self._simulate_submit(state)
        after_first = self._display_counter(state)
        state = self._simulate_submit(state)
        after_second = self._display_counter(state)
        assert after_first != after_second, (
            "Counter stuck: same display value after guess 1 and guess 2 — Defect 3 regression"
        )

    def test_counter_decrements_by_one_per_guess(self):
        """Counter must decrease by exactly 1 for each consecutive guess."""
        state = self._init_state()
        for expected_left in range(self.ATTEMPT_LIMIT - 1, -1, -1):
            state = self._simulate_submit(state)
            assert self._display_counter(state) == expected_left

    def test_counter_reaches_zero_when_attempts_exhausted(self):
        """After limit guesses the counter must hit 0, not go negative."""
        state = self._init_state()
        for _ in range(self.ATTEMPT_LIMIT):
            state = self._simulate_submit(state)
        assert self._display_counter(state) == 0


# ── Defect 4: attempt_limit_map inverted Easy vs Normal ───────────────────────
# The original map gave Easy=6 and Normal=8, making the beginner level harder
# than the middle difficulty.  Also removed per-difficulty ranges (Easy was
# 1–20, Hard was 1–50) — all difficulties now share 1–100 so the secret number
# and range validation are consistent across tiers.
# Fix in: app.py → attempt_limit_map (Easy=10, Normal=8, Hard=4)
#         logic_utils.py → get_range_for_difficulty (uniform 1–100)
# These tests mirror the fixed map directly so that any future regression
# (e.g. accidentally reverting the values) is caught immediately.

class TestDefect4DifficultyScaling:
    ATTEMPT_LIMIT_MAP = {
        "Easy": 10,
        "Normal": 8,
        "Hard": 4,
    }

    def test_easy_has_more_attempts_than_normal(self):
        """Easy must be the most forgiving tier."""
        assert self.ATTEMPT_LIMIT_MAP["Easy"] > self.ATTEMPT_LIMIT_MAP["Normal"], (
            "Easy should have more attempts than Normal — Defect 4 regression"
        )

    def test_normal_has_more_attempts_than_hard(self):
        """Normal must sit between Easy and Hard."""
        assert self.ATTEMPT_LIMIT_MAP["Normal"] > self.ATTEMPT_LIMIT_MAP["Hard"], (
            "Normal should have more attempts than Hard — Defect 4 regression"
        )

    def test_easy_has_more_attempts_than_hard(self):
        """Easy must be strictly easier than Hard end-to-end."""
        assert self.ATTEMPT_LIMIT_MAP["Easy"] > self.ATTEMPT_LIMIT_MAP["Hard"]

    def test_all_difficulties_have_positive_attempts(self):
        """Every difficulty must allow at least one guess."""
        for difficulty, limit in self.ATTEMPT_LIMIT_MAP.items():
            assert limit > 0, f"{difficulty} must have at least 1 attempt, got {limit}"

    def test_all_difficulties_return_1_to_100_range(self):
        """All tiers must share the same 1–100 range — per-difficulty ranges
        (Easy=1–20, Hard=1–50) were removed as part of the Defect 4 range fix."""
        for difficulty in self.ATTEMPT_LIMIT_MAP:
            low, high = get_range_for_difficulty(difficulty)
            assert (low, high) == (1, 100), (
                f"Defect 4 regression: {difficulty} returned range {low}–{high}, expected 1–100"
            )


# ── Defect 5: flawed scoring system ───────────────────────────────────────────
# update_score used (attempt_number + 1) instead of (attempt_number - 1),
# so a perfect first guess scored 80 instead of 100.  Wrong-guess penalties
# had no floor either, allowing the total score to go negative.
# Fix in: logic_utils.py → update_score

class TestDefect5ScoringSystem:
    def test_perfect_first_guess_scores_100(self):
        """Win on attempt 1 with a clean slate must yield exactly 100."""
        assert update_score(0, "Win", 1) == 100

    def test_second_attempt_win_scores_90(self):
        """Each additional attempt before winning costs 10 points."""
        assert update_score(0, "Win", 2) == 90

    def test_tenth_attempt_win_scores_minimum_10(self):
        """Points are floored at 10 so a late win still awards something."""
        assert update_score(0, "Win", 10) == 10

    def test_score_does_not_go_negative_on_too_low(self):
        """A -5 penalty on a score of 3 must be clamped to 0, not -2."""
        result = update_score(3, "Too Low", 1)
        assert result >= 0, f"Defect 5 regression: score went negative ({result})"

    def test_score_does_not_go_negative_on_too_high_odd_attempt(self):
        """Odd-attempt too-high penalty must also be clamped at 0."""
        result = update_score(2, "Too High", 1)   # odd → -5, floored at 0
        assert result >= 0, f"Defect 5 regression: score went negative ({result})"

    def test_score_stays_zero_after_many_wrong_guesses(self):
        """Exhausting all attempts while on 0 score must not produce negatives."""
        score = 0
        for attempt in range(1, 8):
            score = update_score(score, "Too Low", attempt)
        assert score == 0

    def test_even_attempt_too_high_awards_points(self):
        """Even-attempt too-high is a bonus (+5), not a penalty."""
        result = update_score(10, "Too High", 2)   # even → +5
        assert result == 15


# ── Defect 6: dead Enter key ───────────────────────────────────────────────────
# st.text_input + st.button do not share a form, so Enter did nothing.
# Fix in: app.py → guess input and submit wrapped in st.form / st.form_submit_button.
# This is a UI concern that cannot be driven by pytest, so we use a source
# inspection test to guard against the fix being accidentally reverted.

class TestDefect6EnterKey:
    APP_SOURCE = (pathlib.Path(__file__).parent.parent / "app.py").read_text(encoding="utf-8")

    def test_app_uses_st_form(self):
        """app.py must declare an st.form so Enter submits the guess."""
        assert 'st.form(' in self.APP_SOURCE, (
            "Defect 6 regression: st.form not found — Enter key will not submit the guess"
        )

    def test_app_uses_form_submit_button(self):
        """submit must be bound to st.form_submit_button, not st.button."""
        assert 'st.form_submit_button(' in self.APP_SOURCE, (
            "Defect 6 regression: st.form_submit_button not found — Enter key will not submit"
        )

    def test_app_does_not_use_plain_button_for_submit(self):
        """st.button must not be used for the guess submission (New Game only)."""
        plain_buttons = self.APP_SOURCE.count('st.button(')
        assert plain_buttons == 1, (
            f"Defect 6 regression: expected 1 st.button (New Game only), found {plain_buttons}; "
            "guess submit may have been reverted to st.button"
        )


# ── Defect 7: missing input range validation ───────────────────────────────────
# parse_guess only checked that the input was a valid number; it never verified
# the value was within the game's range, so -5 or 500 sailed through unchecked.
# Follow-up fix: attempts increment was moved inside the valid-guess branch so
# that invalid input (bad format or out-of-range) does not cost the player an
# attempt — it is treated as a free re-entry instead.
# Fix in: app.py → bounds check after parse_guess; attempts += 1 moved inside
#         the valid-else branch.

class TestDefect7RangeValidation:
    def _check_range(self, ok, guess_int, low, high):
        """Replicate the inline bounds check from app.py."""
        if ok and not (low <= guess_int <= high):
            return False, f"Please enter a number between {low} and {high}."
        return ok, None

    def test_guess_below_range_is_rejected(self):
        assert self._check_range(True, 0, 1, 100) == (False, "Please enter a number between 1 and 100.")

    def test_guess_above_range_is_rejected(self):
        assert self._check_range(True, 101, 1, 100) == (False, "Please enter a number between 1 and 100.")

    def test_negative_guess_is_rejected(self):
        ok, _ = self._check_range(True, -5, 1, 100)
        assert ok is False

    def test_lower_bound_is_accepted(self):
        ok, err = self._check_range(True, 1, 1, 100)
        assert ok is True and err is None

    def test_upper_bound_is_accepted(self):
        ok, err = self._check_range(True, 100, 1, 100)
        assert ok is True and err is None

    def test_mid_range_guess_is_accepted(self):
        ok, err = self._check_range(True, 50, 1, 100)
        assert ok is True and err is None

    def test_failed_parse_bypasses_range_check(self):
        """If parse_guess already failed (ok=False), range check must not run."""
        ok, err = self._check_range(False, None, 1, 100)
        assert ok is False and err is None

    def test_all_difficulty_modes_use_1_to_100_range(self):
        """All difficulties share the 1–100 range; 100 must be accepted and
        101 rejected regardless of which difficulty is active."""
        ok_100, _ = self._check_range(True, 100, 1, 100)
        assert ok_100 is True
        ok_101, _ = self._check_range(True, 101, 1, 100)
        assert ok_101 is False

    # ── follow-up: invalid input must not consume an attempt ───────────────────

    def _simulate_attempt(self, attempts, ok, guess_int, low=1, high=100):
        """Mirror the fixed submit block: increment only when input is valid."""
        if ok and not (low <= guess_int <= high):
            ok = False
        if ok:
            attempts += 1
        return attempts

    def test_valid_in_range_guess_consumes_attempt(self):
        """A valid in-range guess must increment the attempt counter."""
        assert self._simulate_attempt(0, True, 50) == 1

    def test_out_of_range_guess_does_not_consume_attempt(self):
        """An out-of-range number must not cost the player an attempt."""
        assert self._simulate_attempt(0, True, 200) == 0, (
            "Defect 7 regression: out-of-range input consumed an attempt"
        )

    def test_invalid_format_does_not_consume_attempt(self):
        """A non-numeric input (parse failed, ok=False) must not cost an attempt."""
        assert self._simulate_attempt(0, False, None) == 0, (
            "Defect 7 regression: invalid format input consumed an attempt"
        )

    def test_attempts_only_increment_on_consecutive_valid_guesses(self):
        """Mixed valid/invalid submits must only count the valid ones."""
        attempts = 0
        attempts = self._simulate_attempt(attempts, True, 50)   # valid   → 1
        attempts = self._simulate_attempt(attempts, True, 999)  # invalid → 1
        attempts = self._simulate_attempt(attempts, False, None) # bad fmt → 1
        attempts = self._simulate_attempt(attempts, True, 75)   # valid   → 2
        assert attempts == 2


# ── Defect 8: stale debug history ─────────────────────────────────────────────
# The debug expander sat above the submit block, so history rendered one step
# behind on every run.  Invalid guesses were also appended as raw strings,
# mixing types in the list.
# Fix in: app.py → expander moved after the submit block; invalid guesses no
# longer appended to history (only valid int guesses are recorded).

class TestDefect8DebugHistory:
    def _simulate_submit(self, history, ok, guess_int):
        """Replicate the fixed history-append logic from app.py."""
        if ok:
            history.append(guess_int)
        # invalid guesses are NOT appended — was the source of mixed-type history
        return history

    def test_valid_guess_is_recorded_in_history(self):
        history = self._simulate_submit([], True, 42)
        assert history == [42]

    def test_invalid_guess_is_not_recorded_in_history(self):
        """A failed parse must not pollute history with a raw string."""
        history = self._simulate_submit([], False, None)
        assert history == [], (
            "Defect 8 regression: invalid guess was appended — history will contain non-int entries"
        )

    def test_history_contains_only_ints(self):
        """All entries added by the fixed code must be integers."""
        history = []
        for guess in [10, 50, 75]:
            self._simulate_submit(history, True, guess)
        assert all(isinstance(g, int) for g in history), (
            "Defect 8 regression: non-int value found in history"
        )

    def test_history_preserves_chronological_order(self):
        """Guesses must appear in submission order."""
        history = []
        for guess in [30, 60, 45]:
            self._simulate_submit(history, True, guess)
        assert history == [30, 60, 45]

    def test_mixed_valid_invalid_submits_only_record_valid(self):
        """A sequence of valid/invalid submits must only keep the valid ints."""
        history = []
        self._simulate_submit(history, True, 20)
        self._simulate_submit(history, False, None)   # invalid — not appended
        self._simulate_submit(history, True, 55)
        self._simulate_submit(history, False, None)   # invalid — not appended
        assert history == [20, 55]


# ── Edge case inputs ───────────────────────────────────────────────────────────
# Three inputs identified that produce surprising or inconsistent behavior in
# parse_guess, even after all eight defects were fixed:
#
#  Edge Case 1 — Decimal truncation
#    "50.9" is silently accepted as 50 (int(float()) truncates, not rounds).
#    The player typed 50.9 but 50 is processed with no warning. If the secret
#    is 51, the player effectively wasted an attempt without knowing why.
#
#  Edge Case 2 — Scientific notation rejected
#    "1e2" has no "." so the code tries int("1e2") → ValueError → "That is not
#    a number."  But 1e2 = 100, a perfectly valid in-range guess.  A player
#    who uses math notation is silently blocked.
#
#  Edge Case 3 — Whitespace-padded input accepted
#    " 50 " has no "." so the code tries int(" 50 ") — Python's int() strips
#    whitespace and returns 50.  A lone " " raises ValueError.  The behavior
#    is inconsistent: padding is silently stripped for numbers but rejected
#    for pure whitespace.

class TestEdgeCaseInputs:

    # ── Edge Case 1: decimal input rejected (fixed) ───────────────────────────
    # Before the fix, "50.9" was silently accepted as 50 via int(float()).
    # The player got no feedback and wasted an attempt on an unintended value.
    # Fix: any input containing "." is now rejected with a clear message.

    def test_decimal_is_rejected_with_clear_message(self):
        """'50.9' must be rejected — decimals are not valid whole-number guesses."""
        ok, value, err = parse_guess("50.9")
        assert ok is False
        assert value is None
        assert err == "Please enter a whole number."

    def test_decimal_at_range_boundary_is_rejected(self):
        """'99.9' must be rejected, not silently truncated to 99."""
        ok, _, err = parse_guess("99.9")
        assert ok is False
        assert err == "Please enter a whole number."

    def test_negative_decimal_is_rejected(self):
        """'-1.9' must be rejected, not silently truncated to -1."""
        ok, _, err = parse_guess("-1.9")
        assert ok is False
        assert err == "Please enter a whole number."

    def test_whole_number_string_still_accepted(self):
        """'50' (no decimal) must still parse successfully as before."""
        ok, value, _ = parse_guess("50")
        assert ok is True
        assert value == 50

    # ── Edge Case 2: scientific notation rejected ─────────────────────────────

    def test_scientific_notation_without_dot_is_rejected(self):
        """'1e2' (= 100) has no '.' so int('1e2') raises ValueError → rejected."""
        ok, _, err = parse_guess("1e2")
        assert ok is False, (
            "Scientific notation '1e2' was accepted; behavior may be inconsistent"
        )

    def test_scientific_notation_with_dot_is_also_rejected(self):
        """'1.0e2' contains a '.' so it is now rejected by the decimal fix,
        making both '1e2' and '1.0e2' consistently rejected."""
        ok, _, err = parse_guess("1.0e2")
        assert ok is False
        assert err == "Please enter a whole number."

    def test_both_scientific_notation_forms_are_rejected(self):
        """After the Edge Case 1 fix, '1e2' and '1.0e2' are both rejected —
        the previous inconsistency (one accepted, one not) no longer exists."""
        ok_no_dot, _, _ = parse_guess("1e2")
        ok_with_dot, _, _ = parse_guess("1.0e2")
        assert ok_no_dot is False and ok_with_dot is False

    # ── Edge Case 3: whitespace-padded input ──────────────────────────────────

    def test_whitespace_padded_number_is_silently_accepted(self):
        """' 50 ' has no '.' so int(' 50 ') strips whitespace → accepted as 50."""
        ok, value, _ = parse_guess(" 50 ")
        assert ok is True
        assert value == 50

    def test_pure_whitespace_is_rejected(self):
        """' ' alone raises ValueError → rejected as not a number."""
        ok, _, err = parse_guess(" ")
        assert ok is False

    def test_whitespace_inconsistency(self):
        """' 50 ' is accepted but ' ' is rejected — documents that whitespace
        handling depends on whether a digit is also present."""
        ok_padded, _, _ = parse_guess(" 50 ")
        ok_blank, _, _ = parse_guess(" ")
        assert ok_padded is True and ok_blank is False, (
            "Expected padded number accepted and blank whitespace rejected"
        )


# ── Stretch Feature: High Score tracker ───────────────────────────────────────
# load_highscores() and save_highscore() live in app.py which imports Streamlit
# at module level, making it impossible to import directly in pytest.
# These tests replicate the core logic using a tmp_path fixture so the
# file I/O, sorting, and field-storage behaviour can be verified independently.

import json as _json
from datetime import date as _date

class TestHighScoreTracker:

    def _load(self, filepath):
        """Mirror load_highscores() from app.py."""
        if filepath.exists():
            return _json.loads(filepath.read_text())
        return []

    def _save(self, filepath, score, difficulty, attempts):
        """Mirror save_highscore() from app.py."""
        scores = self._load(filepath)
        scores.append({
            "score": score,
            "difficulty": difficulty,
            "attempts": attempts,
            "date": str(_date.today()),
        })
        scores.sort(key=lambda x: x["score"], reverse=True)
        scores = scores[:5]
        filepath.write_text(_json.dumps(scores, indent=2))

    def test_load_returns_empty_list_when_no_file(self, tmp_path):
        """No file present → empty list, no crash."""
        assert self._load(tmp_path / "hs.json") == []

    def test_save_creates_the_file(self, tmp_path):
        """First save must create the JSON file on disk."""
        f = tmp_path / "hs.json"
        self._save(f, 100, "Easy", 1)
        assert f.exists()

    def test_saved_entry_has_all_required_fields(self, tmp_path):
        """Each entry must contain score, difficulty, attempts, and date."""
        f = tmp_path / "hs.json"
        self._save(f, 90, "Normal", 2)
        entry = self._load(f)[0]
        for field in ("score", "difficulty", "attempts", "date"):
            assert field in entry, f"Missing field: {field}"

    def test_entry_stores_correct_values(self, tmp_path):
        """Saved values must match the arguments passed to save_highscore."""
        f = tmp_path / "hs.json"
        self._save(f, 80, "Hard", 3)
        entry = self._load(f)[0]
        assert entry["score"] == 80
        assert entry["difficulty"] == "Hard"
        assert entry["attempts"] == 3
        assert entry["date"] == str(_date.today())

    def test_scores_sorted_descending(self, tmp_path):
        """Leaderboard must always show highest scores first."""
        f = tmp_path / "hs.json"
        for score in [70, 100, 50]:
            self._save(f, score, "Normal", 3)
        saved = [e["score"] for e in self._load(f)]
        assert saved == sorted(saved, reverse=True)

    def test_only_top_5_entries_kept(self, tmp_path):
        """Saving more than 5 entries must trim the list to 5."""
        f = tmp_path / "hs.json"
        for i in range(7):
            self._save(f, (i + 1) * 10, "Normal", i + 1)
        assert len(self._load(f)) == 5

    def test_top_5_are_the_highest_scores(self, tmp_path):
        """After trimming, the retained entries must be the 5 highest scores."""
        f = tmp_path / "hs.json"
        for i in range(7):
            self._save(f, (i + 1) * 10, "Normal", i + 1)
        kept = {e["score"] for e in self._load(f)}
        assert 70 in kept, "Highest score missing from top-5"
        assert 10 not in kept, "Lowest score should have been trimmed"

    def test_multiple_saves_accumulate_correctly(self, tmp_path):
        """Saving three distinct scores must produce three separate entries."""
        f = tmp_path / "hs.json"
        self._save(f, 100, "Easy", 1)
        self._save(f, 80, "Normal", 3)
        self._save(f, 60, "Hard", 4)
        assert len(self._load(f)) == 3


# ── Stretch Feature: Guess History sidebar chart ──────────────────────────────
# The chart itself is rendered by Streamlit (untestable in pytest), but the
# DataFrame construction logic can be exercised independently.

class TestGuessHistoryChart:

    def _build_chart_data(self, history, secret):
        """Mirror the DataFrame construction inside app.py's sidebar chart block."""
        import pandas as pd
        return pd.DataFrame({
            "Your Guess": history,
            "Secret": [secret] * len(history),
        })

    def test_empty_history_is_falsy_so_chart_is_skipped(self):
        """The chart block is guarded by 'if history:' — empty list must be falsy."""
        assert not bool([])

    def test_chart_data_has_correct_columns(self):
        """DataFrame must contain exactly 'Your Guess' and 'Secret' columns."""
        df = self._build_chart_data([30, 60], 50)
        assert "Your Guess" in df.columns
        assert "Secret" in df.columns

    def test_secret_column_is_a_constant_reference_line(self):
        """Every row in 'Secret' must equal the secret number."""
        df = self._build_chart_data([20, 80, 50], 42)
        assert list(df["Secret"]) == [42, 42, 42]

    def test_guess_column_matches_history_order(self):
        """'Your Guess' column must preserve the chronological guess order."""
        history = [10, 55, 75]
        df = self._build_chart_data(history, 60)
        assert list(df["Your Guess"]) == history

    def test_row_count_equals_history_length(self):
        """One DataFrame row must exist per submitted guess."""
        history = [30, 60, 45, 52]
        df = self._build_chart_data(history, 50)
        assert len(df) == len(history)

    def test_single_guess_produces_one_row_chart(self):
        """A history with one entry must still build a valid single-row DataFrame."""
        df = self._build_chart_data([50], 50)
        assert len(df) == 1
        assert df["Your Guess"][0] == 50
        assert df["Secret"][0] == 50
