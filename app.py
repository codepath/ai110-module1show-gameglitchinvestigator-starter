import os
import random

import streamlit as st

# FIX: all game rules now live in logic_utils.py so they can be tested with
# pytest. app.py is responsible only for UI and session state.
from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_range_for_difficulty,
    hint_message,
    parse_guess,
    update_score,
)

# FIX: the starter printed the secret into the page unconditionally, so the
# game was trivially cheatable. Debug output is now off unless explicitly
# enabled:  GLITCH_DEBUG=1 streamlit run app.py
DEBUG = os.environ.get("GLITCH_DEBUG") == "1"

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Now debugged.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

low, high = get_range_for_difficulty(difficulty)
attempt_limit = get_attempt_limit(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


def reset_game():
    """
    Start a fresh round.

    # FIX: this is the single source of truth for what "a game" is. The
    # starter defined the five state keys in five separate `if not in
    # session_state` blocks, then the New Game button re-listed only two of
    # them (secret, attempts) and left `status` untouched. Because `status`
    # gates the page with st.stop(), a finished game could never be
    # restarted. Both startup and New Game now call this one function, so
    # the two paths cannot drift apart again.
    """
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_outcome = None


# FIX: the starter picked the secret once and never re-picked it when the
# difficulty changed, so switching to Easy (1-20) could leave a secret of 87
# in place -- unguessable. Changing difficulty now starts a fresh round.
if "difficulty" not in st.session_state or st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    reset_game()

st.subheader("Make a guess")

# FIX: the range in this message was hardcoded to "1 and 100" regardless of
# difficulty, and attempts started at 1 so it was always off by one.
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

if DEBUG:
    with st.expander("Developer Debug Info"):
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)
        st.write("Difficulty:", difficulty)
        st.write("History:", st.session_state.history)

raw_guess = st.text_input("Enter your guess:", key="guess_input")

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: New Game is handled BEFORE the status guard below, and now performs a
# full reset. The starter also called st.success() immediately before
# st.rerun(), which discards everything rendered so far -- so that message
# was never actually visible.
if new_game:
    reset_game()
    st.rerun()

if submit and st.session_state.status == "playing":
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        # FIX: the starter did `attempts += 1` before validating, so typing
        # garbage burned a turn. Invalid input no longer costs an attempt.
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX: the starter replaced the secret with str(secret) on every even
        # attempt, which pushed check_guess into a text comparison and
        # inverted the hints on alternating turns. The secret is always an
        # int now.
        outcome = check_guess(guess_int, st.session_state.secret)
        st.session_state.last_outcome = outcome

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.balloons()
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"

# FIX: the hint used to render inside `if submit:`. Streamlit reruns the whole
# script on every interaction and a button is only True for the single rerun
# after its click, so toggling "Show hint" always ran with submit == False and
# the hint silently vanished. The outcome is stored in session state and the
# hint is rendered from it on every run, so the checkbox now works.
if show_hint and st.session_state.last_outcome:
    st.warning(hint_message(st.session_state.last_outcome))

if st.session_state.status == "won":
    st.success(
        f"You won! The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}"
    )
elif st.session_state.status == "lost":
    st.error(
        f"Out of attempts! "
        f"The secret was {st.session_state.secret}. "
        f"Score: {st.session_state.score}"
    )
else:
    st.caption(f"Score: {st.session_state.score}")

if st.session_state.history:
    st.caption(f"Guesses so far: {st.session_state.history}")

st.divider()
st.caption("Built by an AI that claimed this code was production-ready. It was not.")
