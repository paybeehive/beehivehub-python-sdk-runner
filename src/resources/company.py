import questionary

from src.utils import load_payload, print_error, print_result_with_file, print_success


def company_menu(client) -> None:
    while True:
        choice = questionary.select(
            "Company - Select an operation:",
            choices=["Get Company", "Update Company", "← Back"],
        ).ask()

        if choice is None or choice == "← Back":
            return

        if choice == "Get Company":
            _get_company(client)
        elif choice == "Update Company":
            _update_company(client)


def _get_company(client) -> None:
    try:
        result = client.company.get()
        print_success("Company retrieved successfully!")
        print_result_with_file("company_get", result)
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _update_company(client) -> None:
    try:
        payload = load_payload("company-update.json")
        print("\n  Payload: company-update.json")

        result = client.company.update(payload)
        print_success("Company updated successfully!")
        print_result_with_file("company_update", result)
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")
