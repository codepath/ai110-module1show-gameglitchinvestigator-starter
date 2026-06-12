from logic_utils import check_guess

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Tests targeting the swapped-hint bug ---

def test_too_high_hint_says_go_lower():
    # Bug: hint used to say "Go HIGHER!" when guess was above secret
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message, f"Expected hint to say LOWER, got: {message}"
    assert "HIGHER" not in message, f"Hint should not say HIGHER when guess is too high"

def test_too_low_hint_says_go_higher():
    # Bug: hint used to say "Go LOWER!" when guess was below secret
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message, f"Expected hint to say HIGHER, got: {message}"
    assert "LOWER" not in message, f"Hint should not say LOWER when guess is too low"


# --- Tests targeting the string/int type-mismatch bug ---

def test_check_guess_with_int_secret():
    # Bug: on even attempts the caller passed secret as str, breaking comparison
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_check_guess_hint_consistent_across_values():
    # Ensures no TypeError is raised and hint direction is correct for various inputs
    for guess, secret, expected_outcome in [
        (1,   100, "Too Low"),
        (100, 1,   "Too High"),
        (99,  100, "Too Low"),
        (100, 99,  "Too High"),
    ]:
        outcome, message = check_guess(guess, secret)
        assert outcome == expected_outcome, f"check_guess({guess}, {secret}) → {outcome}, want {expected_outcome}"
