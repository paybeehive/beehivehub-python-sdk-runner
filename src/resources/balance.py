import questionary

from src.utils import format_currency, print_error, print_result_with_file, print_success


def balance_menu(client) -> None:
    while True:
        choice = questionary.select(
            "Balance - Select an operation:",
            choices=["Get Balance", "← Back"],
        ).ask()

        if choice is None or choice == "← Back":
            return

        if choice == "Get Balance":
            _get_balance(client)


def _get_balance(client) -> None:
    try:
        result = client.balance.get()
        print_success("Balance retrieved successfully!")

        if isinstance(result, dict) and "amount" in result:
            print(f"\n  Available: {format_currency(result['amount'])}")

        print_result_with_file("balance_get", result)
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")
