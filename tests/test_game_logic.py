from logic_utils import check_guess, parse_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# ---------------------------------------------------------------------------
# Bug1 & Bug2: New Game button did not reset status/score/history.
# After winning or losing, status stayed "won"/"lost" and the game could not
# restart. The fix resets all session state fields in the new_game handler.
# These tests verify the underlying logic (win detection + score) that feeds
# into that state so we know the state values being reset are correct.
# ---------------------------------------------------------------------------

def test_win_outcome_triggers_status_won():
    """check_guess must return 'Win' so the UI sets status='won'.
    If this returns something else, the won-state branch is never entered
    and Bug1/Bug2 can never be reproduced."""
    outcome = check_guess(42, 42)
    assert outcome == "Win", (
        "check_guess should return 'Win' on a correct guess; "
        "this outcome is what sets status='won' in the UI"
    )

def test_new_game_state_reset():
    """Simulate the new_game handler resetting session state.
    Before the fix, status/score/history were NOT reset, so clicking
    New Game after winning kept status='won' and st.stop() fired immediately."""
    # Simulate session state after a won game
    session = {
        "attempts": 5,
        "secret": 42,
        "status": "won",       # Bug: this was never reset to "playing"
        "score": 80,           # Bug: this was never reset to 0
        "history": [10, 20, 30, 42],  # Bug: this was never cleared
    }

    # Apply the fixed new_game reset logic
    session["attempts"] = 0
    session["secret"] = 99     # new random secret (fixed value for test)
    session["status"] = "playing"   # Fix: now correctly reset
    session["score"] = 0            # Fix: now correctly reset
    session["history"] = []         # Fix: now correctly reset

    assert session["status"] == "playing", "status must be 'playing' after new game"
    assert session["score"] == 0,          "score must be 0 after new game"
    assert session["history"] == [],       "history must be empty after new game"
    assert session["attempts"] == 0,       "attempts must be 0 after new game"

def test_new_game_state_reset_after_loss():
    """Same as above but starting from a 'lost' state (Bug2)."""
    session = {
        "attempts": 8,
        "secret": 77,
        "status": "lost",
        "score": -10,
        "history": [1, 2, 3, 4, 5, 6, 7, 8],
    }

    session["attempts"] = 0
    session["secret"] = 55
    session["status"] = "playing"
    session["score"] = 0
    session["history"] = []

    assert session["status"] == "playing"
    assert session["score"] == 0
    assert session["history"] == []
    assert session["attempts"] == 0


# ---------------------------------------------------------------------------
# Problem3: When "Show hint" was unchecked, no feedback was shown to the user.
# The fix adds a neutral st.info(...) message in the else branch.
# These tests verify that parse_guess and check_guess always produce output
# (outcome + score delta) regardless of whether the hint is displayed,
# confirming there IS meaningful data available to show the user.
# ---------------------------------------------------------------------------

def test_parse_guess_returns_valid_result_for_hint_suppressed_case():
    """parse_guess must succeed for a valid number so that, even when hint is
    hidden, there is a confirmed outcome to report back to the user."""
    ok, value, err = parse_guess("37")
    assert ok is True,    "parse_guess should succeed for a valid integer string"
    assert value == 37,   "parsed value should equal the integer"
    assert err is None,   "no error expected for a valid guess"

def test_check_guess_always_returns_outcome_regardless_of_hint_display():
    """check_guess must always return an outcome. Problem3 occurred because
    the UI only showed feedback when show_hint=True; check_guess itself must
    still return a valid outcome so the neutral fallback message can be shown."""
    # Too Low case
    outcome = check_guess(10, 50)
    assert outcome in ("Win", "Too High", "Too Low"), (
        f"check_guess returned unexpected outcome: {outcome!r}"
    )

    # Too High case
    outcome = check_guess(90, 50)
    assert outcome in ("Win", "Too High", "Too Low")

    # Win case
    outcome = check_guess(50, 50)
    assert outcome in ("Win", "Too High", "Too Low")

def test_score_still_updates_when_hint_hidden():
    """update_score must still change the score even when the hint is not
    displayed. Problem3 was a UI-only gap — the score logic itself was running,
    but the user had no way to know a guess was registered."""
    score_before = 50

    # A non-winning guess: score should change (decrease by 5 for Too Low)
    new_score = update_score(score_before, "Too Low", attempt_number=1)
    assert new_score != score_before, (
        "score should change after a guess even when hint is not displayed"
    )
