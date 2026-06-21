from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


# ---------------------------------------------------------------------------
# check_guess
# ---------------------------------------------------------------------------
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_check_guess_is_numeric_not_lexicographic():
    # Regression: 9 vs 100 must compare numerically, not as strings.
    # ("9" > "100" is True lexicographically, which was the original bug.)
    assert check_guess(9, 100)[0] == "Too Low"
    assert check_guess(100, 9)[0] == "Too High"


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# ---------------------------------------------------------------------------
def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)


def test_range_hard_is_hardest():
    low, high = get_range_for_difficulty("Hard")
    # Hard must span a wider range than Normal, or it isn't "hard".
    _, normal_high = get_range_for_difficulty("Normal")
    assert high > normal_high


def test_range_unknown_defaults_to_normal():
    assert get_range_for_difficulty("Banana") == (1, 100)


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------
def test_parse_valid_integer():
    assert parse_guess("42") == (True, 42, None)


def test_parse_float_string_truncates_to_int():
    ok, value, err = parse_guess("3.9")
    assert ok is True
    assert value == 3
    assert err is None


def test_parse_empty_string_is_error():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_none_is_error():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_non_number_is_error():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------
def test_win_on_first_attempt_scores_high():
    # attempt 1 win: 100 - 10*1 = 90 points
    assert update_score(0, "Win", 1) == 90


def test_win_points_floor_at_10():
    # A very late win should never score below the 10-point floor.
    assert update_score(0, "Win", 99) == 10


def test_wrong_guesses_consistently_cost_points():
    # Regression: "Too High" must not REWARD points on even attempts.
    assert update_score(100, "Too High", 2) == 95
    assert update_score(100, "Too High", 3) == 95
    assert update_score(100, "Too Low", 2) == 95
    assert update_score(100, "Too Low", 3) == 95


def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(50, "Whatever", 1) == 50
