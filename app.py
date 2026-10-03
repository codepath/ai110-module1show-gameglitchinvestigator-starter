import random
import streamlit as st

from logic_utils import (
    check_guess,
    get_proximity_label,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

# FIX: moved hint text out of logic_utils so check_guess can return a plain outcome (agent mode)
HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}

# Challenge 4: Enhanced UI — color-coded hint text (Streamlit markdown color syntax).
HINT_COLORS = {
    "Win": "green",
    "Too High": "orange",
    "Too Low": "blue",
}

# Challenge 4: Enhanced UI — icons shown next to each past guess in the history list.
HISTORY_ICONS = {
    "Win": "✅",
    "Too High": "⬆️",
    "Too Low": "⬇️",
    "Invalid": "⚠️",
}

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
    # FIX: was 1, causing off-by-one attempts-left display and parity bugs (Copilot agent mode)
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

attempts_left = max(attempt_limit - st.session_state.attempts, 0)

# Challenge 4: Enhanced UI — at-a-glance metrics and a progress bar instead of plain text.
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Score", st.session_state.score)
metric_col2.metric("Attempts Left", attempts_left)
metric_col3.metric("Difficulty", difficulty)

st.progress(min(st.session_state.attempts / attempt_limit, 1.0))

st.info(f"Guess a number between {low} and {high}.")

with st.expander("Developer Debug Info"):
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

with st.form(key="guess_form", clear_on_submit=False):
    # FIX: st.form avoids the on_click callback's click-race (agent mode)
    raw_guess = st.text_input("Enter your guess:")
    show_hint = st.checkbox("Show hint", value=True)
    submit = st.form_submit_button("Submit Guess 🚀")

new_game = st.button("New Game 🔁")

# Challenge 4: Enhanced UI — structured session summary table instead of a raw list.
if st.session_state.history:
    st.subheader("📋 Session Summary")
    summary_rows = []
    for i, entry in enumerate(st.session_state.history, start=1):
        icon = HISTORY_ICONS.get(entry["outcome"], "❓")
        summary_rows.append(
            {
                "Attempt": i,
                "Guess": entry["guess"],
                "Outcome": f"{icon} {entry['outcome']}",
                "Proximity": entry.get("proximity", "—"),
                "Score": entry.get("score_after", "—"),
            }
        )
    st.table(summary_rows)

# Challenge 4: Enhanced UI — sidebar visualization of guess closeness to the secret.
st.sidebar.divider()
st.sidebar.header("📊 Guess History")
range_size = max(high - low, 1)
valid_guesses = [
    entry for entry in st.session_state.history if entry["outcome"] != "Invalid"
]
if valid_guesses:
    for entry in reversed(valid_guesses):
        distance = abs(entry["guess"] - st.session_state.secret)
        closeness = max(0.0, 1 - (distance / range_size))
        icon = HISTORY_ICONS.get(entry["outcome"], "❓")
        proximity = entry.get("proximity", "")
        st.sidebar.caption(f"{icon} Guess {entry['guess']} — {proximity}")
        st.sidebar.progress(closeness)
else:
    st.sidebar.caption("No guesses yet.")

if new_game:
    st.session_state.attempts = 0
    # FIX: use difficulty-based low/high instead of hardcoded randint(1, 100) (Copilot agent mode)
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    # FIX: reveal the secret on the game-over screen, not just the one-time message (agent mode)
    if st.session_state.status == "won":
        st.success(
            f"You already won. The secret was {st.session_state.secret}. "
            f"Start a new game to play again."
        )
    else:
        st.error(
            f"Game over. The secret was {st.session_state.secret}. "
            f"Start a new game to try again."
        )
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(
            {
                "guess": raw_guess,
                "outcome": "Invalid",
                "proximity": "—",
                "score_after": st.session_state.score,
            }
        )
        st.error(err)
    else:
        assert guess_int is not None  # ok is True here, so parse_guess returned an int
        outcome = check_guess(guess_int, st.session_state.secret)
        proximity = get_proximity_label(guess_int, st.session_state.secret, low, high)
        st.session_state.history.append(
            {"guess": guess_int, "outcome": outcome, "proximity": proximity}
        )

        if show_hint:
            # Challenge 4: Enhanced UI — color-coded hint plus a Hot/Cold proximity emoji.
            color = HINT_COLORS.get(outcome, "gray")
            st.markdown(f":{color}[**{HINT_MESSAGES[outcome]}**]")
            st.caption(f"Proximity: {proximity}")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )
        st.session_state.history[-1]["score_after"] = st.session_state.score

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
