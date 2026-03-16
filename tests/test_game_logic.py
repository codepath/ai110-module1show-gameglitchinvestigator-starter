from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_update_score_win_formula():
    # Attempt number 1 should grant 90 points (100 - 10*1)
    from logic_utils import update_score
    result = update_score(0, "Win", 1)
    assert result == 90


def test_update_score_upper_bound_minimum():
    # If the user wins on very late attempt, minimum 10 points still applied
    from logic_utils import update_score
    result = update_score(0, "Win", 20)
    assert result == 10
