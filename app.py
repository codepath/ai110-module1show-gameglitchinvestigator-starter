import random
import streamlit as st
# FIX #8: Import refactored functions from logic_utils.py
# User-AI collaboration: User pointed to comments requesting code refactoring.
# AI moved helper functions to logic_utils.py and imported them here.
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    get_random_attempt_limit,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

# NEW FEATURE: Added Extra Hard difficulty option
# User-AI collaboration: User requested new "Extra Hard" mode (1-1000, 5 attempts).
# AI added it to the difficulty selector with appropriate index.
difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard", "Extra Hard"],
    index=1,
)

low, high = get_range_for_difficulty(difficulty)

# Initialize session state
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "attempt_limit" not in st.session_state:
    st.session_state.attempt_limit = get_random_attempt_limit(difficulty)

# NEW FEATURE: High score and low score tracking
# User-AI collaboration: User requested tracking of highest and lowest scores
# achieved across all games. AI added session state variables to persist these
# values and update them after each game completes.
if "high_score" not in st.session_state:
    st.session_state.high_score = 0

if "low_score" not in st.session_state:
    st.session_state.low_score = 0

# FIX #2: Store randomized attempt limit in session state
# User-AI collaboration: User requested randomized attempts. AI implemented
# session state storage so the random limit persists throughout the game
# and updates when difficulty changes.
if "last_difficulty" not in st.session_state:
    st.session_state.last_difficulty = difficulty

if st.session_state.last_difficulty != difficulty:
    st.session_state.attempt_limit = get_random_attempt_limit(difficulty)
    st.session_state.last_difficulty = difficulty

attempt_limit = st.session_state.attempt_limit

st.sidebar.caption(f"Range: {low} to {high}")
# FIX #5: Display consistent attempt limit from session state
# User-AI collaboration: User noted attempts counter in sidebar didn't match
# the one in main area. AI fixed by using session state value consistently.
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

st.subheader("Make a guess")

# FIX #5: Calculate remaining attempts correctly
# User-AI collaboration: User reported attempts counter inconsistency.
# AI fixed by properly calculating remaining attempts using session state.
attempts_remaining = attempt_limit - st.session_state.attempts
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempts_remaining}"
)

with st.expander("Developer Debug Info"):
    # FIX #3 (reversed): Initially removed secret per user request to hide it,
    # then user requested to bring it back for debugging purposes.
    # FIX #4: Removed history display as it revealed guessed numbers.
    # User-AI collaboration: User noted debug info was showing secret (allowing
    # cheating) and history (revealing past guesses). AI initially removed both,
    # then added secret back per user's request while keeping history hidden.
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("Status:", st.session_state.status)

    # NEW FEATURE: Display high score and low score trackers
    # User-AI collaboration: User requested high/low score tracking visible
    # in debug section. AI added display of both scores to help track
    # performance across multiple games.
    st.write("---")
    st.write("🏆 High Score:", st.session_state.high_score)
    st.write("📉 Low Score:", st.session_state.low_score)

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

if new_game:
    # FIX #1: Properly reset all game state when starting new game
    # User-AI collaboration: User reported new game button didn't work properly.
    # Original code only reset attempts to 0 (wrong value) and secret. AI fixed
    # to reset all session state: attempts (to 0), status, history, score, and
    # generate new secret and randomized attempt limit.
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.attempt_limit = get_random_attempt_limit(difficulty)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    # FIX #12: Display win/loss messages after page rerun
    # User-AI collaboration: User noted score wasn't updating properly in debug
    # info when winning. AI added st.rerun() after win/loss to refresh page,
    # then moved win/loss messages here to display after rerun with updated score.

    # NEW FEATURE: Update high score and low score trackers
    # User-AI collaboration: User requested tracking of highest and lowest scores.
    # AI added logic to check and update high/low scores whenever a game ends,
    # ensuring trackers always reflect best and worst performances.
    current_score = st.session_state.score

    # Update high score if current score is higher
    if current_score > st.session_state.high_score:
        st.session_state.high_score = current_score

    # Update low score (initialize on first game or if lower than current lowest)
    if st.session_state.low_score == 0 or current_score < st.session_state.low_score:
        st.session_state.low_score = current_score

    if st.session_state.status == "won":
        st.balloons()
        st.success(
            f"You won! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}"
        )
        # Show if this is a new high score
        if current_score == st.session_state.high_score:
            st.success("🏆 NEW HIGH SCORE! 🏆")
        st.info("Start a new game to play again.")
    else:
        st.error(
            f"Game over! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}"
        )
        st.info("Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIX #10: Removed string conversion bug on even attempts
        # User-AI collaboration: AI discovered that original code converted secret
        # to string on even attempts (causing incorrect comparisons). AI removed
        # this buggy logic and now always compares integers directly.
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        # FIX #12: Rerun page after win/loss to update all displays
        # User-AI collaboration: User reported score not updating properly.
        # AI added st.rerun() to refresh page and ensure debug info shows
        # updated score before displaying final win/loss message.
        if outcome == "Win":
            st.session_state.status = "won"
            st.rerun()
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
