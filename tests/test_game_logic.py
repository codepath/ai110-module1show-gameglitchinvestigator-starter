from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


def test_get_range_for_difficulty_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_get_range_for_difficulty_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)


def test_get_range_for_difficulty_hard():
    assert get_range_for_difficulty("Hard") == (1, 200)


def test_parse_guess_valid_float():
    ok, value, error = parse_guess("7.0", 1, 20)
    assert ok is True
    assert value == 7
    assert error is None


def test_parse_guess_reject_decimal():
    ok, value, error = parse_guess("9.9", 1, 20)
    assert ok is False
    assert value is None
    assert error == "Please enter a whole number."


def test_update_score_win_and_penalties():
    # win on first attempt
    assert update_score(0, "Win", 1) == 100
    # win on third attempt -> 100 - 10*(3-1) = 80
    assert update_score(0, "Win", 3) == 80
    # wrong guess penalty
    assert update_score(10, "Too High", 2) == 5


def test_parse_guess_out_of_range_low():
    ok, value, error = parse_guess("0", 1, 100)
    assert ok is False
    assert value is None
    assert error == "Guess must be between 1 and 100."


def test_parse_guess_out_of_range_high():
    ok, value, error = parse_guess("101", 1, 100)
    assert ok is False
    assert value is None
    assert error == "Guess must be between 1 and 100."


def test_check_guess_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_check_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_check_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"
