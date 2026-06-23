from logic_utils import check_guess, parse_guess, hint_for_outcome

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

#FIX: Wrote small test for parsing the right values
#FIX: Revised test for multiple inputs test
def test_parse_guess_only_accepts_integers():
    # Whole numbers parse to an int; decimals and non-numbers are rejected.
    # Valid integer
    assert parse_guess("7") == (True, 7, None)

    # Float should fail
    assert parse_guess("3.5") == (False, None, "That is not a whole number.")

    # Non-numeric string
    assert parse_guess("abc") == (False, None, "That is not a whole number.")

    # Empty input
    assert parse_guess("") == (False, None, "Enter a guess.")
    assert parse_guess("   ") == (False, None, "Enter a guess.")

    # None input
    assert parse_guess(None) == (False, None, "Enter a guess.")

    # Valid with whitespace
    assert parse_guess(" 10 ") == (True, 10, None)

#FIX: Wrote small test for checking right hint message / comparison to secret value
def test_hint_direction_is_correct():
    # Too High -> tell the player to go LOWER; Too Low -> go HIGHER.
    assert "LOWER" in hint_for_outcome("Too High")
    assert "HIGHER" in hint_for_outcome("Too Low")
