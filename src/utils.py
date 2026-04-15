import json
import os
from datetime import datetime, timezone
from pathlib import Path


def load_payload(filename: str) -> dict:
    payload_path = Path(__file__).resolve().parent.parent / "payloads" / filename
    if not payload_path.exists():
        raise FileNotFoundError(f"Payload file not found: {payload_path}")
    with open(payload_path, encoding="utf-8") as f:
        return json.load(f)


def save_output(operation: str, data, sdk_info: dict | None = None) -> str:
    output_dir = Path(os.getenv("OUTPUT_DIR", "./output"))
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"{timestamp}_{operation}.json"
    filepath = output_dir / filename

    output = {"operation": operation, "timestamp": timestamp, "data": data}
    if sdk_info:
        output["sdk_info"] = sdk_info

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)

    return str(filepath)


def format_currency(amount_in_cents: int) -> str:
    value = amount_in_cents / 100
    formatted = f"{value:,.2f}"
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatted}"


def print_success(message: str) -> None:
    print(f"\033[32m✓ {message}\033[0m")


def print_error(message: str) -> None:
    print(f"\033[31m✗ {message}\033[0m")


def print_result(data) -> None:
    if isinstance(data, list):
        print(f"\n  Items returned: {len(data)}")
    elif isinstance(data, dict):
        print(f"\n  Keys: {len(data)}")
    print(f"\n{json.dumps(data, indent=2, ensure_ascii=False, default=str)}")


def print_result_with_file(operation: str, data, sdk_info: dict | None = None) -> None:
    print_result(data)
    filepath = save_output(operation, data, sdk_info)
    print(f"\n\033[90mOutput saved to: {filepath}\033[0m")
