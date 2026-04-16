import questionary

from src.utils import load_payload, print_error, print_result_with_file, print_success


def recipients_menu(client) -> None:
    while True:
        choice = questionary.select(
            "Recipients - Select an operation:",
            choices=[
                "List Recipients",
                "Get Recipient by ID",
                "Create Recipient",
                "Update Recipient",
                "← Back",
            ],
        ).ask()

        if choice is None or choice == "← Back":
            return

        if choice == "List Recipients":
            _list_recipients(client)
        elif choice == "Get Recipient by ID":
            _get_recipient(client)
        elif choice == "Create Recipient":
            _create_recipient(client)
        elif choice == "Update Recipient":
            _update_recipient(client)


def _list_recipients(client) -> None:
    try:
        result = client.recipients.list()
        print_success("Recipients retrieved successfully!")
        print_result_with_file("recipients_list", result)
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _get_recipient(client) -> None:
    try:
        id_str = questionary.text("Enter recipient ID:").ask()
        if id_str is None:
            return

        recipient_id = int(id_str)
        result = client.recipients.get(recipient_id)
        print_success(f"Recipient {recipient_id} retrieved successfully!")
        print_result_with_file("recipients_get", result)
    except ValueError:
        print_error("Invalid ID. Please enter a numeric value.")
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _create_recipient(client) -> None:
    try:
        payload = load_payload("recipient-create.json")
        print("\n  Payload: recipient-create.json")

        result = client.recipients.create(payload)
        print_success("Recipient created successfully!")
        print_result_with_file("recipients_create", result)
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _update_recipient(client) -> None:
    try:
        id_str = questionary.text("Enter recipient ID to update:").ask()
        if id_str is None:
            return

        recipient_id = int(id_str)
        payload = load_payload("recipient-update.json")
        print("\n  Payload: recipient-update.json")

        result = client.recipients.update(recipient_id, payload)
        print_success(f"Recipient {recipient_id} updated successfully!")
        print_result_with_file("recipients_update", result)
    except ValueError:
        print_error("Invalid ID. Please enter a numeric value.")
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")
