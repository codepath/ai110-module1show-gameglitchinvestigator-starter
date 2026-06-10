import pytest

from logic_utils import check_guess


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_guess_too_high():
    # Guess above the secret -> "Too High", and the hint should point LOWER
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_guess_too_low():
    # Guess below the secret -> "Too Low", and the hint should point HIGHER
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


@pytest.mark.parametrize(
    "guess, secret, expected_outcome",
    [
        # str/int mismatches must compare numerically, not lexicographically.
        # "9" vs 10: lexicographic comparison would wrongly call this "Too High".
        ("9", 10, "Too Low"),
        (9, "10", "Too Low"),
        ("100", 20, "Too High"),
        ("50", 50, "Win"),
    ],
)
def test_handles_type_mismatch_numerically(guess, secret, expected_outcome):
    outcome, _ = check_guess(guess, secret)
    assert outcome == expected_outcome
