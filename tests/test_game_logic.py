from logic_utils import check_guess, get_range_for_difficulty

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

def test_too_high_hint_says_go_lower():
    # If guess (60) is higher than secret (50), the hint must tell the
    # player to go LOWER, not HIGHER.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()
    assert "HIGHER" not in message.upper()

def test_too_low_hint_says_go_higher():
    # If guess (40) is lower than secret (50), the hint must tell the
    # player to go HIGHER, not LOWER.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()
    assert "LOWER" not in message.upper()

def test_harder_difficulty_has_wider_range():
    # Higher difficulty should make the game harder by widening the
    # guessing range, not narrowing it. "Hard" must cover at least as
    # many numbers as "Normal", which must cover at least as many as "Easy".
    easy_low, easy_high = get_range_for_difficulty("Easy")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")

    easy_span = easy_high - easy_low
    normal_span = normal_high - normal_low
    hard_span = hard_high - hard_low

    assert easy_span < normal_span
    assert normal_span < hard_span
