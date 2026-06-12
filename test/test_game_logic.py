"""
Regression tests for the guessing-game logic in logic_utils.py.

These specifically target the high/low hint bug in check_guess: the game
used to tell you to "Go HIGHER" when your guess was too high (and vice
versa). The hint direction must be the OPPOSITE of how the guess missed.
"""
import os
import sys

import pytest

# Make logic_utils importable when running pytest from anywhere.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_utils import check_guess


class TestCheckGuessDirection:
    """The hint must point toward the secret, not away from it."""

    def test_guess_too_high_says_go_lower(self):
        outcome, message = check_guess(80, 50)
        assert outcome == "Too High"
        # Bug was: this returned "Go HIGHER". It must tell the player to go lower.
        assert "LOWER" in message.upper()
        assert "HIGHER" not in message.upper()

    def test_guess_too_low_says_go_higher(self):
        outcome, message = check_guess(20, 50)
        assert outcome == "Too Low"
        # Bug was: this returned "Go LOWER". It must tell the player to go higher.
        assert "HIGHER" in message.upper()
        assert "LOWER" not in message.upper()

    def test_correct_guess_wins(self):
        outcome, message = check_guess(50, 50)
        assert outcome == "Win"
        assert "Correct" in message

    @pytest.mark.parametrize(
        "guess, secret, expected_outcome",
        [
            (2, 1, "Too High"),
            (1, 2, "Too Low"),
            (100, 99, "Too High"),
            (99, 100, "Too Low"),
        ],
    )
    def test_outcome_matches_comparison(self, guess, secret, expected_outcome):
        outcome, _ = check_guess(guess, secret)
        assert outcome == expected_outcome

    @pytest.mark.parametrize(
        "guess, secret",
        [(80, 50), (20, 50), (2, 1), (1, 2)],
    )
    def test_hint_direction_is_consistent_with_outcome(self, guess, secret):
        """A "Too High" outcome must never tell the player to go higher."""
        outcome, message = check_guess(guess, secret)
        msg = message.upper()
        if outcome == "Too High":
            assert "LOWER" in msg and "HIGHER" not in msg
        elif outcome == "Too Low":
            assert "HIGHER" in msg and "LOWER" not in msg


class TestCheckGuessTypeErrorFallback:
    """
    The fallback path (mismatched types -> string comparison) was also part
    of the bug and must give the same corrected hint direction.
    """

    def test_string_secret_too_high_says_go_lower(self):
        # int 5 vs str "3": "5" > "3" as strings -> Too High
        outcome, message = check_guess(5, "3")
        assert outcome == "Too High"
        assert "LOWER" in message.upper()
        assert "HIGHER" not in message.upper()

    def test_string_secret_too_low_says_go_higher(self):
        # int 3 vs str "5": "3" < "5" as strings -> Too Low
        outcome, message = check_guess(3, "5")
        assert outcome == "Too Low"
        assert "HIGHER" in message.upper()
        assert "LOWER" not in message.upper()
