import os
import sys

import questionary

from src.check_env import check_env
from src.resources.balance import balance_menu
from src.resources.bank_accounts import bank_accounts_menu
from src.resources.company import company_menu
from src.resources.customers import customers_menu
from src.resources.payment_links import payment_links_menu
from src.resources.recipients import recipients_menu
from src.resources.transactions import transactions_menu
from src.resources.transfers import transfers_menu
from src.sdk import init_sdk


def main() -> None:
    check_env()

    environment = os.getenv("BEEHIVE_ENVIRONMENT", "production")

    print("\n\033[1m🐝 BeehiveHub Python SDK Runner\033[0m")
    print("Interactive tool for testing the Beehive Hub SDK")
    print(f"Environment: \033[33m{environment}\033[0m\n")

    client = init_sdk()

    menu_options = {
        "Transactions": lambda: transactions_menu(client),
        "Customers": lambda: customers_menu(client),
        "Payment Links": lambda: payment_links_menu(client),
        "Recipients": lambda: recipients_menu(client),
        "Bank Accounts": lambda: bank_accounts_menu(client),
        "Transfers": lambda: transfers_menu(client),
        "Company": lambda: company_menu(client),
        "Balance": lambda: balance_menu(client),
        "Exit": None,
    }

    while True:
        try:
            choice = questionary.select(
                "Select a resource:",
                choices=list(menu_options.keys()),
            ).ask()

            if choice is None or choice == "Exit":
                print("\nBye! 👋")
                sys.exit(0)

            menu_options[choice]()

        except KeyboardInterrupt:
            print("\n\nBye! 👋")
            sys.exit(0)


if __name__ == "__main__":
    main()
