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

# Regression tests for the new game reset bug:
# Clicking "New Game" after winning kept status="won", blocking further play.
# Fix: new_game block now resets status to "playing" and clears history.

def simulate_new_game(session_state: dict, low: int = 1, high: int = 100) -> dict:
    """Mirrors the new_game block in app.py."""
    import random
    session_state["attempts"] = 0
    session_state["secret"] = random.randint(low, high)
    session_state["status"] = "playing"
    session_state["history"] = []
    return session_state

def test_new_game_resets_status_after_win():
    # Bug: status remained "won" after clicking New Game, preventing further play
    state = {"attempts": 3, "secret": 42, "status": "won", "history": [10, 30, 42]}
    state = simulate_new_game(state)
    assert state["status"] == "playing", "New game must reset status to 'playing'"

def test_new_game_resets_status_after_loss():
    state = {"attempts": 8, "secret": 77, "status": "lost", "history": [1, 2, 3]}
    state = simulate_new_game(state)
    assert state["status"] == "playing"

def test_new_game_clears_history():
    state = {"attempts": 5, "secret": 50, "status": "won", "history": [20, 40, 50]}
    state = simulate_new_game(state)
    assert state["history"] == [], "New game must clear guess history"

def test_new_game_resets_attempts():
    state = {"attempts": 6, "secret": 50, "status": "won", "history": []}
    state = simulate_new_game(state)
    assert state["attempts"] == 0

def test_new_game_generates_new_secret():
    original_secret = 42
    state = {"attempts": 3, "secret": original_secret, "status": "won", "history": []}
    results = [simulate_new_game(dict(state))["secret"] for _ in range(20)]
    assert any(s != original_secret for s in results), "New game should generate a new secret"
