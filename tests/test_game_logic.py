from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

# Regression tests for the swapped high/low message bug:
# guess=15, secret=91 was showing "Go LOWER!" instead of "Go HIGHER!"
# guess=51, secret=2 was showing "Go HIGHER!" instead of "Go LOWER!"

def test_low_guess_message_says_go_higher():
    # Reported bug: guess=15, secret=91 displayed "Go LOWER!" incorrectly
    outcome, message = check_guess(15, 91)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'Go HIGHER!' but got: {message}"

def test_high_guess_message_says_go_lower():
    # Reported bug: guess=51, secret=2 displayed "Go HIGHER!" incorrectly
    outcome, message = check_guess(51, 2)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'Go LOWER!' but got: {message}"
