from logic_utils import parse_guess, check_guess

# ---------------------------------------------------------------------------
# parse_guess edge cases — format/type validation
# ---------------------------------------------------------------------------

def test_empty_input_rejected():
    ok, val, err = parse_guess("")
    assert ok is False
    assert val is None
    assert err is not None

def test_decimal_input_rejected():
    ok, val, err = parse_guess("3.14")
    assert ok is False
    assert val is None

def test_negative_decimal_rejected():
    ok, val, err = parse_guess("-3.5")
    assert ok is False
    assert val is None

def test_text_input_rejected():
    ok, val, err = parse_guess("abc")
    assert ok is False
    assert val is None

def test_mixed_alphanumeric_rejected():
    # "5abc" is not a valid integer
    ok, val, err = parse_guess("5abc")
    assert ok is False
    assert val is None

def test_whitespace_only_rejected():
    # A string of spaces is not a valid integer
    ok, val, err = parse_guess("   ")
    assert ok is False
    assert val is None

def test_negative_number_accepted_by_parser():
    # parse_guess only validates format; negatives are syntactically valid ints
    ok, val, err = parse_guess("-5")
    assert ok is True
    assert val == -5

def test_number_above_100_accepted_by_parser():
    # parse_guess only validates format; range is checked by check_guess
    ok, val, err = parse_guess("150")
    assert ok is True
    assert val == 150

def test_plus_prefix_accepted_by_parser():
    # Python's int() silently accepts "+50" — make sure this isn't a surprise
    ok, val, err = parse_guess("+50")
    assert ok is True
    assert val == 50

# ---------------------------------------------------------------------------
# check_guess edge cases — range validation
# ---------------------------------------------------------------------------

def test_negative_number_is_invalid():
    outcome, _ = check_guess(-1, 50)
    assert outcome == "Invalid"

def test_negative_five_is_invalid():
    outcome, _ = check_guess(-5, 50)
    assert outcome == "Invalid"

def test_number_above_100_is_invalid():
    outcome, _ = check_guess(101, 50)
    assert outcome == "Invalid"

def test_very_large_number_is_invalid():
    outcome, _ = check_guess(99999, 50)
    assert outcome == "Invalid"

def test_exactly_zero_is_not_invalid():
    # The guard is `guess < 0`, so 0 is treated as in-range (returns Too Low)
    outcome, _ = check_guess(0, 50)
    assert outcome == "Too Low"

def test_exactly_100_is_not_invalid():
    # 100 is the upper boundary and must be accepted as in-range
    outcome, _ = check_guess(100, 50)
    assert outcome == "Too High"

def test_exactly_100_wins_when_secret_is_100():
    outcome, _ = check_guess(100, 100)
    assert outcome == "Win"
