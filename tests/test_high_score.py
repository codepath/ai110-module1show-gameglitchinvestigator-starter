import json

import pytest

from high_score import load_scores, save_score, _sort_and_cap


def test_save_score_persists_and_round_trips(tmp_path):
    # A saved score must be written to disk and reload identically.
    path = tmp_path / "scores.json"
    board = save_score("Normal", score=80, attempts=3, path=path)

    assert board == [{"score": 80, "attempts": 3}]

    reloaded = load_scores(path)
    assert reloaded == {"Normal": [{"score": 80, "attempts": 3}]}


def test_missing_file_returns_empty_dict(tmp_path):
    # load_scores on a path that does not exist must not crash; it returns {}.
    path = tmp_path / "does_not_exist.json"
    assert load_scores(path) == {}


def test_corrupt_file_returns_empty_dict(tmp_path):
    # A malformed JSON file should be treated as "no scores" rather than raising.
    path = tmp_path / "corrupt.json"
    path.write_text("{not valid json", encoding="utf-8")
    assert load_scores(path) == {}


def test_sort_primary_by_fewest_attempts():
    # Fewer attempts ranks higher even when its score is lower.
    entries = [
        {"score": 100, "attempts": 5},
        {"score": 50, "attempts": 2},
    ]
    assert _sort_and_cap(entries) == [
        {"score": 50, "attempts": 2},
        {"score": 100, "attempts": 5},
    ]


def test_sort_breaks_attempt_ties_by_highest_score():
    # Same attempts -> higher score wins the tie-break.
    entries = [
        {"score": 30, "attempts": 3},
        {"score": 90, "attempts": 3},
        {"score": 60, "attempts": 3},
    ]
    assert _sort_and_cap(entries) == [
        {"score": 90, "attempts": 3},
        {"score": 60, "attempts": 3},
        {"score": 30, "attempts": 3},
    ]


def test_board_is_capped_at_five(tmp_path):
    # Inserting more than 5 scores keeps only the best 5 for that difficulty.
    path = tmp_path / "scores.json"
    for i in range(7):
        save_score("Hard", score=10 * i, attempts=i + 1, path=path)

    board = load_scores(path)["Hard"]
    assert len(board) == 5
    # Sorted by fewest attempts: attempts 1..5 survive, 6 and 7 are dropped.
    assert [e["attempts"] for e in board] == [1, 2, 3, 4, 5]


def test_better_late_score_evicts_worst(tmp_path):
    # Fill with 5 mediocre scores, then add one clearly better (fewest attempts).
    path = tmp_path / "scores.json"
    for attempts in (3, 4, 5, 6, 7):
        save_score("Easy", score=50, attempts=attempts, path=path)

    board = save_score("Easy", score=100, attempts=1, path=path)

    assert len(board) == 5
    assert board[0] == {"score": 100, "attempts": 1}
    # The worst (attempts=7) was evicted.
    assert all(e["attempts"] != 7 for e in board)


def test_leaderboards_are_separated_by_difficulty(tmp_path):
    # A score saved under one difficulty must not leak into another.
    path = tmp_path / "scores.json"
    save_score("Hard", score=70, attempts=2, path=path)

    scores = load_scores(path)
    assert "Hard" in scores
    assert "Easy" not in scores
    assert scores["Hard"] == [{"score": 70, "attempts": 2}]
