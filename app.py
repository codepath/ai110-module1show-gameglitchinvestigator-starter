from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

import altair as alt
import pandas as pd
import streamlit as st

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

HIGH_SCORE_PATH = Path(__file__).with_name("high_score.json")


def load_high_score() -> dict[str, Any]:
    if not HIGH_SCORE_PATH.exists():
        return {"score": 0, "difficulty": None, "attempts": None, "updated_at": None}
    try:
        data = json.loads(HIGH_SCORE_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("high_score.json is not a dict")
        return {
            "score": int(data.get("score", 0)),
            "difficulty": data.get("difficulty"),
            "attempts": data.get("attempts"),
            "updated_at": data.get("updated_at"),
        }
    except Exception:
        return {"score": 0, "difficulty": None, "attempts": None, "updated_at": None}


def save_high_score(record: dict[str, Any]) -> None:
    try:
        HIGH_SCORE_PATH.write_text(json.dumps(record, indent=2), encoding="utf-8")
    except Exception:
        pass


def get_hint_message(outcome: str) -> str:
    if outcome == "Win":
        return "🎉 Correct!"
    if outcome == "Too High":
        return "📉 Too high — go LOWER!"
    if outcome == "Too Low":
        return "📈 Too low — go HIGHER!"
    return "Try again."


def hot_cold_label(distance: int) -> str:
    if distance == 0:
        return "Perfect ✅"
    if distance <= 5:
        return "Hot 🔥"
    if distance <= 12:
        return "Warm 🙂"
    return "Cold 🧊"


def reset_game(low: int, high: int) -> None:
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.guesses = []


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮", layout="centered")

st.title("🎮 Game Glitch Investigator")
st.caption("A guessing game that started out glitchy — your job is to fix it responsibly.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Normal", "Hard"], index=1)
attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)
st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "high_score" not in st.session_state:
    st.session_state.high_score = load_high_score()

high_score = st.session_state.high_score
st.sidebar.subheader("High Score")
st.sidebar.metric("Best score", int(high_score.get("score", 0)))
if high_score.get("updated_at"):
    st.sidebar.caption(f"Last updated: {high_score['updated_at']}")

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if st.session_state.difficulty != difficulty:
    # FIXME: Streamlit reruns on every interaction; difficulty changes should reset game state.
    st.session_state.difficulty = difficulty
    reset_game(low, high)

if "secret" not in st.session_state:
    reset_game(low, high)

st.subheader("Make a guess")

attempts_left = max(attempt_limit - int(st.session_state.attempts), 0)
col_a, col_b = st.columns(2)
with col_a:
    st.metric("Score", int(st.session_state.score))
with col_b:
    st.metric("Attempts left", attempts_left)

st.info(f"Guess a number between {low} and {high}.")

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("Guesses:", st.session_state.guesses)

raw_guess = st.text_input("Enter your guess:", key=f"guess_input_{difficulty}")

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIX: Reset state cleanly and keep difficulty/range consistent (done with AI help, then verified in app).
    reset_game(low, high)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)
    if not ok:
        st.error(err)
    elif guess_int is None:
        st.error("Enter a guess.")
    elif guess_int < low or guess_int > high:
        st.error(f"Out of range. Enter a number from {low} to {high}.")
    else:
        st.session_state.attempts += 1
        st.session_state.guesses.append(int(guess_int))

        # FIX: Stable comparison logic in `logic_utils.check_guess` (no type-flipping secret).
        outcome = check_guess(int(guess_int), int(st.session_state.secret))
        hint = get_hint_message(outcome)

        distance = abs(int(guess_int) - int(st.session_state.secret))
        temp = hot_cold_label(distance)

        if show_hint:
            if outcome == "Win":
                st.success(f"{hint} ({temp})")
            else:
                st.warning(f"{hint} ({temp})")

        st.session_state.score = update_score(
            current_score=int(st.session_state.score),
            outcome=outcome,
            attempt_number=int(st.session_state.attempts),
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"

            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )

            # FIX: Feature expansion — persistent high score saved to disk.
            if int(st.session_state.score) > int(high_score.get("score", 0)):
                high_score.update(
                    {
                        "score": int(st.session_state.score),
                        "difficulty": difficulty,
                        "attempts": int(st.session_state.attempts),
                        "updated_at": pd.Timestamp.utcnow().isoformat(timespec="seconds")
                        + "Z",
                    }
                )
                save_high_score(high_score)
                st.sidebar.success("New high score saved!")

        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts! The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )

st.divider()

# Challenge 4: Enhanced UI — show a clean session summary
st.subheader("Session Summary")

if st.session_state.guesses:
    df = pd.DataFrame(
        {
            "Attempt": list(range(1, len(st.session_state.guesses) + 1)),
            "Guess": st.session_state.guesses,
        }
    )
    df["Distance"] = (df["Guess"] - int(st.session_state.secret)).abs()
    df["Hot/Cold"] = df["Distance"].apply(lambda d: hot_cold_label(int(d)))
    df["Result"] = df["Guess"].apply(lambda g: check_guess(int(g), int(st.session_state.secret)))
    st.dataframe(df, hide_index=True, use_container_width=True)

    st.sidebar.subheader("Guess History")
    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Attempt:Q", title="Attempt"),
            y=alt.Y("Guess:Q", title="Guess"),
            tooltip=["Attempt", "Guess", "Distance", "Hot/Cold", "Result"],
        )
        .properties(height=180)
    )
    st.sidebar.altair_chart(chart, use_container_width=True)
else:
    st.caption("No guesses yet. Submit a guess to see your session summary.")

st.caption("Built by an AI… and then debugged by a human.")
