# database file that creates tables and interacts with the class files when need be for queries etc.
CREATE_CPAS = """CREATE TABLE IF NOT EXISTS cpas
(id SERIAL PRIMARY KEY, name TEXT);"""

CREATE_CLIENTS = """CREATE TABLE IF NOT EXISTS clients
(id SERIAL PRIMARY KEY, name TEXT, address TEXT, income INTEGER, materials_submitted BOOLEAN DEFAULT FALSE, 
cpa_id INTEGER REFERENCES cpas(id), assistant_id INTEGER REFERENCES tax_filing_assistants(id));"""

CREATE_TAX_RETURNS = """CREATE TABLE IF NOT EXISTS tax_returns
(id SERIAL PRIMARY KEY, client_id INTEGER REFERENCES clients(id), filed_or_not BOOLEAN DEFAULT FALSE, checked_by TEXT,
tax_return_timestamp INTEGER DEFAULT NULL);"""  # add timestamp

CREATE_ASSISTANTS = """CREATE TABLE IF NOT EXISTS tax_filing_assistants
(id SERIAL PRIMARY KEY, name TEXT);"""


INSERT_CLIENT_RETURN_ID = """INSERT INTO clients (name, address, income, materials_submitted, cpa_id)
VALUES (%s, %s, %s, %s, %s) RETURNING id;"""

INSERT_CPA_RETURN_ID = "INSERT INTO cpas (name) VALUES (%s) RETURNING id;"

INSERT_ASSISTANT_RETURN_ID = "INSERT INTO tax_filing_assistants (name) VALUES (%s) RETURNING id;"

INSERT_TAX_RETURN = """INSERT INTO tax_returns (client_id, filed_or_not, checked_by, tax_return_timestamp) 
VALUES (%s, %s, %s, %s);"""

UPDATE_CLIENTS_MATERIALS = "UPDATE clients SET materials_submitted = %s WHERE name = %s;"

UPDATE_TAX_RETURN_STATUS = """UPDATE tax_returns SET filed_or_not = %s, checked_by = %s, tax_return_timestamp = %s 
WHERE client_id = %s"""

UPDATE_CLIENT_CPA = "UPDATE clients SET cpa_id = %s WHERE id = %s;"

UPDATE_CLIENT_ASSISTANT = "UPDATE clients SET assistant_id = %s WHERE id = %s;"

SELECT_CLIENT_BY_NAME = "SELECT * FROM clients WHERE LOWER(name) = LOWER(%s);"

SELECT_TAX_RETURN = "SELECT * FROM tax_returns WHERE client_id = %s;"

SELECT_CPA_BY_NAME = "SELECT * FROM cpas WHERE LOWER(name) = LOWER(%s);"

SELECT_ASSISTANT_BY_NAME = "SELECT * FROM tax_filing_assistants WHERE LOWER(name) = LOWER(%s);"

SELECT_CPA_CLIENT_RELATIONS = """SELECT cpas.name AS cpa_name, clients.name AS client_name
FROM clients
JOIN cpas ON clients.cpa_id = cpas.id;"""

SELECT_ASSISTANT_CLIENT_RELATIONS = """SELECT tax_filing_assistants.name AS assistant_name, clients.name AS client_name
FROM clients
JOIN tax_filing_assistants ON clients.assistant_id = tax_filing_assistants.id;"""

SELECT_TAX_RETURN_STATUS = """SELECT filed_or_not, checked_by, tax_return_timestamp FROM tax_returns 
WHERE client_id = %s;"""

SELECT_CLIENT_DETAILS = """SELECT clients.id, clients.name, clients.address, clients.income, 
       clients.materials_submitted, cpas.name AS cpa_name, 
       tax_filing_assistants.name AS assistant_name
FROM clients
LEFT JOIN cpas ON clients.cpa_id = cpas.id
LEFT JOIN tax_filing_assistants ON clients.assistant_id = tax_filing_assistants.id
WHERE LOWER(clients.name) = LOWER(%s);"""


def create_tables(connection):
    """
    Creates the necessary database tables if they do not already exist.
    Executes SQL commands to create the 'cpas', 'clients', 'tax_filing_assistants',
    and 'tax_returns' tables.

    Args:
        connection (psycopg2.connection): The database connection object.
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_CPAS)
            cursor.execute(CREATE_ASSISTANTS)
            cursor.execute(CREATE_CLIENTS)
            cursor.execute(CREATE_TAX_RETURNS)


def add_client(connection, client_name, address, income, materials_submitted=False, cpa_id=None):
    """
    Inserts a new client into the database and returns the generated client ID.
    Returns:
        int: The ID of the newly created client.
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_CLIENT_RETURN_ID, (client_name, address, income, materials_submitted, cpa_id))
            client_id = cursor.fetchone()[0]
            return client_id


def add_cpa(connection, cpa_name):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_CPA_RETURN_ID, (cpa_name, ))
            cpa_id = cursor.fetchone()[0]
            return cpa_id


def add_tax_filing_assistant(connection, assistant_name):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_ASSISTANT_RETURN_ID, (assistant_name, ))
            assistant_id = cursor.fetchone()[0]
            return assistant_id


def add_tax_return(connection, client_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_TAX_RETURN, (client_id, False, None, None))


def change_materials_status(connection, client_name, materials_submitted):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_CLIENTS_MATERIALS, (materials_submitted, client_name))


def change_tax_return_status(connection, client_id, filed_or_not, checked_by, tax_return_timestamp):
    """
    Updates the status of a client's tax return in the database.

    Args:
        connection (psycopg2.connection): The database connection object.
        client_id (int): The ID of the client whose tax return is being updated.
        filed_or_not (bool): Whether the tax return has been filed.
        checked_by (str): Indicates whether the return was checked by a "CPA" or "Assistant".
        tax_return_timestamp (float): The timestamp of when the tax return was filed.
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_TAX_RETURN_STATUS, (filed_or_not, checked_by, tax_return_timestamp, client_id))


def get_cpa_by_name(connection, cpa_name):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_CPA_BY_NAME, (cpa_name, ))
            return cursor.fetchone()


def get_tax_filing_assistant_by_name(connection, assistant_name):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ASSISTANT_BY_NAME, (assistant_name, ))
            return cursor.fetchone()


def get_tax_return(connection, client_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_TAX_RETURN, (client_id, ))
            return cursor.fetchone()


def get_cpa_client_relations(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_CPA_CLIENT_RELATIONS)
            return cursor.fetchall()


def get_assistant_client_relations(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ASSISTANT_CLIENT_RELATIONS)
            return cursor.fetchall()


def get_client_details(connection, client_name):
    """
    Retrieves detailed information about a client from the database.
    Returns:
        tuple: A tuple containing client details (ID, name, address, income, materials_submitted, CPA name, assistant name),
               or None if the client does not exist.
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_CLIENT_DETAILS, (client_name, ))
            return cursor.fetchone()


def check_tax_return_status(connection, client_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_TAX_RETURN_STATUS, (client_id, ))
            return cursor.fetchone()


def assign_cpa_to_client(connection, client_id, cpa_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_CLIENT_CPA, (cpa_id, client_id))


def assign_assistant_to_client(connection, client_id, assistant_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_CLIENT_ASSISTANT, (assistant_id, client_id))

