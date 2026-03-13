# FIX: Regression tests added using Claude AI Agent mode.
# I (user) described the bugs found during gameplay; Claude generated targeted pytest cases
# to lock in the correct behavior and prevent the same bugs from reappearing.
from logic_utils import check_guess

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

# Bug regression: hint messages were swapped — "Too High" was showing "Go HIGHER!" and vice versa
def test_too_high_message_says_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in message for Too High, got: {message!r}"

def test_too_low_message_says_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in message for Too Low, got: {message!r}"

# Bug regression: TypeError fallback used str(guess) instead of int(guess),
# causing lexicographic comparison — e.g., "9" > "10" is True, so guess=9 vs secret="10"
# would wrongly return "Too High" instead of "Too Low".
def test_string_secret_type_mismatch_too_low():
    outcome, _ = check_guess(9, "10")
    assert outcome == "Too Low", f"Expected 'Too Low' for guess=9 vs secret='10', got: {outcome!r}"

def test_string_secret_type_mismatch_too_high():
    outcome, _ = check_guess(20, "10")
    assert outcome == "Too High", f"Expected 'Too High' for guess=20 vs secret='10', got: {outcome!r}"

def test_string_secret_type_mismatch_win():
    outcome, _ = check_guess(10, "10")
    assert outcome == "Win", f"Expected 'Win' for guess=10 vs secret='10', got: {outcome!r}"
