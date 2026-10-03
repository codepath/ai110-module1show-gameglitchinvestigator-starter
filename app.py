import random

import streamlit as st

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

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
    "Easy": 6,
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
    st.session_state.attempts = 0

if "trial_used" not in st.session_state:
    st.session_state.trial_used = False

if "score" not in st.session_state:
    st.session_state.score = 50

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# FIX: I asked AI to help separate the trial hint from the real attempts. I checked the suggested flow against my rules and kept this change so the first bound-check does not change the secret or count as a real guess.
if "trial_hint" not in st.session_state:
    st.session_state.trial_hint = ""

st.subheader("Make a guess")

if not st.session_state.trial_used:
    st.info(
        "Trial attempt 0: this does not count as a real guess. "
        "Use it to set a bound and narrow the range before the real round starts."
    )
else:
    current_real_attempt = max(1, st.session_state.attempts)
    st.info(
        f"Guess a number between {low} and {high}. "
        f"Attempt {current_real_attempt} of {attempt_limit}. "
        f"Attempts left: {max(0, attempt_limit - st.session_state.attempts)}"
    )

if st.session_state.trial_hint:
    st.warning(st.session_state.trial_hint)

next_attempt_number = st.session_state.attempts
if not st.session_state.trial_used:
    st.caption(
        "The trial does not count as a real attempt. The next real guess is Attempt 1."
    )
elif next_attempt_number % 2 == 1:
    st.caption(
        "On this attempt, if you are Too Low, you can gain +4 or lose -10. "
        "If you are Too High, you lose -5."
    )
else:
    st.caption(
        "On this attempt, if you are Too Low, you lose -5. "
        "If you are Too High, you can gain +4 or lose -10."
    )

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: I asked AI to look at why a new game kept old state. After checking the suggestion, I reset the attempts, trial state, hint, secret, history, score, and status together.
if new_game:
    st.session_state.attempts = 0
    st.session_state.trial_used = False
    st.session_state.trial_hint = ""
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 50
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    # FIX: I explained to AI that the first submit needed to be a trial-only bound-check, not a normal move.
    # I reviewed the change and kept it because it keeps the secret stable and shows a hint without consuming a real attempt.
    if not st.session_state.trial_used:
        ok, guess_int, err = parse_guess(raw_guess)

        if not ok:
            st.session_state.history.append(raw_guess)
            st.error(err)
        else:
            st.session_state.trial_used = True
            st.session_state.history.append(f"Trial:{guess_int}")
            outcome = check_guess(guess_int, st.session_state.secret)

            if outcome == "Win":
                trial_message = "🎉 Trial hint: Correct! This is the exact value, but the trial still does not count as a real attempt."
            elif outcome == "Too High":
                trial_message = f"📉 Trial guess of {guess_int} was too high. The upper bound is {guess_int}."
            else:
                trial_message = f"📈 Trial guess of {guess_int} was too low. The lower bound is {guess_int}."

            # FIX: I showed AI that the trial hint disappeared after the rerun. I checked its session-state suggestion and used it to keep the bound clue visible when the real round starts.
            st.session_state.trial_hint = trial_message if show_hint else ""
            st.info(
                f"Trial attempt 0 used. Your bound check was '{outcome}'. "
                "This does not count as a real attempt, and the secret stays the same. "
                "The real round starts now."
            )
            if show_hint:
                st.warning(st.session_state.trial_hint)
            st.rerun()
    else:
        # FIX: I told AI the attempt counter was one behind, then checked the suggested state change.
        # I incremented the real attempt immediately after submit so the display matches the actual game state.
        st.session_state.attempts += 1

        ok, guess_int, err = parse_guess(raw_guess)

        if not ok:
            st.session_state.history.append(raw_guess)
            st.error(err)
        else:
            st.session_state.history.append(guess_int)

            secret = st.session_state.secret
            outcome = check_guess(guess_int, secret)

            if outcome == "Win":
                message = "🎉 Correct!"
            elif outcome == "Too High":
                message = "📉 Go LOWER!"
            else:
                message = "📈 Go HIGHER!"

            if show_hint:
                st.warning(message)

            # FIX: I asked AI to help trace why the displayed score did not match the final score.
            # I reviewed the result and applied the win bonus immediately, while regular guesses update the score once.
            if outcome == "Win":
                win_bonus = max(10, 100 - 10 * (st.session_state.attempts + 1))
                st.session_state.score = st.session_state.score + win_bonus
                st.session_state.status = "won"
                st.balloons()
                st.success(
                    f"You won! The secret was {st.session_state.secret}. "
                    f"Final score: {st.session_state.score}"
                )
            elif st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
            else:
                score_delta = 0
                if outcome == "Too High":
                    if st.session_state.attempts % 2 == 0:
                        score_delta = random.choice([4, -10])
                    else:
                        score_delta = -5
                elif outcome == "Too Low":
                    if st.session_state.attempts % 2 != 0:
                        score_delta = random.choice([4, -10])
                    else:
                        score_delta = -5

                new_score = st.session_state.score + score_delta
                st.session_state.score = new_score

                if new_score < 0:
                    st.session_state.status = "lost"
                    st.error(
                        f"You went below 0 points and lost the game. "
                        f"The secret was {st.session_state.secret}. "
                        f"Final score: {st.session_state.score}"
                    )

st.metric(label="Current score", value=st.session_state.score)
