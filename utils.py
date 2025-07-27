import pickle

DATABASE_FILE = 'database.pkl'


def load_database():
    """Loads the database from the pickle file."""
    try:
        with open(DATABASE_FILE, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {'users': {}, 'tables': {}}


def save_database(data):
    """Saves the updated database back to the pickle file."""
    with open(DATABASE_FILE, 'wb') as f:
        pickle.dump(data, f)


def add_user(username, password):
    """Adds a new user to the database."""
    db = load_database()
    if username in db['users']:
        raise ValueError("User already exists.")
    db['users'][username] = password
    save_database(db)


def authenticate_user(username, password):
    """Authenticates a user."""
    db = load_database()
    return db['users'].get(username) == password


def add_table(table_id, table):
    """Adds a new table to the database."""
    db = load_database()
    if table_id in db['tables']:
        raise ValueError("Table ID already exists.")
    db['tables'][table_id] = table
    save_database(db)


def get_tables():
    """Retrieves all tables from the database."""
    db = load_database()
    return db['tables']


def update_table(table_id, updated_table):
    """Updates a table in the database."""
    db = load_database()
    if table_id not in db['tables']:
        raise ValueError("Table not found.")
    db['tables'][table_id] = updated_table
    save_database(db)
