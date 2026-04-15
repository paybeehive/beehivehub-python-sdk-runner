from unittest.mock import MagicMock, patch

import pytest

from src.resources.bank_accounts import _create_bank_account, _list_bank_accounts


@pytest.fixture
def client():
    return MagicMock()


@pytest.fixture(autouse=True)
def no_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")


# --- _list_bank_accounts ---


def test_list_bank_accounts_calls_client_with_integer_id(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.bank_accounts.list.return_value = []

    with patch("src.resources.bank_accounts.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "12"
        _list_bank_accounts(client)

    client.bank_accounts.list.assert_called_once_with(12)


def test_list_bank_accounts_invalid_id_shows_error(capsys, client):
    with patch("src.resources.bank_accounts.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "abc"
        _list_bank_accounts(client)

    output = capsys.readouterr().out
    assert "✗" in output
    client.bank_accounts.list.assert_not_called()


def test_list_bank_accounts_user_cancels_skips_client(client):
    with patch("src.resources.bank_accounts.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = None
        _list_bank_accounts(client)

    client.bank_accounts.list.assert_not_called()


# --- _create_bank_account ---


def test_create_bank_account_calls_client_with_id_and_payload(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.bank_accounts.create.return_value = {"id": 1}

    with patch("src.resources.bank_accounts.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "12"
        _create_bank_account(client)

    call_args = client.bank_accounts.create.call_args[0]
    assert call_args[0] == 12
    assert isinstance(call_args[1], dict)


def test_create_bank_account_invalid_id_shows_error(capsys, client):
    with patch("src.resources.bank_accounts.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "oops"
        _create_bank_account(client)

    output = capsys.readouterr().out
    assert "✗" in output
    client.bank_accounts.create.assert_not_called()
