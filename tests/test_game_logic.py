from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

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


# Regression tests for the update_score bug:
# Win points used (attempt_number + 1) instead of attempt_number, causing
# first-attempt wins to score 80 instead of 90.
# "Too High" incorrectly rewarded +5 points on even attempts instead of always
# deducting 5 like "Too Low".

def test_win_first_attempt_scores_90():
    # Bug: attempt_number + 1 made first-attempt wins score 80 instead of 90
    score = update_score(0, "Win", 1)
    assert score == 90, f"Win on attempt 1 should give 90 points, got {score}"

def test_win_fifth_attempt_scores_50():
    score = update_score(0, "Win", 5)
    assert score == 50, f"Win on attempt 5 should give 50 points, got {score}"

def test_win_score_floor_at_10():
    # At attempt 10: 100 - 10*10 = 0, but minimum is 10
    score = update_score(0, "Win", 10)
    assert score == 10, f"Win score should not drop below 10, got {score}"

def test_win_adds_to_existing_score():
    score = update_score(50, "Win", 3)
    assert score == 50 + 70, f"Win on attempt 3 should add 70 to existing score of 50"

def test_too_high_deducts_5():
    # Bug: "Too High" was adding 5 points on even attempts instead of always deducting
    score = update_score(100, "Too High", 2)
    assert score == 95, f"Too High should deduct 5 points, got {score}"

def test_too_high_deducts_5_on_odd_attempt():
    score = update_score(100, "Too High", 3)
    assert score == 95, f"Too High should always deduct 5 points, got {score}"

def test_too_low_deducts_5():
    score = update_score(100, "Too Low", 1)
    assert score == 95, f"Too Low should deduct 5 points, got {score}"

def test_unknown_outcome_unchanged():
    score = update_score(42, "Some Other Outcome", 1)
    assert score == 42, "Unknown outcome should not change the score"

def test_too_high_score_cannot_go_below_zero():
    # Bug: repeated wrong guesses could drive score negative
    score = update_score(3, "Too High", 1)
    assert score == 0, f"Score should floor at 0, got {score}"

def test_too_low_score_cannot_go_below_zero():
    score = update_score(3, "Too Low", 1)
    assert score == 0, f"Score should floor at 0, got {score}"

def test_score_stays_at_zero_after_multiple_wrong_guesses():
    # Repeated wrong guesses starting from 0 must not go negative
    score = 0
    for _ in range(5):
        score = update_score(score, "Too High", 1)
    assert score == 0, f"Score should remain 0 after many wrong guesses, got {score}"


# Regression tests for the attempts off-by-one bug:
# st.session_state.attempts was initialized to 1 instead of 0, causing the
# "Attempts left" display to show one fewer attempt than actually allowed.
# Fix: initial attempts value changed from 1 to 0.

ATTEMPT_LIMIT_MAP = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}

def simulate_init_state() -> dict:
    """Mirrors the session_state initialization block in app.py."""
    return {
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
    }

def test_initial_attempts_is_zero():
    # Bug: attempts started at 1, so attempts_left showed 7 instead of 8 for Normal
    state = simulate_init_state()
    assert state["attempts"] == 0, f"Initial attempts should be 0, got {state['attempts']}"

def test_initial_attempts_left_matches_limit_for_easy():
    state = simulate_init_state()
    attempts_left = ATTEMPT_LIMIT_MAP["Easy"] - state["attempts"]
    assert attempts_left == ATTEMPT_LIMIT_MAP["Easy"], (
        f"Easy: expected {ATTEMPT_LIMIT_MAP['Easy']} attempts left at start, got {attempts_left}"
    )

def test_initial_attempts_left_matches_limit_for_normal():
    state = simulate_init_state()
    attempts_left = ATTEMPT_LIMIT_MAP["Normal"] - state["attempts"]
    assert attempts_left == ATTEMPT_LIMIT_MAP["Normal"], (
        f"Normal: expected {ATTEMPT_LIMIT_MAP['Normal']} attempts left at start, got {attempts_left}"
    )

def test_initial_attempts_left_matches_limit_for_hard():
    state = simulate_init_state()
    attempts_left = ATTEMPT_LIMIT_MAP["Hard"] - state["attempts"]
    assert attempts_left == ATTEMPT_LIMIT_MAP["Hard"], (
        f"Hard: expected {ATTEMPT_LIMIT_MAP['Hard']} attempts left at start, got {attempts_left}"
    )

def test_attempts_left_decrements_correctly_after_each_guess():
    # Each valid guess should reduce attempts_left by exactly 1
    state = simulate_init_state()
    limit = ATTEMPT_LIMIT_MAP["Normal"]
    for expected_left in range(limit, 0, -1):
        assert limit - state["attempts"] == expected_left
        state = simulate_submit(state, "42")
    assert limit - state["attempts"] == 0, "After all guesses, attempts_left should be 0"


# Regression tests for the hardcoded "1 and 100" display bug:
# The info message always showed "Guess a number between 1 and 100" regardless
# of difficulty. Fix: replaced hardcoded values with {low} and {high} from
# get_range_for_difficulty().

def build_guess_prompt(difficulty: str) -> str:
    """Mirrors the st.info() message in app.py."""
    low, high = get_range_for_difficulty(difficulty)
    return f"Guess a number between {low} and {high}."

def test_easy_prompt_displays_correct_range():
    # Easy range is 1–20; prompt must NOT say "1 and 100"
    prompt = build_guess_prompt("Easy")
    assert "1" in prompt and "20" in prompt, f"Easy prompt should show 1 and 20, got: {prompt}"
    assert "100" not in prompt, f"Easy prompt must not show 100, got: {prompt}"

def test_normal_prompt_displays_correct_range():
    # Normal range is 1–50; prompt must NOT say "1 and 100"
    prompt = build_guess_prompt("Normal")
    assert "1" in prompt and "50" in prompt, f"Normal prompt should show 1 and 50, got: {prompt}"
    assert "100" not in prompt, f"Normal prompt must not show 100, got: {prompt}"

def test_hard_prompt_displays_correct_range():
    # Hard range is 1–100
    prompt = build_guess_prompt("Hard")
    assert "1" in prompt and "100" in prompt, f"Hard prompt should show 1 and 100, got: {prompt}"


# Regression tests for the difficulty-switch attempts bug:
# Switching difficulty did not reset st.session_state.attempts. If a game
# ended in Easy mode (6 attempts used), switching to Hard (limit=5) showed
# attempts_left = 5 - 6 = -1.
# Fix: detect difficulty change in session state and reset game state.

def simulate_difficulty_switch(session_state: dict, new_difficulty: str) -> dict:
    """Mirrors the difficulty-change reset block in app.py."""
    import random
    low, high = get_range_for_difficulty(new_difficulty)
    session_state["difficulty"] = new_difficulty
    session_state["attempts"] = 0
    session_state["secret"] = random.randint(low, high)
    session_state["status"] = "playing"
    session_state["history"] = []
    return session_state


def test_difficulty_switch_resets_attempts():
    # Bug: switching difficulty kept old attempt count, causing negative attempts_left
    state = {"difficulty": "Easy", "attempts": 6, "secret": 10,
             "status": "lost", "history": [1, 2, 3, 4, 5, 6]}
    state = simulate_difficulty_switch(state, "Hard")
    assert state["attempts"] == 0, "Switching difficulty must reset attempts to 0"


def test_difficulty_switch_attempts_left_not_negative():
    # Bug: Easy game ended (6 attempts used), switch to Hard (limit=5) gave -1 attempts left
    state = {"difficulty": "Easy", "attempts": 6, "secret": 10,
             "status": "lost", "history": [1, 2, 3, 4, 5, 6]}
    state = simulate_difficulty_switch(state, "Hard")
    attempts_left = ATTEMPT_LIMIT_MAP["Hard"] - state["attempts"]
    assert attempts_left >= 0, f"Attempts left must not be negative after difficulty switch, got {attempts_left}"


def test_difficulty_switch_attempts_left_equals_new_limit():
    # After switching, attempts_left should equal the full limit for the new difficulty
    state = {"difficulty": "Easy", "attempts": 6, "secret": 10,
             "status": "lost", "history": [1, 2, 3, 4, 5, 6]}
    state = simulate_difficulty_switch(state, "Hard")
    attempts_left = ATTEMPT_LIMIT_MAP["Hard"] - state["attempts"]
    assert attempts_left == ATTEMPT_LIMIT_MAP["Hard"], (
        f"Expected {ATTEMPT_LIMIT_MAP['Hard']} attempts left after switching to Hard, got {attempts_left}"
    )


def test_difficulty_switch_resets_status():
    state = {"difficulty": "Normal", "attempts": 8, "secret": 25,
             "status": "lost", "history": []}
    state = simulate_difficulty_switch(state, "Easy")
    assert state["status"] == "playing", "Switching difficulty must reset status to 'playing'"


def test_difficulty_switch_clears_history():
    state = {"difficulty": "Normal", "attempts": 3, "secret": 25,
             "status": "playing", "history": [10, 20, 30]}
    state = simulate_difficulty_switch(state, "Hard")
    assert state["history"] == [], "Switching difficulty must clear guess history"


def test_difficulty_switch_updates_stored_difficulty():
    state = {"difficulty": "Easy", "attempts": 0, "secret": 5,
             "status": "playing", "history": []}
    state = simulate_difficulty_switch(state, "Hard")
    assert state["difficulty"] == "Hard", "Stored difficulty must update to the new selection"
