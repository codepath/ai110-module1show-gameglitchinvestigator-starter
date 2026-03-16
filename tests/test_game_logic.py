from logic_utils import check_guess, parse_guess

# FIX: Tests updated to unpack the (outcome, message) tuple returned by check_guess.
# New tests added with Claude Code to cover the backwards hint bug and parse_guess edge cases.

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_message_says_lower():
    # FIX: Previously this message said "Go HIGHER" — verifying the hint now correctly says lower
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_message_says_higher():
    # FIX: Previously this message said "Go LOWER" — verifying the hint now correctly says higher
    _, message = check_guess(40, 50)
    assert "HIGHER" in message

def test_parse_guess_valid():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_empty():
    ok, value, err = parse_guess("")
    assert ok is False
    assert err == "Enter a guess."

def test_parse_guess_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert err == "That is not a number."
