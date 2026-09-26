import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    hint_message,
    parse_guess,
    update_score,
)


# --- Starter tests (unchanged) ------------------------------------------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Bug 1: the hint text contradicted the outcome ----------------------

def test_too_high_hint_tells_player_to_go_lower():
    """The starter paired "Too High" with "Go HIGHER!", walking the player
    away from the answer on every turn."""
    assert "LOWER" in hint_message("Too High")


def test_too_low_hint_tells_player_to_go_higher():
    assert "HIGHER" in hint_message("Too Low")


# --- Bug 2: secret was coerced to str on even attempts ------------------

def test_string_secret_is_not_compared_as_text():
    """The starter compared int vs str, hit TypeError, and fell back to
    alphabetical comparison where "9" > "100". A guess of 9 against a secret
    of 100 was reported as "Too High"."""
    assert check_guess(9, "100") == "Too Low"


def test_string_secret_still_detects_a_win():
    assert check_guess(50, "50") == "Win"


# --- Bug 3: score moved differently depending on turn parity ------------

def test_wrong_guess_costs_the_same_on_odd_and_even_attempts():
    """The starter gave +5 for "Too High" on even attempts and -5 on odd."""
    assert update_score(50, "Too High", 2) == update_score(50, "Too High", 3)


def test_wrong_guess_loses_points():
    assert update_score(50, "Too Low", 1) == 45


def test_score_never_goes_negative():
    assert update_score(0, "Too Low", 1) == 0


def test_winning_sooner_scores_higher():
    assert update_score(0, "Win", 1) > update_score(0, "Win", 4)


# --- Bug 4: out-of-range and decimal guesses were accepted --------------

def test_guess_outside_range_is_rejected():
    ok, value, err = parse_guess("999", 1, 20)
    assert ok is False
    assert value is None
    assert "between 1 and 20" in err


def test_guess_inside_range_is_accepted():
    ok, value, err = parse_guess("15", 1, 20)
    assert (ok, value, err) == (True, 15, None)


def test_decimal_guess_is_rejected_not_silently_truncated():
    """The starter turned "50.9" into 50 without telling the player."""
    ok, value, err = parse_guess("50.9", 1, 100)
    assert ok is False


def test_empty_guess_is_rejected():
    ok, value, err = parse_guess("", 1, 100)
    assert ok is False


# --- Bug 5: "Hard" was easier than "Normal" -----------------------------

def test_hard_range_is_wider_than_normal():
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")
    assert (hard_high - hard_low) > (normal_high - normal_low)


def test_unknown_difficulty_falls_back_to_normal():
    assert get_range_for_difficulty("Nightmare") == get_range_for_difficulty("Normal")
