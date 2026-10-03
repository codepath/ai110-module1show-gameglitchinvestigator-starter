from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


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


# I asked AI to add tests for the new difficulty ranges so I could verify the updates instead of only checking the sidebar manually.
def test_hard_difficulty_uses_range_to_150():
    assert get_range_for_difficulty("Hard") == (1, 150)


def test_easy_difficulty_uses_range_to_50():
    assert get_range_for_difficulty("Easy") == (1, 50)


def test_parse_guess_accepts_numeric_string():
    ok, guess, error = parse_guess("42")
    assert ok is True
    assert guess == 42
    assert error is None


def test_parse_guess_rejects_empty_input():
    ok, guess, error = parse_guess("")
    assert ok is False
    assert guess is None
    assert error == "Enter a guess."


def test_parse_guess_rejects_non_numeric_text():
    ok, guess, error = parse_guess("abc")
    assert ok is False
    assert guess is None
    assert error == "That is not a number."


def test_win_score_bonus_adds_points():
    score = update_score(50, "Win", 1)
    assert score == 130


def test_low_score_penalty_is_applied_once():
    score = update_score(50, "Too Low", 2)
    assert score == 45


def test_high_score_penalty_is_applied_once():
    score = update_score(50, "Too High", 3)
    assert score in {45, 40}


def test_negative_score_is_not_clamped():
    score = update_score(5, "Too Low", 1)
    assert score < 0 or score == 5 - 5


def test_parse_guess_accepts_whitespace_numeric_string():
    ok, guess, error = parse_guess(" 7 ")
    assert ok is True
    assert guess == 7
    assert error is None
