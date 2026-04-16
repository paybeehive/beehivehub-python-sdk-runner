import questionary

from src.utils import load_payload, print_error, print_result_with_file, print_success


def bank_accounts_menu(client) -> None:
    while True:
        choice = questionary.select(
            "Bank Accounts - Select an operation:",
            choices=["List Bank Accounts", "Create Bank Account", "← Back"],
        ).ask()

        if choice is None or choice == "← Back":
            return

        if choice == "List Bank Accounts":
            _list_bank_accounts(client)
        elif choice == "Create Bank Account":
            _create_bank_account(client)


def _list_bank_accounts(client) -> None:
    try:
        id_str = questionary.text("Enter recipient ID:").ask()
        if id_str is None:
            return

        recipient_id = int(id_str)
        result = client.bank_accounts.list(recipient_id)
        print_success(f"Bank accounts for recipient {recipient_id} retrieved!")
        print_result_with_file("bank_accounts_list", result)
    except ValueError:
        print_error("Invalid ID. Please enter a numeric value.")
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _create_bank_account(client) -> None:
    try:
        id_str = questionary.text("Enter recipient ID:").ask()
        if id_str is None:
            return

        recipient_id = int(id_str)
        payload = load_payload("bank-account-create.json")
        print("\n  Payload: bank-account-create.json")

        result = client.bank_accounts.create(recipient_id, payload)
        print_success(f"Bank account created for recipient {recipient_id}!")
        print_result_with_file("bank_accounts_create", result)
    except ValueError:
        print_error("Invalid ID. Please enter a numeric value.")
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")
