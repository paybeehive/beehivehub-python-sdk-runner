import os

from beehivehub import create_beehivehub_client


def init_sdk():
    api_key = os.getenv("BEEHIVE_SECRET_KEY", "")
    environment = os.getenv("BEEHIVE_ENVIRONMENT", "production")

    return create_beehivehub_client(api_key=api_key, environment=environment)
