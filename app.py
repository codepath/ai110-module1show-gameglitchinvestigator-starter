import random
import json
from pathlib import Path
from datetime import date
import streamlit as st
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    get_hot_cold,
)

# Feature: High Score tracker Start
HIGHSCORES_FILE = Path(__file__).parent / "highscores.json"


def load_highscores():
    if HIGHSCORES_FILE.exists():
        with open(HIGHSCORES_FILE, "r") as f:
            return json.load(f)
    return []


def save_highscore(score, difficulty, attempts):
    scores = load_highscores()
    scores.append({
        "score": score,
        "difficulty": difficulty,
        "attempts": attempts,
        "date": str(date.today()),
    })
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:5]
    with open(HIGHSCORES_FILE, "w") as f:
        json.dump(scores, f, indent=2)
# Feature: High Score tracker End


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

# Defect 4 Fix Start: Two problems corrected here.
# (1) Attempt counts were inverted: Easy=6, Normal=8, Hard=5 made Normal
#     easier than Easy. Confirmed the expected ordering with AI and corrected.
# (2) get_range_for_difficulty returned 1–20 for Easy and 1–50 for Hard, so
#     the secret number and range validation were tighter on those tiers while
#     still showed "1 to 100". This caused a mismatch where a secret above 20
#     could be generated on Easy but the player could not guess above 20.
#     Removed per-difficulty ranges; all tiers now share 1–100 uniformly.
#     Difficulty is expressed solely through attempt count.
attempt_limit_map = {
    "Easy": 10,
    "Normal": 8,
    "Hard": 4,
}
# Defect 4 Fix End: Easy=10, Normal=8, Hard=4 over a uniform 1–100 range.
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Feature: Guess History sidebar chart Start
if st.session_state.get("history"):
    import pandas as pd
    history = st.session_state.history
    secret = st.session_state.secret
    chart_data = pd.DataFrame({
        "Your Guess": history,
        "Secret": [secret] * len(history),
    })
    st.sidebar.line_chart(chart_data)
# Feature: Guess History sidebar chart End

# Feature: High Score tracker Start
_hs_list = load_highscores()
if _hs_list:
    st.sidebar.subheader("High Scores")
    for _hs in _hs_list:
        st.sidebar.caption(
            f"{_hs['date']} | {_hs['difficulty']} | "
            f"Attempts: {_hs['attempts']} | Score: {_hs['score']}"
        )
# Feature: High Score tracker End

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# Defect 3 Fix Start: attempts was initialized to 1, so the counter started at
# N-1 before any guess was made, and the display lagged one run behind because
# st.info() renders before the submit block increments the value.
# We traced both causes by reading session_state in the debug panel and asking
# AI to walk through Streamlit's top-to-bottom execution model. AI showed that
# on the run triggered by a button click, the counter line executes before the
# increment line — so the display always reflects the previous run's value.
# Fix: initialize to 0 and use st.empty() placeholder filled after the submit
# block so the counter always reflects the post-increment value.
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
# Defect 3 Fix End: attempts starts at 0; counter_placeholder below is filled
# after the submit block so it always reflects the post-increment value.

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

counter_placeholder = st.empty()


# Defect 6 Fix Start: st.text_input + st.button do not share a form, so
# pressing Enter in the input field did nothing — the player had to click
# the button manually. We confirmed this by reading Streamlit docs and asking
# AI which widget enables Enter-to-submit; AI pointed to st.form +
# st.form_submit_button as the correct pattern. Wrapping the input and submit
# button inside st.form ties Enter key presses to form submission
# automatically.
with st.form("guess_form"):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )
    submit = st.form_submit_button("Submit Guess 🚀")
# Defect 6 Fix End

col1, col2 = st.columns(2)
with col1:
    new_game = st.button("New Game 🔁")
with col2:
    show_hint = st.checkbox("Show hint", value=True)

# Defect 2 Fix Start: The New Game button reset attempts and secret but forgot
# to clear status and score. Because the st.stop() guard checks status
# immediately on rerun, the game stayed stuck in "won"/"lost" and was
# unplayable after the first round. We traced the freeze to the missing resets
# by reading the session_state in the debug panel, then asked AI to review the
# new_game block. AI identified the two missing lines; we verified by winning a
# game and confirming a fresh round started correctly after clicking New Game.
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(1, 100)
    st.session_state.status = "playing"
    st.session_state.score = 0
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()
# Defect 2 Fix End

# Feature: Session Summary Table Start


def render_session_summary():
    """Render a table summarizing every guess made in the current game."""
    import pandas as pd
    history = st.session_state.get("history", [])
    secret = st.session_state.get("secret")
    if not history or secret is None:
        return
    rows = []
    for i, g in enumerate(history, start=1):
        outcome, _ = check_guess(g, secret)
        if outcome == "Win":
            direction = "✅ Win"
        elif outcome == "Too High":
            direction = "↓ Too High"
        else:
            direction = "↑ Too Low"
        rows.append({
            "Attempt": i,
            "Guess": g,
            "Direction": direction,
            "Distance": abs(g - secret),
        })
    st.subheader("📋 Session Summary")
    st.dataframe(
        pd.DataFrame(rows), use_container_width=True, hide_index=True
    )
# Feature: Session Summary Table End


if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    render_session_summary()
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    # Defect 7 Fix Start: parse_guess only checked that the input was a valid
    # number; it never checked whether the value fell within the game's range.
    # Numbers like -5 or 500 were accepted and processed as normal guesses.
    # We spotted this by typing 0 and 999 and watching them sail through.
    # AI confirmed that parse_guess has no knowledge of the range and suggested
    # adding the bounds check here in app.py right after parsing, since
    # low/high
    # are already in scope and parse_guess stays a general-purpose utility.
    # Follow-up: attempts increment moved inside the valid-guess branch below
    # so that invalid input (bad format or out-of-range) is treated as a free
    # re-entry and does not cost the player an attempt. Discussed with AI —
    # penalizing a typo is poor UX, especially on Hard with only 4 attempts.
    if ok and not (low <= guess_int <= high):
        ok = False
        err = f"Please enter a number between {low} and {high}."
    # Defect 7 Fix End

    if not ok:
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # Defect 1 - Issue 2 Fix Start: The original code cast secret to str
        # on even attempts and kept it as int on odd ones
        # (attempt_number % 2 == 0). In Python 3, comparing int > str raises
        # TypeError, so check_guess fell into its except block and did string
        # comparison — making hints flip randomly for the same guess. We
        # spotted the toggle by re-submitting the same number twice and
        # watching the hint change. AI explained why int/str comparison is
        # undefined in Python 3; the fix is to always pass the raw int
        # directly from session_state without any type conversion.
        secret = st.session_state.secret
        # Defect 1 - Issue 2 Fix End

        outcome, message = check_guess(guess_int, secret)

        # Feature: Color-coded Hot/Cold hints Start
        if show_hint and outcome != "Win":
            hc_label, hc_text = get_hot_cold(guess_int, secret)
            combined = f"{message} — {hc_text}"
            if hc_label in ("blazing", "hot"):
                st.error(combined)
            elif hc_label == "warm":
                st.warning(combined)
            else:
                st.info(combined)
        # Feature: Color-coded Hot/Cold hints End

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            # Feature: High Score tracker Start
            save_highscore(
                st.session_state.score,
                difficulty,
                st.session_state.attempts,
            )
            # Feature: High Score tracker End
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
            render_session_summary()
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
                render_session_summary()

counter_placeholder.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

# Defect 8 Fix Start: the debug expander was placed above the submit block, so
# it rendered with stale session_state values from the start of the current
# run.
# History, attempts, and score were all one step behind after every submission.
# We caught this by submitting a guess and comparing the debug panel to the
# actual game state. AI explained Streamlit's top-to-bottom render order and
# suggested moving the expander to after all state mutations so it always
# reflects the final values for the current run.
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)
# Defect 8 Fix End

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
