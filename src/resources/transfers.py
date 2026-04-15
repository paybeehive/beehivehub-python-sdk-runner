import questionary

from src.utils import (
    format_currency,
    load_payload,
    print_error,
    print_result_with_file,
    print_success,
)


def transfers_menu(client) -> None:
    while True:
        choice = questionary.select(
            "Transfers - Select an operation:",
            choices=["Create Transfer", "Get Transfer by ID", "← Back"],
        ).ask()

        if choice is None or choice == "← Back":
            return

        if choice == "Create Transfer":
            _create_transfer(client)
        elif choice == "Get Transfer by ID":
            _get_transfer(client)


def _create_transfer(client) -> None:
    try:
        payload = load_payload("transfer-create.json")
        print("\n  Payload: transfer-create.json")

        if "amount" in payload:
            print(f"  Amount: {format_currency(payload['amount'])}")

        result = client.transfers.create(payload)
        print_success("Transfer created successfully!")
        print_result_with_file("transfers_create", result)
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _get_transfer(client) -> None:
    try:
        id_str = questionary.text("Enter transfer ID:").ask()
        if id_str is None:
            return

        transfer_id = int(id_str)
        result = client.transfers.get(transfer_id)
        print_success(f"Transfer {transfer_id} retrieved successfully!")
        print_result_with_file("transfers_get", result)
    except ValueError:
        print_error("Invalid ID. Please enter a numeric value.")
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")
