# tax-filing-project
A Python application for managing tax filings and client relationships.
The application manages tax filing processes, client records, and CPA/Assistant relationships. This project showcases skills in Python, SQL, database integration, and building user-friendly command-line applications.

## Features
- **Client Management**:
  - Add, update, and manage client records, including names, addresses, and income details.
  - Check the status of submitted materials for each client.

- **CPA and Assistant Assignment**:
  - Assign Certified Public Accountants (CPAs) to clients to manage their tax filings.
  - Assign Tax Filing Assistants to support clients and CPAs in preparing tax returns.

- **Tax Filing Workflow**:
  - Track the status of tax returns, including whether they have been filed and by whom (CPA or assistant).
  - Mark tax returns as filed and record timestamps for filing.

- **Database Integration**:
  - Uses PostgreSQL to store and manage client, CPA, assistant, and tax return data.
  - Automatically creates necessary database tables on first run.

- **Role-Based Operations**:
  - Enable CPAs and assistants to perform specific tasks based on their roles.

- **Command-Line Interface**:
  - User-friendly menu system for navigating and interacting with the application.

## Requirements
- Python 3.8+
- PostgreSQL
- Required Python packages (see `requirements.txt`)

## Usage
1. **Start the Application**:
   - Run the following command to launch the application:
     ```bash
     python main.py
     ```

2. **Navigate Through the Menu**:
   - The application will display a menu with various options. Simply enter the number corresponding to the action you'd like to perform:
     -- Menu --
     1) Add new client
     2) Add new CPA
     3) Add new tax filing assistant
     4) Mark client materials as submitted
     5) Check status of client's materials
     6) Create a tax return file for a client
     7) Mark a client's tax return as filed
     8) Check the status of a client's tax return
     9) Assign a CPA to a client
     10) Display all CPA-client relationships
     11) Assign an assistant to a client
     12) Display all assistant-client relationships
     13) Get client details
     14) Exit

3. **Perform Operations**:
   - Examples of operations you can perform:
     - **Add a Client**:
       - Enter the client's name, address, and income when prompted.
     - **Mark Materials as Submitted**:
       - Choose the client and update their status.
     - **Track Tax Returns**:
       - View the filing status and timestamps for a client’s tax return.
     - **Assign Roles**:
       - Assign CPAs and assistants to specific clients.
     - **Retrieve Client Details**:
       - Display all relevant information about a specific client.

4. **Exit the Application**:
   - To exit, select option `14` from the menu.

