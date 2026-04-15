from unittest.mock import MagicMock, patch

import pytest

from src.resources.customers import _create_customer, _get_customer, _list_customers


@pytest.fixture
def client():
    return MagicMock()


@pytest.fixture(autouse=True)
def no_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")


# --- _list_customers ---


def test_list_customers_calls_client_with_email(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    with patch("src.resources.customers.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "test@example.com"
        _list_customers(client)

    client.customers.list.assert_called_once_with({"email": "test@example.com"})


def test_list_customers_trims_whitespace_from_email(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    with patch("src.resources.customers.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "  user@test.com  "
        _list_customers(client)

    client.customers.list.assert_called_once_with({"email": "user@test.com"})


def test_list_customers_empty_email_shows_error_and_skips_client(capsys, client):
    with patch("src.resources.customers.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "   "
        _list_customers(client)

    output = capsys.readouterr().out
    assert "✗" in output
    client.customers.list.assert_not_called()


def test_list_customers_user_cancels_skips_client(client):
    with patch("src.resources.customers.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = None
        _list_customers(client)

    client.customers.list.assert_not_called()


# --- _get_customer ---


def test_get_customer_calls_client_with_integer_id(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.customers.get.return_value = {"id": 42, "name": "John"}

    with patch("src.resources.customers.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "42"
        _get_customer(client)

    client.customers.get.assert_called_once_with(42)


def test_get_customer_invalid_id_shows_error_and_skips_client(capsys, client):
    with patch("src.resources.customers.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "not-a-number"
        _get_customer(client)

    output = capsys.readouterr().out
    assert "✗" in output
    client.customers.get.assert_not_called()


def test_get_customer_user_cancels_skips_client(client):
    with patch("src.resources.customers.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = None
        _get_customer(client)

    client.customers.get.assert_not_called()


# --- _create_customer ---


def test_create_customer_calls_client_with_payload(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.customers.create.return_value = {"id": 1}

    _create_customer(client)

    assert client.customers.create.called
    payload_arg = client.customers.create.call_args[0][0]
    assert isinstance(payload_arg, dict)
    assert "name" in payload_arg
    assert "email" in payload_arg


def test_create_customer_api_error_shows_error(capsys, client):
    client.customers.create.side_effect = Exception("validation error")

    _create_customer(client)

    output = capsys.readouterr().out
    assert "validation error" in output
