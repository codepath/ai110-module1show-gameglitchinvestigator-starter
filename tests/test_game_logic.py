from logic_utils import check_guess, get_range_for_difficulty, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"

def test_hint_bug_fix():
    # Test the specific bug case: secret=11, guess=20 should be "Too High"
    outcome, message = check_guess(20, 11)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"

    # Test with secret as string (simulating the bug scenario)
    outcome, message = check_guess(20, "11")
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"

    # Test guess too low with string secret
    outcome, message = check_guess(5, "11")
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


def test_get_range_for_difficulty():
    # Test that difficulty ranges are correct, ensuring new game uses proper range
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)
    # Test default case
    assert get_range_for_difficulty("Invalid") == (1, 100)


def test_update_score():
    # Test winning on first attempt
    assert update_score(0, "Win", 0) == 90  # 100 - 10*(0+1) = 90
    # Test winning on later attempt
    assert update_score(0, "Win", 5) == 40  # 100 - 10*6 = 40
    # Test winning on last possible attempt
    assert update_score(0, "Win", 9) == 10  # 100 - 10*10 = 0, min 10

    # Test Too High on odd attempt (attempt_number starts from 0?)
    # Wait, in code: if attempt_number % 2 == 0: +5 else -5
    # But attempts start from 1 in submit, but attempt_number is st.session_state.attempts, which is incremented to 1 first.
    # For first guess, attempts=1, outcome checked, then score updated with attempt_number=1
    # So for "Too High" on first guess, attempt_number=1, 1%2==1, -5
    assert update_score(0, "Too High", 1) == -5
    # For second guess, attempts=2, attempt_number=2, 2%2==0, +5
    assert update_score(0, "Too High", 2) == 5

    # Test Too Low
    assert update_score(0, "Too Low", 1) == -5

    # Test invalid outcome
    assert update_score(0, "Invalid", 1) == 0
