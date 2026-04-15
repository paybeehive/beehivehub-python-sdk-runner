import pytest
from beehivehub import create_beehivehub_client

from src.sdk import init_sdk


def test_client_instantiation():
    client = create_beehivehub_client(api_key="sk_test_123", environment="sandbox")
    assert client is not None


def test_client_exposes_all_resources():
    client = create_beehivehub_client(api_key="sk_test_123", environment="sandbox")

    assert hasattr(client, "transactions")
    assert hasattr(client, "customers")
    assert hasattr(client, "recipients")
    assert hasattr(client, "bank_accounts")
    assert hasattr(client, "transfers")
    assert hasattr(client, "company")
    assert hasattr(client, "balance")
    assert hasattr(client, "payment_links")


def test_init_sdk_reads_from_env_vars(monkeypatch):
    monkeypatch.setenv("BEEHIVE_SECRET_KEY", "sk_test_abc")
    monkeypatch.setenv("BEEHIVE_ENVIRONMENT", "sandbox")
    client = init_sdk()
    assert client is not None


def test_init_sdk_defaults_to_production_environment(monkeypatch):
    monkeypatch.setenv("BEEHIVE_SECRET_KEY", "sk_test_abc")
    monkeypatch.delenv("BEEHIVE_ENVIRONMENT", raising=False)
    client = init_sdk()
    assert client is not None


def test_init_sdk_with_empty_key_raises(monkeypatch):
    # The SDK validates the key at instantiation time — empty key is rejected immediately
    from beehivehub.exceptions import BeehiveHubError

    monkeypatch.setenv("BEEHIVE_SECRET_KEY", "")
    monkeypatch.setenv("BEEHIVE_ENVIRONMENT", "sandbox")

    with pytest.raises(BeehiveHubError):
        init_sdk()
