from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == ("Win", "🎉 Correct!")

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == ("Too High", "📉 Go LOWER!")

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == ("Too Low", "📈 Go HIGHER!")


def test_check_guess_regression_string_secret_and_hint_direction():
    # Regression: check_guess should work even when secret is a string,
    # and directional hints must match the numeric comparison.
    assert check_guess(75, "50") == ("Too High", "📉 Go LOWER!")
    assert check_guess(25, "50") == ("Too Low", "📈 Go HIGHER!")
    assert check_guess(50, "50") == ("Win", "🎉 Correct!")
