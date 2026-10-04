from logic_utils import check_guess, get_range_for_difficulty, update_score

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

def test_guess_too_high_is_consistent_across_attempts():
    # Bug: the secret used to be coerced to a string on every other
    # attempt (attempts % 2 == 0), which made comparisons unreliable
    # and could flip a "Too High" guess into a false "Too Low"/"Win".
    # A guess of 60 against a secret of 50 must always read "Too High",
    # regardless of which attempt number it is.
    for attempt_number in range(1, 6):
        assert check_guess(60, 50) == "Too High"

def test_range_for_easy_difficulty():
    # Bug: the "Make a guess" info message was hardcoded to "1 and 100"
    # for every difficulty. Easy should actually span 1-20.
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_range_for_normal_difficulty():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_range_for_hard_difficulty():
    # Bug: Hard also displayed "1 and 100" instead of its real 1-50 range.
    assert get_range_for_difficulty("Hard") == (1, 50)

def test_too_high_scoring_is_consistent():
    # Bug: "Too High" used to award +5 on even attempts and -5 on odd
    # attempts, so the score depended on attempt parity instead of
    # being a consistent penalty.
    score_after_attempt_1 = update_score(current_score=0, outcome="Too High", attempt_number=1)
    score_after_attempt_2 = update_score(current_score=0, outcome="Too High", attempt_number=2)
    assert score_after_attempt_1 == score_after_attempt_2 == -5
