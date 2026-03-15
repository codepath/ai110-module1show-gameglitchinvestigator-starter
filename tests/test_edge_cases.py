from logic_utils import check_guess, parse_guess


def test_parse_guess_rejects_empty():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert isinstance(err, str)


def test_parse_guess_rejects_whitespace():
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert isinstance(err, str)


def test_parse_guess_accepts_decimal_string():
    ok, value, err = parse_guess("3.9")
    assert ok is True
    assert value == 3
    assert err is None


def test_parse_guess_accepts_negative_int():
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None


def test_parse_guess_accepts_very_large_int():
    ok, value, err = parse_guess("999999999999999999999999")
    assert ok is True
    assert value == 999999999999999999999999
    assert err is None


def test_check_guess_handles_negative_guess():
    assert check_guess(-5, 10) == "Too Low"
