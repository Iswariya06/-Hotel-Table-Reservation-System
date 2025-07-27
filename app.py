from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import ReservationManager, User, Table
import pickle

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Initialize Reservation Manager
reservation_manager = ReservationManager()

# Load Users from Serialized Database
try:
    with open("database.pkl", "rb") as db:
        users = pickle.load(db)
except FileNotFoundError:
    users = {"admin": {"password": "admin123", "role": "admin"}}

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', tables=reservation_manager.get_all_tables(), username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash("Username already exists")
        else:
            users[username] = {"password": password, "role": "user"}
            with open("database.pkl", "wb") as db:
                pickle.dump(users, db)
            flash("Signup successful! Please log in.")
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/reserve/<int:table_id>', methods=['GET', 'POST'])
def reserve(table_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        time_slot = request.form['time_slot']
        user = User(session['username'])
        reservation_manager.add_observer(user)  # Add observer
        success = reservation_manager.reserve_table(table_id, user, time_slot)
        if success:
            flash("Table reserved successfully!")
            return redirect(url_for('index'))
        else:
            flash("Table is already reserved or unavailable.")
            return redirect(url_for('reserve', table_id=table_id))

    return render_template('reserve.html', table_id=table_id)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('role') != 'admin':
        flash("Access denied")
        return redirect(url_for('index'))

    if request.method == 'POST':
        table_id = int(request.form['table_id'])
        reservation_manager.add_table(table_id)
        flash(f"Table {table_id} added successfully!")

    return render_template('admin.html', 
                           tables=reservation_manager.get_all_tables(),
                           reserved_tables={k: v for k, v in reservation_manager.get_all_tables().items()
                                            if isinstance(v.state)})

if __name__ == '__main__':
    app.run(debug=True)
