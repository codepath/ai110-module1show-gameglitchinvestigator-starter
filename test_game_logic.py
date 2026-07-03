from logic_utils import check_guess

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

def test_guess_out_of_range_low():
    # If guess is less than 1, it should return "Invalid"
    result = check_guess(0, 50)
    assert result == ("Invalid", "❌ Guess must be between 1 and 100!")

def test_guess_out_of_range_high():
    # If guess is greater than 100, it should return "Invalid"
    result = check_guess(101, 50)
    assert result == ("Invalid", "❌ Guess must be between 1 and 100!")