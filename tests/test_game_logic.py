from logic_utils import check_guess, get_range_for_difficulty, parse_guess
import random
# FIX: refactored logic so it only compares to the outcome and not the message

def test_new_game_resets_state_after_loss():
    # Simulate a finished (lost) game state
    state = {
        "secret": 42,
        "attempts": 5,
        "score": 10,
        "status": "lost",
        "difficulty": "Normal",
        "history": [10, 20, 30, 40, 50],
    }

    # Simulate pressing "New Game" — mirrors the handler in app.py
    new_difficulty = "Easy"
    low, high = get_range_for_difficulty(new_difficulty)
    state["attempts"] = 0
    state["secret"] = random.randint(low, high)
    state["score"] = 0
    state["status"] = "playing"
    state["difficulty"] = new_difficulty
    state["history"] = []

    assert state["status"] == "playing"
    assert state["attempts"] == 0
    assert state["score"] == 0
    assert state["history"] == []
    assert low <= state["secret"] <= high

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result[0] == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result[0] == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result[0] == "Too Low"


def test_difficulty_ranges():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (21, 50)
    assert get_range_for_difficulty("Hard") == (51, 100)


def test_parse_guess_rejects_non_whole_numbers():
    # Decimal numbers should be rejected
    ok, val, _ = parse_guess("3.14")
    assert ok is False
    assert val is None

    # Words should be rejected with a ValueError (not a bare Exception)
    ok, val, _ = parse_guess("abc")
    assert ok is False
    assert val is None

    # Empty string should be rejected
    ok, val, _ = parse_guess("")
    assert ok is False
    assert val is None
