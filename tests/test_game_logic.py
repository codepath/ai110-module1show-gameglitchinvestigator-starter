from streamlit.testing.v1 import AppTest

from logic_utils import check_guess


def test_enter_key_submits_guess_via_form():
    # Regression test for the bug where pressing Enter in the guess input
    # did nothing. The fix moves the input + submit into an st.form, so the
    # submit becomes a form_submit_button (which Enter triggers natively).
    #
    # This test asserts the structural guarantee that makes Enter work:
    #   1. the guess input and a submit button live inside a form, and
    #   2. submitting that form actually processes the guess.
    at = AppTest.from_file("app.py").run()

    # Structural guarantee that makes Enter work: the guess input and its
    # submit button must live inside a single st.form. Enter only submits
    # when the control is a form_submit_button; a plain st.button (the old
    # code) ignores Enter entirely. AppTest can't press a physical Enter key,
    # so we assert the structure that wires Enter to submission instead.
    forms = at.get("form")
    assert forms, "guess input must be inside an st.form so Enter submits it"

    form = forms[0]
    child_types = {type(c).__name__ for c in form.children.values()}
    assert "TextInput" in child_types, "the guess input must be inside the form"

    submit_btn = next(
        b for b in form.children.values() if type(b).__name__ == "Button"
    )
    assert submit_btn.form_id, "submit must be a form_submit_button, not st.button"

    # Drive the form the same way pressing Enter does: set the input, submit.
    at.text_input[0].set_value("50").run()
    submit_btn.click().run()

    # The guess must have been registered: history records it and the
    # attempt counter advanced past its initial value.
    assert 50 in at.session_state["history"]
    assert at.session_state["attempts"] > 1
    assert not at.exception


def _submit_guess(at, value):
    """Type a guess into the form and submit it, then return the AppTest."""
    at.text_input[0].set_value(str(value)).run()
    at.button[0].click().run()
    return at


def _errors(at):
    return [e.value for e in at.error]


def test_out_of_bounds_high_guess_is_rejected():
    # Regression test for the bug where guesses outside the playable range
    # were accepted. On Normal the range is 1-100, so 150 must be rejected
    # with an out-of-range error and never compared to the secret.
    at = _submit_guess(AppTest.from_file("app.py").run(), 150)

    assert any("Out of range" in e for e in _errors(at))
    # The game must still be playable (no win/loss recorded from a bad guess).
    assert at.session_state["status"] == "playing"
    assert not at.exception


def test_out_of_bounds_low_guess_is_rejected():
    # Below the minimum (0 and negatives) must also be rejected on Normal.
    at = _submit_guess(AppTest.from_file("app.py").run(), 0)

    assert any("Out of range" in e for e in _errors(at))
    assert at.session_state["status"] == "playing"
    assert not at.exception


def test_boundary_values_are_accepted():
    # The range is inclusive: 1 and 100 are valid guesses on Normal and must
    # NOT raise an out-of-range error.
    for boundary in (1, 100):
        at = _submit_guess(AppTest.from_file("app.py").run(), boundary)
        assert not any("Out of range" in e for e in _errors(at))
        assert boundary in at.session_state["history"]
        assert not at.exception


def test_range_tracks_difficulty():
    # The valid range follows the selected difficulty. Easy is 1-20, so 25 is
    # in-range for Normal but out-of-range for Easy.
    at = AppTest.from_file("app.py").run()
    at.selectbox[0].set_value("Easy").run()
    _submit_guess(at, 25)

    assert any("Out of range" in e for e in _errors(at))
    assert "between 1 and 20" in " ".join(_errors(at))
    assert not at.exception


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win.
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_guess_too_high_hints_lower():
    # Guess is above the secret -> outcome "Too High", hint must say GO LOWER.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_guess_too_low_hints_higher():
    # Guess is below the secret -> outcome "Too Low", hint must say GO HIGHER.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


def test_hint_direction_is_not_reversed():
    # Regression test for the original glitch where the high/low hints
    # were swapped. A high guess must never tell the player to go higher,
    # and a low guess must never tell them to go lower.
    _, high_message = check_guess(99, 50)
    assert "HIGHER" not in high_message

    _, low_message = check_guess(1, 50)
    assert "LOWER" not in low_message


def test_string_secret_still_gives_correct_hint():
    # The app passes the secret as a string on even attempts; the hint
    # must still be correct.
    outcome, message = check_guess(60, "50")
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"
