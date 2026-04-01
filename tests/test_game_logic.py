from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

def test_winning_guess():
    # Test winning with different numbers from game ranges
    # Easy range (1-20): test with 10
    outcome, message = check_guess(10, 10)
    assert outcome == "Win"
    assert message == "🎉 Correct!"

    # Normal range (1-50): test with 35
    outcome, message = check_guess(35, 35)
    assert outcome == "Win"
    assert message == "🎉 Correct!"

def test_guess_too_high():
    # Test too high hints with numbers from actual game ranges
    # Easy range (1-20): secret=15, guess=18
    outcome, message = check_guess(18, 15)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"

    # Normal range (1-50): secret=22, guess=28
    outcome, message = check_guess(28, 22)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"

def test_guess_too_low():
    # Test too low hints with numbers from actual game ranges
    # Easy range (1-20): secret=12, guess=8
    outcome, message = check_guess(8, 12)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"

    # Normal range (1-50): secret=42, guess=35
    outcome, message = check_guess(35, 42)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


def test_get_range_for_difficulty():
    # Test the ranges for each difficulty level
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)
    # Test default case for invalid difficulty
    assert get_range_for_difficulty("Invalid") == (1, 100)


def test_parse_guess():
    # Test valid positive number
    ok, value, error = parse_guess("10")
    assert ok == True
    assert value == 10
    assert error is None

    # Test negative number
    ok, value, error = parse_guess("-5")
    assert ok == False
    assert value is None
    assert error == "Guess must be a positive number greater than zero."

    # Test zero
    ok, value, error = parse_guess("0")
    assert ok == False
    assert value is None
    assert error == "Guess must be a positive number greater than zero."

    # Test non-number
    ok, value, error = parse_guess("abc")
    assert ok == False
    assert value is None
    assert error == "That is not a number."

    # Test empty string
    ok, value, error = parse_guess("")
    assert ok == False
    assert value is None
    assert error == "Enter a guess."

    # Test None
    ok, value, error = parse_guess(None)
    assert ok == False
    assert value is None
    assert error == "Enter a guess."


def test_update_score():
    # Test winning with different attempt numbers
    # Win on attempt 1: 100 - 10*1 = 90 points
    assert update_score(0, "Win", 1) == 90
    assert update_score(50, "Win", 1) == 140  # current_score + 90

    # Win on attempt 5: 100 - 10*5 = 50 points
    assert update_score(0, "Win", 5) == 50

    # Win on attempt 10: 100 - 10*10 = 0, but min 10 points
    assert update_score(0, "Win", 10) == 10

    # Win on attempt 15: still min 10
    assert update_score(0, "Win", 15) == 10

    # Test incorrect guesses: Too High or Too Low deduct 5 points, but score never goes below 0
    assert update_score(0, "Too High", 1) == 0
    assert update_score(10, "Too High", 2) == 5  # 10 - 5 = 5
    assert update_score(0, "Too Low", 1) == 0
    assert update_score(20, "Too Low", 3) == 15

    # Test invalid outcome: return current_score unchanged
    assert update_score(100, "Invalid", 1) == 100
