from pathlib import Path

from streamlit.testing.v1 import AppTest

from logic_utils import check_guess

APP_PATH = str(Path(__file__).resolve().parent.parent / "app.py")

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_attempts_left_display_counts_down():
    # Normal difficulty allows 8 attempts; only valid guesses should use one up
    at = AppTest.from_file(APP_PATH, default_timeout=15).run()
    assert "Attempts left: 8" in at.info[0].value

    # Pick a guess that can't win so the game keeps going
    secret = at.session_state.secret
    wrong_guess = 1 if secret != 1 else 2

    at.text_input[0].input(str(wrong_guess))
    at.button[0].click().run()
    assert "Attempts left: 7" in at.info[0].value

    # An invalid guess should not change the count
    at.text_input[0].input("abc")
    at.button[0].click().run()
    assert "Attempts left: 7" in at.info[0].value
