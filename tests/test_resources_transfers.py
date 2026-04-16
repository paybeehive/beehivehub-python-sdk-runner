from unittest.mock import MagicMock, patch

import pytest

from src.resources.transfers import _create_transfer, _get_transfer


@pytest.fixture
def client():
    return MagicMock()


@pytest.fixture(autouse=True)
def no_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")


# --- _create_transfer ---


def test_create_transfer_calls_client_with_payload(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.transfers.create.return_value = {"id": 1, "status": "pending"}

    _create_transfer(client)

    assert client.transfers.create.called
    payload_arg = client.transfers.create.call_args[0][0]
    assert isinstance(payload_arg, dict)


def test_create_transfer_api_error_shows_error(capsys, client):
    client.transfers.create.side_effect = Exception("insufficient funds")

    _create_transfer(client)

    output = capsys.readouterr().out
    assert "insufficient funds" in output


# --- _get_transfer ---


def test_get_transfer_calls_client_with_integer_id(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.transfers.get.return_value = {"id": 5}

    with patch("src.resources.transfers.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "5"
        _get_transfer(client)

    client.transfers.get.assert_called_once_with(5)


def test_get_transfer_invalid_id_shows_error(capsys, client):
    with patch("src.resources.transfers.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "xyz"
        _get_transfer(client)

    output = capsys.readouterr().out
    assert "✗" in output
    client.transfers.get.assert_not_called()


def test_get_transfer_user_cancels_skips_client(client):
    with patch("src.resources.transfers.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = None
        _get_transfer(client)

    client.transfers.get.assert_not_called()
