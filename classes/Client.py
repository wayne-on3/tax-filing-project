import database
from connection_pool import get_connection


class Client:
    """
    Represents a client in the tax filing system.
    """
    def __init__(self, name, address, income, materials_submitted=False, cpa=None, assistant=None, _id=None):
        self._id = _id
        self.name = name
        self.address = address
        self.income = income
        self.materials_submitted = materials_submitted
        self.cpa = cpa
        self.assistant = assistant

    def __str__(self):
        # used to print the client instances in a readable, relevant way
        cpa_association = f"CPA: {self.cpa}" if self.cpa else "CPA: None"
        assistant_association = f"Assistant: {self.assistant}" if self.assistant else "Assistant: None"
        return (
            f"Client ID: {self._id}\n"
            f"Name: {self.name}\n"
            f"Address: {self.address}\n"
            f"Income: ${self.income:,}\n"
            f"{cpa_association}\n"
            f"{assistant_association}"
        )

    def save(self):
        """
        Represents a client in the tax filing system.
        Inserts the client's details into the database and updates the `_id`
        attribute with the generated ID.
        """
        with get_connection() as connection:
            new_client_id = database.add_client(connection, self.name, self.address, self.income)
            self._id = new_client_id

    def mark_materials_submitted(self):
        """
        Marks the client's materials as submitted.
        Updates the `materials_submitted` attribute to `True` and reflects the change
        in the database.
        """
        self.materials_submitted = True
        with get_connection() as connection:
            database.change_materials_status(connection, self.name, self.materials_submitted)

    def assign_cpa(self, cpa_id):
        """Assigns a CPA to the client.
        Updates the `cpa_id` for the client in the database to associate the client
        with the given CPA.
        """
        with get_connection() as connection:
            database.assign_cpa_to_client(connection, self._id, cpa_id)

    def assign_assistant(self, assistant_id):
        with get_connection() as connection:
            database.assign_assistant_to_client(connection, self._id, assistant_id)

    def materials_status(self):
        # check if client has submitted their materials
        return self.materials_submitted

    @classmethod
    def get(cls, name):
        """
        Retrieves a client from the database by name.
        Args:
            name (str): The name of the client to retrieve.
        Returns:
            Client or None: An instance of the `Client` class if a matching client is found,
            otherwise `None`.
        """
        with get_connection() as connection:
            client_row = database.get_client_details(connection, name)
            if client_row:
                return cls(
                    name=client_row[1], address=client_row[2], income=client_row[3], materials_submitted=client_row[4],
                    cpa=client_row[5], assistant=client_row[6], _id=client_row[0]
                )
            return None

