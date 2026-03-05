from logic_utils import check_guess, parse_guess, validate_range, get_range_for_difficulty, update_score


# --- check_guess tests ---

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


def test_high_guess_says_go_lower():
    outcome, message = check_guess(75, 50)
    assert "LOWER" in message


def test_low_guess_says_go_higher():
    outcome, message = check_guess(25, 50)
    assert "HIGHER" in message


# --- parse_guess tests ---

def test_parse_valid_number():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False


def test_parse_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert "not a number" in err


# --- validate_range tests ---

def test_validate_in_range():
    ok, err = validate_range(50, 1, 100)
    assert ok is True


def test_validate_out_of_range():
    ok, err = validate_range(150, 1, 100)
    assert ok is False


def test_validate_negative():
    ok, err = validate_range(-5, 1, 100)
    assert ok is False


# --- get_range_for_difficulty tests ---

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50


def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


# --- update_score tests ---

def test_score_on_win():
    score = update_score(0, "Win", 1)
    assert score > 0


def test_score_penalty_on_wrong():
    score = update_score(50, "Too High", 1)
    assert score < 50
