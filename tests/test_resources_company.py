from unittest.mock import MagicMock

import pytest

from src.resources.company import _get_company, _update_company


@pytest.fixture
def client():
    return MagicMock()


@pytest.fixture(autouse=True)
def no_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")


# --- _get_company ---


def test_get_company_calls_client(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.company.get.return_value = {"id": 1, "name": "Acme Corp"}

    _get_company(client)

    client.company.get.assert_called_once()


def test_get_company_api_error_shows_error(capsys, client):
    client.company.get.side_effect = Exception("not found")

    _get_company(client)

    output = capsys.readouterr().out
    assert "not found" in output


# --- _update_company ---


def test_update_company_calls_client_with_payload(client, tmp_path, monkeypatch):
    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))
    client.company.update.return_value = {"id": 1}

    _update_company(client)

    assert client.company.update.called
    assert isinstance(client.company.update.call_args[0][0], dict)


def test_update_company_api_error_shows_error(capsys, client):
    client.company.update.side_effect = Exception("permission denied")

    _update_company(client)

    output = capsys.readouterr().out
    assert "permission denied" in output
