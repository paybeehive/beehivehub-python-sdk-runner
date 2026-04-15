from unittest.mock import MagicMock, patch

import pytest

from src.check_env import check_env


def _mock_env_path(exists: bool) -> MagicMock:
    m = MagicMock()
    m.exists.return_value = exists
    return m


def _set_mock_path(MockPath, exists: bool) -> None:
    MockPath.return_value.resolve.return_value.parent.parent.__truediv__.return_value = (
        _mock_env_path(exists)
    )


def test_missing_env_file_exits_with_code_1():
    with patch("src.check_env.Path") as MockPath:
        _set_mock_path(MockPath, False)
        with pytest.raises(SystemExit) as exc_info:
            check_env()
    assert exc_info.value.code == 1


def test_env_file_present_but_key_is_empty_exits(monkeypatch):
    monkeypatch.setenv("BEEHIVE_SECRET_KEY", "")
    with patch("src.check_env.Path") as MockPath, patch("src.check_env.load_dotenv"):
        _set_mock_path(MockPath, True)
        with pytest.raises(SystemExit) as exc_info:
            check_env()
    assert exc_info.value.code == 1


def test_env_file_present_but_key_is_placeholder_exits(monkeypatch):
    # The placeholder value from .env.example should be treated as unconfigured
    monkeypatch.setenv("BEEHIVE_SECRET_KEY", "your_secret_key_here")
    with patch("src.check_env.Path") as MockPath, patch("src.check_env.load_dotenv"):
        _set_mock_path(MockPath, True)
        with pytest.raises(SystemExit) as exc_info:
            check_env()
    assert exc_info.value.code == 1


def test_env_file_with_valid_key_does_not_exit(monkeypatch):
    monkeypatch.setenv("BEEHIVE_SECRET_KEY", "sk_live_abc123")
    with patch("src.check_env.Path") as MockPath, patch("src.check_env.load_dotenv"):
        _set_mock_path(MockPath, True)
        check_env()  # should not raise SystemExit
