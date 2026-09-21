"""Streamlit UI for the number-guessing game.

This file is deliberately thin: it reads widgets, calls into `logic_utils`, and
renders the result. Every game rule lives in `logic_utils.py` so it can be
tested with pytest.

# FIX: the starter mixed the rules into the UI, so no rule could be tested
# without booting Streamlit -- and the starter test suite failed 3/3 against
# NotImplementedError stubs. Refactored with Claude Code in agent mode, then
# reviewed hunk by hunk; see reflection.md for what I kept and what I rejected.
"""

import random

import streamlit as st

from logic_utils import (
    TOO_HIGH,
    TOO_LOW,
    WIN,
    build_session_table,
    check_guess,
    format_high_scores,
    get_attempt_limit,
    get_range_for_difficulty,
    hint_message,
    parse_guess,
    proximity_label,
    proximity_trend,
    update_high_scores,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game, debugged and repaired.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

# # FIX: the range and the attempt budget used to be defined in two separate
# places in this file and could drift apart. Both now come from the single
# DIFFICULTIES table in logic_utils.py.
low, high = get_range_for_difficulty(difficulty)
attempt_limit = get_attempt_limit(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


def start_new_game(active_difficulty: str) -> None:
    """Reset every piece of game state for a fresh round.

    # FIX: the old "New Game" handler reset only `attempts` and `secret`. It
    # left `score`, `status` and `history` untouched, so after one win `status`
    # stayed "won", the next rerun hit st.stop(), and the app was permanently
    # unplayable -- clicking New Game was what kept it stuck. Resetting state
    # lives in one function now so no caller can forget a field.
    """
    game_low, game_high = get_range_for_difficulty(active_difficulty)
    # # FIX: was `random.randint(1, 100)` hardcoded, ignoring the difficulty.
    st.session_state.secret = random.randint(game_low, game_high)
    st.session_state.attempts = 0  # # FIX: was initialised to 1 (off by one).
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.difficulty = active_difficulty
    # NOTE: `high_scores` is deliberately NOT reset here. It is the one piece of
    # state that outlives a round -- resetting it would defeat the whole point
    # of a high-score table. See init below.


if "status" not in st.session_state:
    start_new_game(difficulty)

# Survives New Game and difficulty changes; only ever cleared by the explicit
# "Reset high scores" button in the sidebar.
if "high_scores" not in st.session_state:
    st.session_state.high_scores = {}

# # FIX: the secret used to be generated once inside `if "secret" not in
# st.session_state` and never reseeded. Switching from Normal to Easy narrowed
# the range to 1-20 but left the old secret (87 in my repro) in place, so the
# game became mathematically unwinnable. Changing difficulty now starts a fresh
# round in the new range.
if st.session_state.difficulty != difficulty:
    start_new_game(difficulty)
    st.info(f"Difficulty changed to {difficulty}. New game started.")

st.subheader("Make a guess")

# # FIX: two bugs in the status banner.
# 1. It was hardcoded to "between 1 and 100" regardless of difficulty, so on
#    Easy the game lied about its own rules.
# 2. Streamlit runs this script top to bottom on every interaction, so a banner
#    printed HERE is printed before the guess further down has been processed --
#    the count it showed was always one rerun behind (a fresh Normal game
#    advertised 7 of its 8 attempts, and after a guess it still said 8).
#
# The fix is to reserve the slots now and fill them at the end of the script,
# once this run's guess has actually been handled. That is the Streamlit idiom
# for "render at this position, with a value I do not know yet".
status_slot = st.empty()
debug_slot = st.empty()


def render_status() -> None:
    """Fill the reserved slots with the state as of the end of this run."""
    attempts_left = max(0, attempt_limit - st.session_state.attempts)
    status_slot.info(
        f"Guess a number between {low} and {high}. Attempts left: {attempts_left}"
    )
    with debug_slot.container():
        with st.expander("Developer Debug Info"):
            st.write("Secret:", st.session_state.secret)
            st.write("Attempts used:", st.session_state.attempts)
            st.write("Attempts left:", attempts_left)
            st.write("Score:", st.session_state.score)
            st.write("Difficulty:", difficulty)
            st.write("Status:", st.session_state.status)
            st.write("History:", st.session_state.history)
            st.write("High scores:", st.session_state.high_scores)


def render_sidebar_history() -> None:
    """Render the Guess History panel in the sidebar.

    Newest guess first, each row annotated with its Hot/Cold proximity so the
    player can see themselves closing in rather than having to remember.
    """
    st.sidebar.divider()
    st.sidebar.subheader("📜 Guess History")

    if not st.session_state.history:
        st.sidebar.caption("No guesses yet this round.")
        return

    secret = st.session_state.secret
    for number, guess in reversed(list(enumerate(st.session_state.history, start=1))):
        outcome = check_guess(guess, secret)
        arrow = {WIN: "🎯", TOO_HIGH: "⬇️", TOO_LOW: "⬆️"}[outcome]
        st.sidebar.write(
            f"{arrow} **{guess}** — {proximity_label(guess, secret, low, high)}"
            f"  \n<small>guess {number} · {outcome}</small>",
            unsafe_allow_html=True,
        )


def render_sidebar_high_scores() -> None:
    """Render the persistent High Scores table in the sidebar."""
    st.sidebar.divider()
    st.sidebar.subheader("🏆 High Scores")

    rows = format_high_scores(st.session_state.high_scores)
    if not rows:
        st.sidebar.caption("Win a round to set a record.")
        return

    st.sidebar.table(rows)
    if st.sidebar.button("Reset high scores"):
        st.session_state.high_scores = {}
        st.rerun()


raw_guess = st.text_input("Enter your guess:", key=f"guess_input_{difficulty}")

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    start_new_game(difficulty)
    st.success("New game started.")
    st.rerun()


def render_round_summary() -> None:
    """Show a per-guess summary table once the round is over."""
    if not st.session_state.history:
        return
    st.subheader("📊 Round summary")
    st.table(
        build_session_table(
            st.session_state.history, st.session_state.secret, low, high
        )
    )


if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success(
            f"You won with a score of {st.session_state.score}. "
            "Click New Game 🔁 to play again."
        )
    else:
        st.error(
            f"Game over -- the secret was {st.session_state.secret}. "
            "Click New Game 🔁 to try again."
        )
    render_round_summary()
    render_status()  # fill the reserved slots before bailing out of the script
    render_sidebar_history()
    render_sidebar_high_scores()
    st.stop()

if submit:
    # # FIX: `attempts += 1` used to run here, BEFORE validation, so a typo
    # like "abc" burned one of your turns. The attempt is only consumed once we
    # know the input is a real, in-range guess.
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.error(err)
    else:
        previous_guess = (
            st.session_state.history[-1] if st.session_state.history else None
        )
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # # FIX: the root cause of the lying hints was right here -- on every
        # even attempt the secret was coerced with str(), which broke the
        # equality check and turned `guess > secret` into a lexicographic
        # string comparison via a swallowed TypeError. The secret is passed
        # through as the int it has always been.
        outcome = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(hint_message(outcome))

            # Hot/Cold feedback: the direction hint says which way to move, the
            # proximity label says how far there is left to go, and the trend
            # says whether the last guess was an improvement.
            if outcome != WIN:
                trend = proximity_trend(
                    previous_guess, guess_int, st.session_state.secret
                )
                trend_text = {
                    "warmer": " (warmer than your last guess 🔺)",
                    "colder": " (colder than your last guess 🔻)",
                    "same": " (same distance as your last guess ➡️)",
                    "": "",
                }[trend]
                label = proximity_label(guess_int, st.session_state.secret, low, high)
                st.info(f"{label}{trend_text}")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == WIN:
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won in {st.session_state.attempts} "
                f"attempt{'s' if st.session_state.attempts != 1 else ''}! "
                f"The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )

            # High score tracking: only a win sets a record.
            previous_best = st.session_state.high_scores.get(difficulty)
            st.session_state.high_scores = update_high_scores(
                st.session_state.high_scores,
                difficulty,
                st.session_state.score,
                st.session_state.attempts,
            )
            if st.session_state.high_scores.get(difficulty) != previous_best:
                st.success(f"🏆 New {difficulty} high score!")

            render_round_summary()
        else:
            remaining = max(0, attempt_limit - st.session_state.attempts)
            if remaining == 0:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
                render_round_summary()

# Rendered last on purpose: by this point this run's guess has been counted, so
# the numbers shown are the real current ones rather than last run's.
render_status()
render_sidebar_history()
render_sidebar_high_scores()

st.divider()
st.caption("Rebuilt by a human who read the diff.")
