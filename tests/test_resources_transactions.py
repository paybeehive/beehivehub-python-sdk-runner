from unittest.mock import MagicMock, patch

import pytest

from src.resources.transactions import (
    _create_transaction,
    _get_transaction,
    _list_transactions,
    _refund_transaction,
    _update_delivery,
)


@pytest.fixture
def client():
    return MagicMock()


@pytest.fixture(autouse=True)
def no_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")


# --- _list_transactions ---


def test_list_transactions_with_all_params(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.transactions.list.return_value = []

    with patch("src.resources.transactions.questionary") as mock_q:
        mock_q.text.return_value.ask.side_effect = ["10", "5", "2024-01-01"]
        _list_transactions(client)

    client.transactions.list.assert_called_once_with(
        {"limit": 10, "offset": 5, "createdFrom": "2024-01-01"}
    )


def test_list_transactions_with_no_params_passes_none(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.transactions.list.return_value = []

    with patch("src.resources.transactions.questionary") as mock_q:
        mock_q.text.return_value.ask.side_effect = ["", "", ""]
        _list_transactions(client)

    client.transactions.list.assert_called_once_with(None)


def test_list_transactions_invalid_limit_shows_error(capsys, client):
    with patch("src.resources.transactions.questionary") as mock_q:
        mock_q.text.return_value.ask.side_effect = ["not-a-number", "", ""]
        _list_transactions(client)

    output = capsys.readouterr().out
    assert "✗" in output
    client.transactions.list.assert_not_called()


def test_list_transactions_user_cancels_at_first_prompt(client):
    with patch("src.resources.transactions.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = None
        _list_transactions(client)

    client.transactions.list.assert_not_called()


# --- _get_transaction ---


def test_get_transaction_calls_client_with_integer_id(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.transactions.get.return_value = {"id": 99}

    with patch("src.resources.transactions.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "99"
        _get_transaction(client)

    client.transactions.get.assert_called_once_with(99)


def test_get_transaction_invalid_id_shows_error(capsys, client):
    with patch("src.resources.transactions.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "abc"
        _get_transaction(client)

    output = capsys.readouterr().out
    assert "✗" in output
    client.transactions.get.assert_not_called()


# --- _create_transaction ---


def test_create_transaction_calls_client_with_payload(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.transactions.create.return_value = {"id": 1, "status": "pending"}

    _create_transaction(client)

    assert client.transactions.create.called
    payload_arg = client.transactions.create.call_args[0][0]
    assert isinstance(payload_arg, dict)


# --- _refund_transaction ---


def test_refund_transaction_full_refund(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.transactions.refund.return_value = {"status": "refunded"}

    with patch("src.resources.transactions.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "10"
        mock_q.select.return_value.ask.return_value = "Full refund"
        _refund_transaction(client)

    client.transactions.refund.assert_called_once_with(10)


def test_refund_transaction_partial_refund(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.transactions.refund.return_value = {"status": "refunded"}

    with patch("src.resources.transactions.questionary") as mock_q:
        mock_q.text.return_value.ask.side_effect = ["10", "2500"]
        mock_q.select.return_value.ask.return_value = "Partial refund"
        _refund_transaction(client)

    client.transactions.refund.assert_called_once_with(10, 2500)


# --- _update_delivery ---


def test_update_delivery_calls_client_with_id_and_payload(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.transactions.update_delivery.return_value = {"status": "delivered"}

    with patch("src.resources.transactions.questionary") as mock_q:
        mock_q.text.return_value.ask.return_value = "7"
        _update_delivery(client)

    assert client.transactions.update_delivery.called
    call_args = client.transactions.update_delivery.call_args[0]
    assert call_args[0] == 7
    assert isinstance(call_args[1], dict)
