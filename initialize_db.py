import pickle

# Initial data for the database
initial_data = {
    'users': {},  # Stores users in the format {username: password}
    'tables': {},  # Stores tables in the format {table_id: Table instance}
}

# Save the initial data to the file
with open('database.pkl', 'wb') as f:
    pickle.dump(initial_data, f)

print("Database initialized!")
