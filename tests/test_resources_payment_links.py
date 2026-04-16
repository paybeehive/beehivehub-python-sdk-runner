from unittest.mock import MagicMock, patch

import pytest

from src.resources.payment_links import (
    _create_payment_link,
    _delete_payment_link,
    _get_payment_link,
    _list_payment_links,
    _update_payment_link,
)


@pytest.fixture
def client():
    return MagicMock()


@pytest.fixture(autouse=True)
def no_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")


# --- _list_payment_links ---


def test_list_payment_links_calls_client(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.payment_links.list.return_value = []

    _list_payment_links(client)

    client.payment_links.list.assert_called_once()


# --- _get_payment_link ---


def test_get_payment_link_calls_client_with_integer_id(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.payment_links.get.return_value = {"id": 7}

    with patch("src.resources.payment_links.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "7"
        _get_payment_link(client)

    client.payment_links.get.assert_called_once_with(7)


def test_get_payment_link_displays_url_when_present(capsys, client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.payment_links.get.return_value = {"id": 7, "url": "https://pay.example.com/abc"}

    with patch("src.resources.payment_links.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "7"
        _get_payment_link(client)

    output = capsys.readouterr().out
    assert "https://pay.example.com/abc" in output


def test_get_payment_link_invalid_id_shows_error(capsys, client):
    with patch("src.resources.payment_links.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "bad"
        _get_payment_link(client)

    output = capsys.readouterr().out
    assert "✗" in output
    client.payment_links.get.assert_not_called()


# --- _create_payment_link ---


def test_create_payment_link_calls_client_with_payload(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.payment_links.create.return_value = {"id": 1, "url": "https://pay.example.com/new"}

    _create_payment_link(client)

    assert client.payment_links.create.called
    assert isinstance(client.payment_links.create.call_args[0][0], dict)


def test_create_payment_link_displays_url_on_success(capsys, client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.payment_links.create.return_value = {"id": 1, "url": "https://pay.example.com/new"}

    _create_payment_link(client)

    output = capsys.readouterr().out
    assert "https://pay.example.com/new" in output


# --- _update_payment_link ---


def test_update_payment_link_calls_client_with_id_and_payload(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.payment_links.update.return_value = {"id": 4}

    with patch("src.resources.payment_links.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "4"
        _update_payment_link(client)

    call_args = client.payment_links.update.call_args[0]
    assert call_args[0] == 4
    assert isinstance(call_args[1], dict)


def test_update_payment_link_invalid_id_shows_error(capsys, client):
    with patch("src.resources.payment_links.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "???"
        _update_payment_link(client)

    output = capsys.readouterr().out
    assert "✗" in output
    client.payment_links.update.assert_not_called()


# --- _delete_payment_link ---


def test_delete_payment_link_calls_client_with_integer_id(client):
    with patch("src.resources.payment_links.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "9"
        _delete_payment_link(client)

    client.payment_links.delete.assert_called_once_with(9)


def test_delete_payment_link_invalid_id_shows_error(capsys, client):
    with patch("src.resources.payment_links.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "nope"
        _delete_payment_link(client)

    output = capsys.readouterr().out
    assert "✗" in output
    client.payment_links.delete.assert_not_called()
