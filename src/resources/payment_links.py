import questionary

from src.utils import (
    format_currency,
    load_payload,
    print_error,
    print_result_with_file,
    print_success,
)


def payment_links_menu(client) -> None:
    while True:
        choice = questionary.select(
            "Payment Links - Select an operation:",
            choices=[
                "List Payment Links",
                "Get Payment Link by ID",
                "Create Payment Link",
                "Update Payment Link",
                "Delete Payment Link",
                "← Back",
            ],
        ).ask()

        if choice is None or choice == "← Back":
            return

        if choice == "List Payment Links":
            _list_payment_links(client)
        elif choice == "Get Payment Link by ID":
            _get_payment_link(client)
        elif choice == "Create Payment Link":
            _create_payment_link(client)
        elif choice == "Update Payment Link":
            _update_payment_link(client)
        elif choice == "Delete Payment Link":
            _delete_payment_link(client)


def _list_payment_links(client) -> None:
    try:
        result = client.payment_links.list()
        print_success("Payment links retrieved successfully!")
        print_result_with_file("payment_links_list", result)
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _get_payment_link(client) -> None:
    try:
        id_str = questionary.text("Enter payment link ID:").ask()
        if id_str is None:
            return

        link_id = int(id_str)
        result = client.payment_links.get(link_id)
        print_success(f"Payment link {link_id} retrieved successfully!")

        if isinstance(result, dict) and "url" in result:
            print(f"\n  URL: {result['url']}")

        print_result_with_file("payment_links_get", result)
    except ValueError:
        print_error("Invalid ID. Please enter a numeric value.")
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _create_payment_link(client) -> None:
    try:
        payload = load_payload("payment-link-create.json")
        print("\n  Payload: payment-link-create.json")

        if "amount" in payload:
            print(f"  Amount: {format_currency(payload['amount'])}")

        result = client.payment_links.create(payload)
        print_success("Payment link created successfully!")

        if isinstance(result, dict) and "url" in result:
            print(f"\n  Share URL: {result['url']}")

        print_result_with_file("payment_links_create", result)
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _update_payment_link(client) -> None:
    try:
        id_str = questionary.text("Enter payment link ID to update:").ask()
        if id_str is None:
            return

        link_id = int(id_str)
        payload = load_payload("payment-link-update.json")
        print("\n  Payload: payment-link-update.json")

        result = client.payment_links.update(link_id, payload)
        print_success(f"Payment link {link_id} updated successfully!")
        print_result_with_file("payment_links_update", result)
    except ValueError:
        print_error("Invalid ID. Please enter a numeric value.")
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _delete_payment_link(client) -> None:
    try:
        id_str = questionary.text("Enter payment link ID to delete:").ask()
        if id_str is None:
            return

        link_id = int(id_str)
        client.payment_links.delete(link_id)
        print_success(f"Payment link {link_id} deleted successfully!")
    except ValueError:
        print_error("Invalid ID. Please enter a numeric value.")
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")
