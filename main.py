# main function that prompts user for an action they would like to execute.
import datetime

import pytz

import database
from classes.Client import Client
from classes.CPA import CPA
from classes.TaxFilingAssistant import TaxFilingAssistant
from classes.TaxReturn import TaxReturn
from connection_pool import get_connection

DATABASE_PROMPT = "Enter the DATABASE_URL value or leave empty to load from .env file: "
MENU_PROMPT = """-- Menu --

1) Add new client
2) Add new cpa
3) Add new tax filing assistant
4) Mark client materials as submitted
5) Check status of client's materials
6) Create a tax return file for a client
7) Mark a client's tax return as filed
8) Check the status of a client's tax return
9) Assign a cpa to a client
10) Display all cpa-client relationships
11) Assign an assistant to a client
12) Display all assistant-client relationships
13) Get client details
14) Exit

Enter your choice: """
NEW_OPTION_PROMPT = "Enter new option text (or leave empty to stop adding options): "


def prompt_add_client():
    """
    Prompts the user to add a new client to the database.
    Collects the client's name, address, and income from user input, validates
    the inputs, and saves the client to the database.
    """
    client_name = get_name("Enter client's name: ")
    client_address = get_name("Enter client's address: ")
    while True:
        try:
            client_income = input("Enter client's income: ").strip()
            client_income = float(client_income)
            if client_income < 0:
                print("Income cannot be negative. Please enter a valid number.")
            else:
                break
        except ValueError:
            print("Inputted income is not valid. Enter a numeric value.")
    client = Client(name=client_name, address=client_address, income=client_income)
    client.save()


def prompt_add_cpa():
    cpa_name = get_name("Enter CPA's name: ")
    cpa = CPA(name=cpa_name)
    cpa.save()


def prompt_add_tax_filing_assistant():
    assistant_name = get_name("Enter Tax Filing Assistant's name: ")
    assistant = TaxFilingAssistant(name=assistant_name)
    assistant.save()


def prompt_mark_materials_submitted():
    """
    Marks a client's materials as submitted.
    Prompts the user for a client's name, retrieves the corresponding client
    from the database, and updates the materials submission status.
    """
    client_name = input("What is the name of the client? ")
    client = Client.get(client_name)
    if not client:
        print("There is no client with that name in the database.")
        return
    client.mark_materials_submitted()


def prompt_add_tax_return():
    """
    add a tax return file for a client so that it can be marked as filed by another function below.
    """
    client_name = input("Enter the name of the client to create a tax return for: ")
    client = Client.get(client_name)
    if not client:
        print("There is no client with that name in the database.")
        return
    if TaxReturn.get(client._id):
        print("A tax return already exists for that client.")
        return
    TaxReturn.create(client)


def prompt_check_materials():
    client_name = input("What is the name of the client? ")
    client = Client.get(client_name)
    if not client:
        print("There is no client with that name in the database.")
        return
    if client.materials_status():
        print("This client's materials have been submitted.")
    else:
        print("This client's materials have not been submitted.")


def prompt_mark_tax_return():
    """
    Marks a client's tax return as filed.
    Prompts the user for the client's name and determines whether the tax return
    was filed by a CPA or a Tax Filing Assistant. Updates the database accordingly.
    Prints messages if the client or tax return does not exist or if the input is invalid.
    """
    client_name = input("What is the client's name? ")
    client = Client.get(client_name)
    if not client:
        print("There is no client with that name in the database.")
        return

    tax_return = TaxReturn.get(client._id)
    if not tax_return:
        print("There is no tax return file for this client. Please create one first")
        return

    print("Who is filing the return?")
    print("1) CPA")
    print("2) Tax Filing Assistant")
    choice = input("choice: ")

    if choice == "1":
        tax_return.mark_filed("CPA")
    elif choice == "2":
        tax_return.mark_filed("Assistant")
    else:
        print("Invalid. Please enter 1 or 2.")
        return


def prompt_assign_cpa():
    # assign cpa to a client
    client_name = input("What is the client's name? ")
    client = Client.get(client_name)
    if not client:
        print("There is no client with that name in the database.")
        return
    cpa_name = input("Enter the name of the CPA: ")
    cpa = CPA.get(cpa_name)
    if not cpa:
        print("There is no CPA with that name.")
        return
    client.assign_cpa(cpa._id)
    print(f"Assigned CPA '{cpa_name}' to {client_name}.")


def prompt_assign_assistant():
    # assign assistant to a client
    client_name = input("What is the client's name? ")
    client = Client.get(client_name)
    if not client:
        print("There is no client with that name in the database.")
        return
    assistant_name = input("Enter the name of the assistant: ")
    assistant = TaxFilingAssistant.get(assistant_name)
    if not assistant:
        print("There is no assistant with that name.")
        return
    client.assign_assistant(assistant._id)


def prompt_check_tax_return_status():
    """
    Checks and displays the status of a client's tax return.
    Prompts the user for the client's name, retrieves the tax return status
    from the database, and displays whether it has been filed, by whom, and when.
    """
    client_name = input("What is the client's name? ")
    client = Client.get(client_name)
    if not client:
        print("There is no client with that name in the database.")
        return
    status = TaxReturn.is_filed(client._id)
    if not status:
        print("There is no tax return file for this client. Please create one first")
        return

    if status["filed"]:
        if status["checked_by"] == "yes":
            filed_by = "a CPA"
        else:
            filed_by = "a tax filing assistant"
        time_filed_utc = datetime.datetime.fromtimestamp(status["tax_return_timestamp"], tz=pytz.utc)
        time_filed_eastern_us = time_filed_utc.astimezone(pytz.timezone("US/Eastern"))
        filed_time_str = time_filed_eastern_us.strftime("%Y-%m-%d %I:%M:%S %p %Z")
        print(f"{client_name.title()}'s tax return was filed by {filed_by} on {filed_time_str}.")
    else:
        print(f"{client_name.title()}'s tax return has not been filed.")


def prompt_get_client_details():
    # get all client details by name
    client_name = input("What is the client's name? ")
    client = Client.get(client_name)
    if not client:
        print("There is no client with that name in the database.")
        return
    print("--- Client Details ---")
    print(client)


def print_cpa_client_relations():
    relations = CPA.get_client_relations()
    relations = sorted(relations, key=lambda x: x["cpa_name"].lower())
    print("--- CPA-Client Relations ---")
    for relation in relations:
        print(f"CPA: {relation['cpa_name']} | Client: {relation['client_name']}")


def print_assistant_client_relations():
    relations = TaxFilingAssistant.get_client_relations()
    relations = sorted(relations, key=lambda x: x["assistant_name"].lower())
    print("--- Assistant-Client Relations ---")
    for relation in relations:
        print(f"Assistant: {relation['assistant_name']} | Client: {relation['client_name']}")


def get_name(prompt):
    """
    Prompts the user for a non-empty string input.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        str: The non-empty string input provided by the user.
    """
    while True:
        name = input(prompt).strip()
        if not name:
            print("Input cannot be empty. Try again.")
        else:
            return name


MENU_OPTIONS = {
    "1": prompt_add_client,
    "2": prompt_add_cpa,
    "3": prompt_add_tax_filing_assistant,
    "4": prompt_mark_materials_submitted,
    "5": prompt_check_materials,
    "6": prompt_add_tax_return,
    "7": prompt_mark_tax_return,
    "8": prompt_check_tax_return_status,
    "9": prompt_assign_cpa,
    "10": print_cpa_client_relations,
    "11": prompt_assign_assistant,
    "12": print_assistant_client_relations,
    "13": prompt_get_client_details,
}


def menu():
    """
    Initializes the database connection, creates necessary tables, and
    processes user inputs to execute the corresponding actions.
    """
    with get_connection() as connection:
        database.create_tables(connection)
    while (selection := input(MENU_PROMPT)) != "14":
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print("Invalid input selected. Please try again.")


if __name__ == "__main__":
    menu()