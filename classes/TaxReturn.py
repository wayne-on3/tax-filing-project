import datetime
import pytz as pytz
import database
from connection_pool import get_connection


class TaxReturn:
    """
    Represents a tax return for a client.
    """
    def __init__(self, client_id, filed_or_not=False, checked_by=None, tax_return_timestamp=None, _id=None):
        self._id = _id
        self.client_id = client_id
        self.filed_or_not = filed_or_not
        self.checked_by = checked_by
        self.tax_return_timestamp = tax_return_timestamp

    def mark_filed(self, filed_by):
        """
            Marks the tax return as filed and records who filed it.
            Updates the `filed_or_not` attribute to `True`, sets the `checked_by`
            attribute to indicate whether the return was filed by a CPA or an assistant,
            and records the timestamp of the filing.
        """
        self.filed_or_not = True
        if filed_by == "CPA":
            self.checked_by = "yes"
        else:
            self.checked_by = "no"
        with get_connection() as connection:
            current_datetime_utc = datetime.datetime.now(tz=pytz.utc)
            current_timestamp = current_datetime_utc.timestamp()
            database.change_tax_return_status(connection, self.client_id, self.filed_or_not, self.checked_by, current_timestamp)

    @classmethod
    def get(cls, client_id):
        """
            Retrieves a tax return from the database based on the client's ID.
            Returns:
                TaxReturn or None: An instance of the `TaxReturn` class if a matching
                tax return is found, otherwise `None`.
        """
        with get_connection() as connection:
            tax_return_info = database.get_tax_return(connection, client_id)
            if tax_return_info:
                return cls(
                    client_id=tax_return_info[1],
                    filed_or_not=tax_return_info[2],
                    checked_by=tax_return_info[3],
                    tax_return_timestamp=tax_return_info[4],
                    _id=tax_return_info[0],
                )
            return None

    @classmethod
    def create(cls, client):
        with get_connection() as connection:
            database.add_tax_return(connection, client._id)
        return cls(client_id=client._id)

    @classmethod
    def is_filed(cls, client_id):
        """
            Checks whether a tax return has been filed for a specific client.
            Returns:
                dict or None: A dictionary containing the filing status (`filed`),
                who checked it (`checked_by`), and the filing timestamp
                (`tax_return_timestamp`), or `None` if no tax return is found.
        """
        with get_connection() as connection:
            status = database.check_tax_return_status(connection, client_id)
            if status:
                return {"filed": status[0], "checked_by": status[1], "tax_return_timestamp": status[2]}
            return None

