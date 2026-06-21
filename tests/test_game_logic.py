from logic_utils import check_guess
from streamlit.testing.v1 import AppTest


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_guess_too_high():
    # If secret is 50 and guess is 60, it is too high and hint should say lower
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_guess_too_low():
    # If secret is 50 and guess is 40, it is too low and hint should say higher
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


def test_new_game_button_restarts_every_click():
    at = AppTest.from_file("app.py")
    at.run()

    new_game_button = next(
        button for button in at.button if button.label.startswith("New Game")
    )

    baseline_game_id = at.session_state["game_id"]

    # Simulate a completed game, then verify New Game resets everything.
    at.session_state["status"] = "lost"
    at.session_state["score"] = 35
    at.session_state["history"] = [12, 77]
    at.session_state["attempts"] = 4
    new_game_button.click()
    at.run()

    assert at.session_state["status"] == "playing"
    assert at.session_state["score"] == 0
    assert at.session_state["history"] == []
    assert at.session_state["attempts"] == 0
    assert at.session_state["game_id"] == baseline_game_id + 1

    # Do it again to confirm every click restarts correctly.
    at.session_state["status"] = "won"
    at.session_state["score"] = 50
    at.session_state["history"] = [50]
    at.session_state["attempts"] = 2
    previous_game_id = at.session_state["game_id"]
    new_game_button = next(
        button for button in at.button if button.label.startswith("New Game")
    )
    new_game_button.click()
    at.run()

    assert at.session_state["status"] == "playing"
    assert at.session_state["score"] == 0
    assert at.session_state["history"] == []
    assert at.session_state["attempts"] == 0
    assert at.session_state["game_id"] == previous_game_id + 1
