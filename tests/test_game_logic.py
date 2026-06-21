import pytest

from logic_utils import check_guess, update_score


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


@pytest.mark.parametrize("attempt_number", [1, 2, 3, 4, 5, 6, 7, 8])
def test_wrong_guess_never_increases_score(attempt_number):
    # Regression: "Too High" on even attempts used to ADD 5 points,
    # rewarding a wrong guess. A wrong guess must always lose points,
    # regardless of which attempt it is.
    assert update_score(100, "Too High", attempt_number) == 95
    assert update_score(100, "Too Low", attempt_number) == 95


def test_too_high_and_too_low_are_penalized_equally():
    # Both wrong outcomes should cost the same; they were inconsistent before.
    assert (
        update_score(50, "Too High", 4)
        == update_score(50, "Too Low", 4)
        == 45
    )


def test_first_attempt_win_awards_full_points():
    # Regression: the win formula used (attempt_number + 1), so a first-try
    # win paid less than 100. Winning on attempt 1 should award the full 100.
    assert update_score(0, "Win", 1) == 100


def test_win_points_decrease_with_more_attempts():
    # Each additional attempt drops the reward by 10.
    assert update_score(0, "Win", 2) == 90
    assert update_score(0, "Win", 3) == 80


def test_win_points_floor_at_ten():
    # Late wins are floored at 10 points, never negative.
    assert update_score(0, "Win", 20) == 10
