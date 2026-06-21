from logic_utils import check_guess


# These tests target the inverted-hint bug fixed in check_guess:
# "Too High" (guess bigger than secret) must tell the player to go LOWER,
# and "Too Low" must tell them to go HIGHER. Asserting on the message
# direction — not just the outcome label — is what actually pins the bug,
# since the original code returned the right label with the wrong arrow.

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_too_high_tells_player_to_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    # Regression: a guess above the secret must point the player LOWER.
    assert "LOWER" in message
    assert "HIGHER" not in message


def test_too_low_tells_player_to_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    # Regression: a guess below the secret must point the player HIGHER.
    assert "HIGHER" in message
    assert "LOWER" not in message


# The string-comparison fallback (TypeError branch) carried the same
# inverted-hint bug. It triggers when secret is a str and guess is an int,
# which is exactly the type-mismatch path the game could hit.

def test_string_fallback_win():
    outcome, message = check_guess(50, "50")
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_string_fallback_too_high_goes_lower():
    outcome, message = check_guess(60, "50")
    assert outcome == "Too High"
    assert "LOWER" in message


def test_string_fallback_too_low_goes_higher():
    outcome, message = check_guess(40, "50")
    assert outcome == "Too Low"
    assert "HIGHER" in message
