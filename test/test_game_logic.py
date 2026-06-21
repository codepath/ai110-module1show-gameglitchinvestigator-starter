"""Tests for the guessing-game logic in logic_utils.py."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from logic_utils import check_guess

def test_guess_too_high_says_go_lower():
    # 60 is higher than the secret 50, so the player should be told to go LOWER.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()


def test_guess_too_low_says_go_higher():
    # 40 is lower than the secret 50, so the player should be told to go HIGHER.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()


def test_correct_guess_wins():
    # 50 matches the secret 50, so this is a win.
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
