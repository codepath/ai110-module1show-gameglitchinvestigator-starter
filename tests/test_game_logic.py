from logic_utils import check_guess, get_proximity_label, parse_guess, update_score


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


def test_win_on_first_attempt_scores_90_not_80():
    # Regression test for the off-by-one bug: formula used to be
    # 100 - 10 * (attempt_number + 1), scoring 80 instead of 90.
    result = update_score(current_score=0, outcome="Win", attempt_number=1)
    assert result == 90


def test_too_high_always_deducts_even_on_even_attempt():
    # Regression test for the parity bug: "Too High" used to add +5
    # instead of -5 when attempt_number was even.
    result = update_score(current_score=0, outcome="Too High", attempt_number=2)
    assert result == -5


# --- Challenge 1: Advanced Edge-Case Testing ---

def test_parse_guess_none_returns_error():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_empty_string_returns_error():
    ok, value, err = parse_guess("")
    assert ok is False
    assert err == "Enter a guess."


def test_parse_guess_whitespace_is_not_a_number():
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert err == "That is not a number."


def test_parse_guess_non_numeric_string_returns_error():
    ok, value, err = parse_guess("banana")
    assert ok is False
    assert err == "That is not a number."


def test_parse_guess_decimal_string_truncates_to_int():
    ok, value, err = parse_guess("12.7")
    assert ok is True
    assert value == 12
    assert err is None


def test_parse_guess_negative_number_is_accepted():
    ok, value, err = parse_guess("-15")
    assert ok is True
    assert value == -15


def test_check_guess_handles_negative_numbers():
    assert check_guess(-10, -5) == "Too Low"
    assert check_guess(-3, -5) == "Too High"
    assert check_guess(-5, -5) == "Win"


def test_update_score_win_floor_clamps_at_10():
    # Late-game win (attempt 15) should clamp to the 10-point floor,
    # not go negative.
    result = update_score(current_score=0, outcome="Win", attempt_number=15)
    assert result == 10


def test_update_score_unknown_outcome_leaves_score_unchanged():
    result = update_score(current_score=42, outcome="Unknown", attempt_number=1)
    assert result == 42


# --- Known edge cases that can still trip up the game (not yet fixed) ---

def test_check_guess_accepts_out_of_range_guesses():
    # No bounds check against the difficulty's low/high: an absurd guess is
    # still compared normally instead of being rejected as out of range.
    assert check_guess(999999999, 50) == "Too High"


def test_update_score_has_no_floor_on_the_way_down():
    # Unlike the win formula's 10-point floor, wrong guesses keep
    # subtracting 5 with no lower bound.
    result = update_score(current_score=-100, outcome="Too Low", attempt_number=1)
    assert result == -105


def test_parse_guess_negative_decimal_truncates_toward_zero():
    # int(float(...)) truncates toward zero, not floor, so "-0.5" becomes
    # 0 instead of -1 -- a surprising rounding direction for negatives.
    ok, value, err = parse_guess("-0.5")
    assert ok is True
    assert value == 0


# --- Challenge 4: Enhanced UI -- Hot/Cold proximity labels ---

def test_proximity_label_exact_match_is_spot_on():
    assert get_proximity_label(50, 50, 1, 100) == "🎯 Spot On!"


def test_proximity_label_close_guess_is_hot():
    assert get_proximity_label(48, 50, 1, 100) == "🔥 Hot"


def test_proximity_label_mid_distance_is_warm():
    assert get_proximity_label(70, 50, 1, 100) == "🌡️ Warm"


def test_proximity_label_far_guess_is_cold():
    assert get_proximity_label(100, 50, 1, 100) == "🧊 Cold"
