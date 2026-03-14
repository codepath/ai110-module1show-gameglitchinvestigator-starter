import random
import streamlit as st
import time                   # if you still have the 10‑second delay

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    # secret may be an int or a numeric string (glitch), normalise it
    try:
        secret_val = int(secret)
    except (TypeError, ValueError):
        # leave it alone if it isn’t a number
        secret_val = secret

    # direct equality check
    if guess == secret_val:
        return "Win", "🎉 Correct!"

    try:
        # numeric comparison
        if guess > secret_val:
            # guess is too high, tell the player to go lower
            return "Too High", "📉 Go LOWER!"
        else:
            # guess is too low, tell them to go higher
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        # fall back to string comparison if types still mismatch
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 11,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

# placeholder for the hint message; re‑using this will “refresh” it
hint_slot = st.empty()

# build a little form so that Enter will submit the guess
with st.form("guess_form"):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )
    show_hint = st.checkbox("Show hint", value=True)
    submit = st.form_submit_button("Submit Guess 🚀")

# “new game” stays outside the form
new_game = st.button("New Game 🔁")

if new_game:
    # re‑initialise everything the way it was at startup
    st.session_state.attempts = 1             # first attempt
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    hint_slot.empty()            # clear any leftover hint
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    # clear whatever was there previously
    hint_slot.empty()

    ok, guess_int, err = parse_guess(raw_guess)
    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            # cycle through several “colours” based on attempt count
            hint_funcs = [
                hint_slot.warning,  # yellow
                hint_slot.info,     # blue
                hint_slot.success,  # green
                hint_slot.error,    # red
            ]
            func = hint_funcs[(st.session_state.attempts - 1) % len(hint_funcs)]
            func(message)

            # optional: make the hint disappear after ten seconds
            time.sleep(10)
            hint_slot.empty()
        else:
            hint_slot.empty()

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
