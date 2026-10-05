import random

import streamlit as st

from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_hint_message,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")


def start_new_round(difficulty: str):
    """Reset every piece of game state for a fresh round."""
    low, high = get_range_for_difficulty(difficulty)
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.flash = None
    st.session_state.celebrate = False
    # The guess box is keyed on input_nonce, so bumping it gives us a brand
    # new (empty) widget instead of carrying the previous guess over.
    st.session_state.input_nonce = st.session_state.get("input_nonce", 0) + 1


st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

low, high = get_range_for_difficulty(difficulty)
attempt_limit = get_attempt_limit(difficulty)

# First run, or the player switched difficulty: the old secret may be outside
# the new range, so start a fresh round rather than leaving an unwinnable game.
if st.session_state.get("difficulty") != difficulty:
    start_new_round(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

attempts_left = max(attempt_limit - st.session_state.attempts, 0)

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempts_left}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{st.session_state.input_nonce}",
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    start_new_round(difficulty)
    st.session_state.flash = ("success", "New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.celebrate:
        st.balloons()
        st.session_state.celebrate = False

    if st.session_state.status == "won":
        st.success(
            f"You won! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}"
        )
    else:
        st.error(
            f"Out of attempts! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}"
        )
    st.caption("Press New Game 🔁 to play again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        # A typo is not a guess, so it costs neither an attempt nor points.
        st.session_state.flash = ("error", err)
    else:
        # Only a real guess burns an attempt.
        st.session_state.attempts += 1
        # Clear the box so an accidental second click cannot resubmit it.
        st.session_state.input_nonce += 1
        st.session_state.history.append((guess_int, st.session_state.secret))

        outcome = check_guess(guess_int, st.session_state.secret)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.session_state.celebrate = True
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
        else:
            st.session_state.flash = ("warning", get_hint_message(outcome))

    st.rerun()

# Rendered after a rerun so the panel above always shows up-to-date numbers.
flash = st.session_state.flash
if flash:
    level, text = flash
    if level == "warning" and not show_hint:
        pass
    else:
        getattr(st, level)(text)
    st.session_state.flash = None

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
