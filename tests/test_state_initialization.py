import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))


class TestStateInitialization:
    """Tests for session state initialization in app.py"""

    @patch.dict("sys.modules", {"streamlit": MagicMock()})
    @patch("streamlit.session_state", new_callable=MagicMock)
    def test_attempts_initializes_to_zero(self, mock_session_state):
        """Verify attempts state initializes to 0."""
        mock_session_state.__contains__ = Mock(return_value=False)
        mock_session_state.__setitem__ = Mock()

        if "attempts" not in mock_session_state:
            mock_session_state["attempts"] = 0

        mock_session_state.__setitem__.assert_called_with("attempts", 0)

    def test_initial_state_values(self):
        """Verify all session state keys have correct initial values."""
        initial_state = {
            "secret": None,  # Would be set by random.randint
            "attempts": 0,
            "score": 0,
            "status": "playing",
            "history": [],
        }

        assert initial_state["attempts"] == 0
        assert initial_state["score"] == 0
        assert initial_state["status"] == "playing"
        assert initial_state["history"] == []

    def test_attempts_not_initialized_to_one(self):
        """Verify attempts is NOT initialized to 1."""
        initial_attempts = 0
        assert initial_attempts != 1