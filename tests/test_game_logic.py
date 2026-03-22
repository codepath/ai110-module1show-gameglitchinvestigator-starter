from logic_utils import check_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

def test_score_update_on_win():
    # Winning should reward 5 points
    new_score = update_score(current_score=0, outcome="Win", attempt_number=1)
    assert new_score == 5

def test_score_update_on_win_with_existing_score():
    # Winning should reward 5 points on top of existing score
    new_score = update_score(current_score=10, outcome="Win", attempt_number=2)
    assert new_score == 15

def test_score_update_on_too_high():
    # Wrong guess (too high) should penalize 1 point
    new_score = update_score(current_score=10, outcome="Too High", attempt_number=1)
    assert new_score == 9

def test_score_update_on_too_low():
    # Wrong guess (too low) should penalize 1 point
    new_score = update_score(current_score=10, outcome="Too Low", attempt_number=1)
    assert new_score == 9

def test_score_update_too_high_multiple_attempts():
    # Score should consistently penalize 1 point per wrong guess
    initial_score = 20
    score_after_first_wrong = update_score(initial_score, "Too High", 1)
    score_after_second_wrong = update_score(score_after_first_wrong, "Too Low", 2)
    assert score_after_first_wrong == 19
    assert score_after_second_wrong == 18

def test_score_can_go_negative():
    # Score should be able to go negative on multiple wrong guesses
    new_score = update_score(current_score=0, outcome="Too High", attempt_number=1)
    assert new_score == -1
