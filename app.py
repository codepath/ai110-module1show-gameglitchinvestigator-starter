import random
import streamlit as st


def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
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
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High" or outcome == "Too Low":
        return current_score - 5

    return current_score


def heat_label(guess: int, secret: int, low: int, high: int) -> str:
    distance = abs(guess - secret)
    range_size = high - low
    if distance == 0:
        return "🎯 Exact!"
    if distance <= range_size * 0.10:
        return "🔥 Hot"
    if distance <= range_size * 0.25:
        return "🌡️ Warm"
    return "🧊 Cold"


def check_new_record(highscores: dict, difficulty: str, score: int) -> bool:
    """Returns True if score beats the current best for difficulty."""
    return score > highscores.get(difficulty, 0)


# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(page_title="Number Guesser", page_icon="🎮")
st.title("🎮 Number Guesser")


# ── Sidebar: Settings ─────────────────────────────────────────────────────────

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 8,
    "Normal": 6,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# ── Sidebar: High Scores ──────────────────────────────────────────────────────

st.sidebar.divider()
st.sidebar.subheader("🏆 High Scores")
for diff in ["Easy", "Normal", "Hard"]:
    best = st.session_state.highscores.get(diff, 0) if "highscores" in st.session_state else 0
    st.sidebar.caption(f"{diff}: **{best} pts**")

# ── Session state ─────────────────────────────────────────────────────────────

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []  # list of {"guess": int, "outcome": str, "heat": str}

if "highscores" not in st.session_state:
    st.session_state.highscores = {}  # {"Easy": int, "Normal": int, "Hard": int}

if "last_hint" not in st.session_state:
    st.session_state.last_hint = None  # {"message": str, "outcome": str, "heat": str}

# ── Sidebar: Guess History ────────────────────────────────────────────────────

if st.session_state.history:
    st.sidebar.divider()
    st.sidebar.subheader("📋 Guess History")
    for entry in st.session_state.history:
        guess = entry["guess"]
        outcome = entry["outcome"]
        heat = entry["heat"]
        direction = "✅" if outcome == "Win" else ("⬆️" if outcome == "Too Low" else "⬇️")
        progress = int(min(max((guess - low) / (high - low), 0.0), 1.0) * 100)
        color = "#ef4444" if heat == "🔥 Hot" else "#f97316" if heat == "🌡️ Warm" else "#3b82f6"
        st.sidebar.caption(f"{direction} **{guess}** — {heat}")
        st.sidebar.markdown(
            f'<div style="background:#e5e7eb;border-radius:4px;height:8px;margin-bottom:6px">'
            f'<div style="width:{progress}%;background:{color};height:8px;border-radius:4px"></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

# ── Main: game info ───────────────────────────────────────────────────────────

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)


raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)
with col4:
    give_up = st.button("Give Up 🏳️")

if give_up and st.session_state.status == "playing":
    st.session_state.status = "gave_up"
    st.rerun()

if show_hint and st.session_state.last_hint:
    h = st.session_state.last_hint
    if h["outcome"] == "Win":
        st.success(h["message"])
    elif h["heat"] == "🔥 Hot":
        st.warning(f"{h['message']}  —  {h['heat']}")
    elif h["heat"] == "🌡️ Warm":
        st.info(f"{h['message']}  —  {h['heat']}")
    else:
        st.error(f"{h['message']}  —  {h['heat']}")

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.last_hint = None
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    elif st.session_state.status == "gave_up":
        st.warning(f"You gave up. The secret was **{st.session_state.secret}**. Start a new game to try again.")
    else:
        st.error("Game over. Start a new game to try again.")

    # ── Session summary table ─────────────────────────────────────────────────
    if st.session_state.history:
        st.subheader("📊 Session Summary")
        rows = []
        for i, entry in enumerate(st.session_state.history, start=1):
            rows.append({
                "Attempt": i,
                "Guess": entry["guess"],
                "Distance": abs(entry["guess"] - st.session_state.secret),
                "Heat": entry["heat"],
                "Result": entry["outcome"],
            })
        st.table(rows)

    st.stop()

# ── Submit logic ──────────────────────────────────────────────────────────────

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    else:
        outcome, message = check_guess(guess_int, st.session_state.secret)
        heat = heat_label(guess_int, st.session_state.secret, low, high)

        st.session_state.history.append({
            "guess": guess_int,
            "outcome": outcome,
            "heat": heat,
        })

        st.session_state.last_hint = {"message": message, "outcome": outcome, "heat": heat}

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            is_new_record = check_new_record(st.session_state.highscores, difficulty, st.session_state.score)
            if is_new_record:
                st.session_state.highscores[difficulty] = st.session_state.score
            st.balloons()
            st.session_state.status = "won"
            if is_new_record:
                st.success(
                    f"🏆 New high score for {difficulty}! "
                    f"The secret was {st.session_state.secret}. "
                    f"Final score: {st.session_state.score}"
                )
            else:
                st.success(
                    f"You won! The secret was {st.session_state.secret}. "
                    f"Final score: {st.session_state.score}"
                )
            st.rerun()
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
            st.rerun()

st.divider()
