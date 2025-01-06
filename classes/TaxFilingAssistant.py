import database
from connection_pool import get_connection


class TaxFilingAssistant:
    def __init__(self, name, _id=None):
        self._id = _id
        self.name = name

    def save(self):
        with get_connection() as connection:
            assistant_id = database.add_tax_filing_assistant(connection, self.name)
            self._id = assistant_id

    @classmethod
    def get(cls, name):
        with get_connection() as connection:
            assistant_row = database.get_tax_filing_assistant_by_name(connection, name)
            if assistant_row:
                return cls(name=assistant_row[1], _id=assistant_row[0])
            return None

    @classmethod
    def get_client_relations(cls):
        """
            Retrieves all relationships between Tax Filing Assistants and clients from the database.
            Returns:
                list of dict: A list of dictionaries where each dictionary contains
                'assistant_name' and 'client_name' representing an assistant-client relationship.
        """
        with get_connection() as connection:
            relations = database.get_assistant_client_relations(connection)
            return [{"assistant_name": relation[0], "client_name": relation[1]} for relation in relations]
