from unittest.mock import MagicMock

import pytest

from src.resources.balance import _get_balance


@pytest.fixture
def client():
    return MagicMock()


@pytest.fixture(autouse=True)
def no_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")


def test_get_balance_calls_client(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.balance.get.return_value = {"amount": 5000}

    _get_balance(client)

    client.balance.get.assert_called_once()


def test_get_balance_displays_formatted_amount(capsys, client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.balance.get.return_value = {"amount": 10000}

    _get_balance(client)

    output = capsys.readouterr().out
    assert "R$ 100,00" in output


def test_get_balance_without_amount_field_does_not_crash(client, tmp_path, monkeypatch):
    # API may return a dict without "amount" — should not raise
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.balance.get.return_value = {"status": "ok"}

    _get_balance(client)

    client.balance.get.assert_called_once()


def test_get_balance_handles_api_error(capsys, client):
    client.balance.get.side_effect = Exception("unauthorized")

    _get_balance(client)

    output = capsys.readouterr().out
    assert "unauthorized" in output
