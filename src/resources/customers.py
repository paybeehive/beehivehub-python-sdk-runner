import questionary

from src.utils import load_payload, print_error, print_result_with_file, print_success


def customers_menu(client) -> None:
    while True:
        choice = questionary.select(
            "Customers - Select an operation:",
            choices=["List Customers", "Get Customer by ID", "Create Customer", "← Back"],
        ).ask()

        if choice is None or choice == "← Back":
            return

        if choice == "List Customers":
            _list_customers(client)
        elif choice == "Get Customer by ID":
            _get_customer(client)
        elif choice == "Create Customer":
            _create_customer(client)


def _list_customers(client) -> None:
    try:
        email = questionary.text("Enter customer email to search:").ask()
        if email is None:
            return

        if not email.strip():
            print_error("Email is required to search customers.")
            input("\nPress Enter to continue...")
            return

        result = client.customers.list({"email": email.strip()})
        print_success(f"Customers found for '{email.strip()}'")
        print_result_with_file("customers_list", result)
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _get_customer(client) -> None:
    try:
        id_str = questionary.text("Enter customer ID:").ask()
        if id_str is None:
            return

        customer_id = int(id_str)
        result = client.customers.get(customer_id)
        print_success(f"Customer {customer_id} retrieved successfully!")
        print_result_with_file("customers_get", result)
    except ValueError:
        print_error("Invalid ID. Please enter a numeric value.")
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")


def _create_customer(client) -> None:
    try:
        payload = load_payload("customer-create.json")
        print("\n  Payload: customer-create.json")

        result = client.customers.create(payload)
        print_success("Customer created successfully!")
        print_result_with_file("customers_create", result)
    except Exception as e:
        print_error(str(e))

    input("\nPress Enter to continue...")
