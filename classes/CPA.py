import database
from connection_pool import get_connection


class CPA:
    """
    Represents a Certified Public Accountant
    """
    def __init__(self, name, _id=None):
        self._id = _id
        self.name = name

    def save(self):
        """
        Saves the CPA to the database. Inserts the CPA's details into the database and updates the `_id`
        attribute with the generated ID.
        """
        with get_connection() as connection:
            cpa_id = database.add_cpa(connection, self.name)
            self._id = cpa_id

    @classmethod
    def get(cls, name):
        """
        Retrieves a CPA from the database by name.
        Returns:
            CPA or None: An instance of the `CPA` class if a matching CPA is found,
            otherwise `None`.
        """
        with get_connection() as connection:
            cpa_row = database.get_cpa_by_name(connection, name)
            if cpa_row:
                return cls(name=cpa_row[1], _id=cpa_row[0])
            return None

    @classmethod
    def get_client_relations(cls):
        """
            Retrieves all relationships between CPAs and clients from the database.
            Returns:
                list of dict: A list of dictionaries where each dictionary contains
                'cpa_name' and 'client_name' representing a CPA-client relationship.
        """
        with get_connection() as connection:
            relations = database.get_cpa_client_relations(connection)
            return [{"cpa_name": relation[0], "client_name": relation[1]} for relation in relations]