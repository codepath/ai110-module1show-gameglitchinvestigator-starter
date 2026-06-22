"""Persistent high-score tracking.

Scores are stored in a single JSON file, keyed by difficulty level. Each
difficulty keeps only its top 5 entries, ranked by fewest attempts first and
then by highest score. All file access is defensive: a missing or corrupt
file is treated as "no scores yet" rather than an error.
"""

import json
from pathlib import Path

# Default location of the scoreboard file (project root).
DEFAULT_PATH = Path(__file__).resolve().parent / "high_scores.json"

# Maximum number of entries retained per difficulty.
MAX_ENTRIES = 5


def _sort_and_cap(entries):
    """Sort entries by fewest attempts, then highest score, and keep the top 5.

    Args:
        entries: A list of ``{"score": int, "attempts": int}`` dicts.

    Returns:
        A new list sorted with the best entry first, truncated to ``MAX_ENTRIES``.
    """
    ranked = sorted(entries, key=lambda e: (e["attempts"], -e["score"]))
    return ranked[:MAX_ENTRIES]


def load_scores(path=DEFAULT_PATH):
    """Load the full scoreboard from disk.

    Args:
        path: Path to the JSON scoreboard file.

    Returns:
        A dict mapping difficulty -> list of score entries. Returns an empty
        dict if the file does not exist or cannot be parsed.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_score(difficulty, score, attempts, path=DEFAULT_PATH):
    """Record a completed game's result and persist the updated leaderboard.

    Loads the current scoreboard, inserts the new entry under ``difficulty``,
    re-sorts and caps that difficulty's list at 5, then writes everything back.

    Args:
        difficulty: The difficulty level ("Easy", "Normal", "Hard", ...).
        score: The final score achieved.
        attempts: The number of attempts the player used.
        path: Path to the JSON scoreboard file.

    Returns:
        The capped, sorted list of entries for ``difficulty`` after insertion.
    """
    scores = load_scores(path)

    board = scores.get(difficulty, [])
    board.append({"score": int(score), "attempts": int(attempts)})
    board = _sort_and_cap(board)
    scores[difficulty] = board

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(scores, fh, indent=2)

    return board
