import sys
from pathlib import Path

from dotenv import load_dotenv


def check_env() -> None:
    env_path = Path(__file__).resolve().parent.parent / ".env"

    if not env_path.exists():
        print("\n\033[31m✗ .env file not found!\033[0m")
        print("\nTo get started:")
        print("  1. Copy the example file:  cp .env.example .env")
        print("  2. Edit .env and add your BEEHIVE_SECRET_KEY")
        print("  3. Run again:  python -m src.cli")
        sys.exit(1)

    load_dotenv(env_path)

    import os

    secret_key = os.getenv("BEEHIVE_SECRET_KEY", "")

    if not secret_key or secret_key == "your_secret_key_here":
        print("\n\033[31m✗ BEEHIVE_SECRET_KEY is not configured!\033[0m")
        print("\nEdit your .env file and set a valid API key.")
        print("Get your key at: https://docs.beehivehub.io/")
        sys.exit(1)
