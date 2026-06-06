import pytest
from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


class TestCheckGuess:
    """Tests for check_guess function."""

    @pytest.mark.parametrize(
        "guess,secret,expected_outcome,expected_message",
        [
            (50, 50, "Win", "🎉 Correct!"),
            (60, 50, "Too High", "📉 Go LOWER!"),
            (40, 50, "Too Low", "📈 Go HIGHER!"),
            (50, "50", "Win", "🎉 Correct!"),
            (60, "50", "Too High", "📉 Go LOWER!"),
            (40, "50", "Too Low", "📈 Go HIGHER!"),
        ],
    )
    def test_check_guess(self, guess, secret, expected_outcome, expected_message):
        outcome, message = check_guess(guess, secret)
        assert outcome == expected_outcome
        assert message == expected_message


class TestParseGuess:
    """Tests for parse_guess function."""

    @pytest.mark.parametrize(
        "raw_input,expected_ok,expected_value,expected_error",
        [
            ("42", True, 42, None),
            ("42.7", True, 42, None),
            ("-5", True, -5, None),
            ("0", True, 0, None),
            ("", False, None, "Enter a guess."),
            (None, False, None, "Enter a guess."),
            ("not a number", False, None, "That is not a number."),
            ("abc123", False, None, "That is not a number."),
        ],
    )
    def test_parse_guess(self, raw_input, expected_ok, expected_value, expected_error):
        ok, value, error = parse_guess(raw_input)
        assert ok is expected_ok
        assert value == expected_value
        assert error == expected_error


class TestUpdateScore:
    """Tests for update_score function."""

    @pytest.mark.parametrize(
        "current_score,outcome,attempt_number,expected_score",
        [
            (0, "Win", 1, 80),
            (0, "Win", 5, 40),
            (0, "Win", 11, 10),  # min score is 10
            (100, "Too High", 2, 105),  # even attempt
            (100, "Too High", 3, 95),  # odd attempt
            (100, "Too Low", 2, 95),
            (100, "Unknown", 5, 100),  # unknown outcome
        ],
    )
    def test_update_score(self, current_score, outcome, attempt_number, expected_score):
        score = update_score(current_score, outcome, attempt_number)
        assert score == expected_score


class TestGetRangeForDifficulty:
    """Tests for get_range_for_difficulty function."""

    @pytest.mark.parametrize(
        "difficulty,expected_low,expected_high",
        [
            ("Easy", 1, 20),
            ("Normal", 1, 100),
            ("Hard", 1, 50),
            ("Unknown", 1, 100),  # default
        ],
    )
    def test_get_range_for_difficulty(self, difficulty, expected_low, expected_high):
        low, high = get_range_for_difficulty(difficulty)
        assert low == expected_low
        assert high == expected_high
