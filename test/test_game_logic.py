from logic_utils import update_score


def test_correct_guess_never_leaves_a_negative_final_score():
    """A run of wrong guesses must not make the winning score negative."""
    score = 0
    for attempt in range(1, 99):
        score = update_score(score, "Too Low", attempt)

    final_score = update_score(score, "Win", attempt_number=5)

    assert final_score >= 0
    assert final_score == 10
