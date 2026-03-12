from logic_utils import check_guess, get_range_for_difficulty, parse_guess

# Regression tests for the swapped difficulty range bug:
# Normal was returning (1, 100) and Hard was returning (1, 50) — they were swapped.

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert (low, high) == (1, 20), f"Easy should be 1–20, got {low}–{high}"

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert (low, high) == (1, 50), f"Normal should be 1–50, got {low}–{high}"

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert (low, high) == (1, 100), f"Hard should be 1–100, got {low}–{high}"

def test_hard_range_is_wider_than_normal():
    # Catch the swap: Hard must have a higher ceiling than Normal
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, "Hard difficulty should have a wider range than Normal"


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


# Regression tests for the invalid-input bug:
# Submitting a non-numeric input (e.g. ".") was incrementing attempts and
# appending the raw string to history, allowing attempts to go negative.
# Fix: attempts and history are only updated for valid (parseable) guesses.


def simulate_submit(session_state: dict, raw_guess: str) -> dict:
    """Mirrors the fixed submit block in app.py."""
    ok, guess_int, _ = parse_guess(raw_guess)
    if ok:
        session_state["attempts"] += 1
        session_state["history"].append(guess_int)
    return session_state


def test_invalid_input_does_not_increment_attempts():
    # Bug: submitting "." incremented attempts even though it is not a valid guess
    state = {"attempts": 3, "history": []}
    state = simulate_submit(state, ".")
    assert state["attempts"] == 3, "Invalid input must not increment attempts"


def test_invalid_input_not_added_to_history():
    # Bug: submitting "." appended the raw string to history
    state = {"attempts": 0, "history": []}
    state = simulate_submit(state, ".")
    assert state["history"] == [], "Invalid input must not be added to history"


def test_non_numeric_string_does_not_increment_attempts():
    state = {"attempts": 2, "history": []}
    state = simulate_submit(state, "abc")
    assert state["attempts"] == 2, "Non-numeric input must not increment attempts"


def test_non_numeric_string_not_added_to_history():
    state = {"attempts": 0, "history": []}
    state = simulate_submit(state, "abc")
    assert state["history"] == [], "Non-numeric input must not be added to history"


def test_valid_input_increments_attempts():
    # Confirm valid guesses still work correctly after the fix
    state = {"attempts": 2, "history": []}
    state = simulate_submit(state, "42")
    assert state["attempts"] == 3


def test_valid_input_added_to_history():
    state = {"attempts": 0, "history": []}
    state = simulate_submit(state, "42")
    assert state["history"] == [42]
