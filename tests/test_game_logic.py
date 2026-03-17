from logic_utils import check_guess, get_range_for_difficulty, parse_guess, get_attempt_limit, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result[0] == "Win" # we want to make sure that the result is correct so it will result[0] from (Win, Correct) tupple

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result[0] == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result[0] == "Too Low"

def test_too_high_hint():
    result = check_guess(60, 50)
    assert result[1] == "📉 Go LOWER!"

def test_too_low_hint():
    result = check_guess(40, 50)
    assert result[1] == "📈 Go HIGHER!"

def test_get_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20 

def test_get_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50

def test_get_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100

def test_parse_guess_int():
    ok, value, err = parse_guess("50")
    assert isinstance(value, int)

def test_parse_guess_invalid():
    ok, value, err = parse_guess("abc")
    assert ok == False
    assert value is None

def test_parse_guess_empty():
    ok, value, err = parse_guess("")
    assert ok == False

def test_parse_guess_decimal():
    ok, value, err = parse_guess("3.7")
    assert value == 3
    assert isinstance(value, int)
    
def test_get_easy_attempt_limit():
    assert get_attempt_limit("Easy") == 6

def test_get_normal_attempt_limit():
    assert get_attempt_limit("Normal") == 8

def test_get_hard_attempt_limit():
    assert get_attempt_limit("Hard") == 5

def test_update_score_win():
    result = update_score(0, "Win", 1)
    assert result > 0

def test_update_score_too_low():
    result = update_score(10, "Too Low", 1)
    assert result > 0

def test_update_score_too_high_odd():
    result = update_score(10, "Too High", 1)
    assert result == 5

def test_update_score_too_high_even():
    result = update_score(10, "Too High", 2)
    assert result == 15