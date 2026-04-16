import questionary

from src.utils import (
    format_currency,
    load_payload,
    print_error,
    print_result_with_file,
    print_success,
)


def transactions_menu(client) -> None:
    while True:
        choice = questionary.select(
            "Transactions - Select an operation:",
            choices=[
                "List Transactions",
                "Get Transaction by ID",
                "Create Transaction",
                "Refund Transaction",
                "Update Delivery Status",
                "← Back",
            ],
        ).ask()

        if choice is None or choice == "← Back":
            return

        if choice == "List Transactions":
            _list_transactions(client)
        elif choice == "Get Transaction by ID":
            _get_transaction(client)
        elif choice == "Create Transaction":
            _create_transaction(client)
        elif choice == "Refund Transaction":
            _refund_transaction(client)
        elif choice == "Update Delivery Status":
            _update_delivery(client)


def _list_transactions(client) -> None:
    try:
        params = {}

        limit = questionary.text("Limit (leave empty for default):").ask()
        if limit is None:
            return
        if limit.strip():
            params["limit"] = int(limit.strip())

        offset = questionary.text("Offset (leave empty for default):").ask()
        if offset is None:
            return
        if offset.strip():
            params["offset"] = int(offset.strip())

        created_from = questionary.text("Created from - ISO date (leave empty to skip):").ask()
        if created_from is None:
            return
        if created_from.strip():
            params["createdFrom"] = created_from.strip()

        result = client.transactions.list(params if params else None)
        print_success("Transactions retrieved successfully!")
        print_result_with_file("transactions_list", result)
    except ValueError:
        print_error("Invalid numeric value.")
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _get_transaction(client) -> None:
    try:
        id_str = questionary.text("Enter transaction ID:").ask()
        if id_str is None:
            return

        transaction_id = int(id_str)
        result = client.transactions.get(transaction_id)
        print_success(f"Transaction {transaction_id} retrieved successfully!")
        print_result_with_file("transactions_get", result)
    except ValueError:
        print_error("Invalid ID. Please enter a numeric value.")
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _create_transaction(client) -> None:
    try:
        payload = load_payload("transaction-create.json")
        print("\n  Payload: transaction-create.json")

        if "amount" in payload:
            print(f"  Amount: {format_currency(payload['amount'])}")

        result = client.transactions.create(payload)
        print_success("Transaction created successfully!")
        print_result_with_file("transactions_create", result)
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _refund_transaction(client) -> None:
    try:
        id_str = questionary.text("Enter transaction ID to refund:").ask()
        if id_str is None:
            return

        transaction_id = int(id_str)

        refund_type = questionary.select(
            "Refund type:",
            choices=["Full refund", "Partial refund"],
        ).ask()

        if refund_type is None:
            return

        if refund_type == "Partial refund":
            amount_str = questionary.text("Enter refund amount (in cents):").ask()
            if amount_str is None:
                return

            amount = int(amount_str)
            print(f"\n  Partial refund: {format_currency(amount)}")
            result = client.transactions.refund(transaction_id, amount)
        else:
            print("\n  Full refund")
            result = client.transactions.refund(transaction_id)

        print_success(f"Transaction {transaction_id} refunded successfully!")
        print_result_with_file("transactions_refund", result)
    except ValueError:
        print_error("Invalid numeric value.")
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _update_delivery(client) -> None:
    try:
        id_str = questionary.text("Enter transaction ID:").ask()
        if id_str is None:
            return

        transaction_id = int(id_str)
        payload = load_payload("delivery-update.json")
        print("\n  Payload: delivery-update.json")

        result = client.transactions.update_delivery(transaction_id, payload)
        print_success(f"Delivery status updated for transaction {transaction_id}!")
        print_result_with_file("transactions_update_delivery", result)
    except ValueError:
        print_error("Invalid ID. Please enter a numeric value.")
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")
