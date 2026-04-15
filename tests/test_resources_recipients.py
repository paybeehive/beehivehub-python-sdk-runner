from unittest.mock import MagicMock, patch

import pytest

from src.resources.recipients import (
    _create_recipient,
    _get_recipient,
    _list_recipients,
    _update_recipient,
)


@pytest.fixture
def client():
    return MagicMock()


@pytest.fixture(autouse=True)
def no_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")


# --- _list_recipients ---


def test_list_recipients_calls_client(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.recipients.list.return_value = []

    _list_recipients(client)

    client.recipients.list.assert_called_once()


def test_list_recipients_api_error_shows_error(capsys, client):
    client.recipients.list.side_effect = Exception("forbidden")

    _list_recipients(client)

    output = capsys.readouterr().out
    assert "forbidden" in output


# --- _get_recipient ---


def test_get_recipient_calls_client_with_integer_id(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.recipients.get.return_value = {"id": 3}

    with patch("src.resources.recipients.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "3"
        _get_recipient(client)

    client.recipients.get.assert_called_once_with(3)


def test_get_recipient_invalid_id_shows_error(capsys, client):
    with patch("src.resources.recipients.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "bad"
        _get_recipient(client)

    output = capsys.readouterr().out
    assert "✗" in output
    client.recipients.get.assert_not_called()


def test_get_recipient_user_cancels_skips_client(client):
    with patch("src.resources.recipients.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = None
        _get_recipient(client)

    client.recipients.get.assert_not_called()


# --- _create_recipient ---


def test_create_recipient_calls_client_with_payload(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.recipients.create.return_value = {"id": 10}

    _create_recipient(client)

    assert client.recipients.create.called
    assert isinstance(client.recipients.create.call_args[0][0], dict)


# --- _update_recipient ---


def test_update_recipient_calls_client_with_id_and_payload(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.recipients.update.return_value = {"id": 3}

    with patch("src.resources.recipients.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "3"
        _update_recipient(client)

    call_args = client.recipients.update.call_args[0]
    assert call_args[0] == 3
    assert isinstance(call_args[1], dict)


def test_update_recipient_invalid_id_shows_error(capsys, client):
    with patch("src.resources.recipients.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "nope"
        _update_recipient(client)

    output = capsys.readouterr().out
    assert "✗" in output
    client.recipients.update.assert_not_called()
