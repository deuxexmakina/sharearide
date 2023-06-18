from flask import Flask, jsonify, request
import sqlite3
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS, cross_origin
import bcrypt
from datetime import datetime


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # Allow all origins and support credentials

app.config['JWT_SECRET_KEY'] = 'group3'
jwt = JWTManager(app)
# CORS(app)


# Set up SQLite3 database
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              email TEXT NOT NULL,
              city TEXT NOT NULL,
              current_location TEXT NOT NULL,
              payment_mode TEXT NOT NULL,
              reputation INTEGER,
              violations INTEGER,
              car_type TEXT,
              seats INTEGER,
              role TEXT,
              password TEXT)''')
conn.commit()

entries = [
    ("Admin", "admin@ron.com", "New York", "Times Square", "Credit Card", 4, 2, "Sedan", 4, "admin", bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())),
    ("Driver", "driver@ron.com", "Los Angeles", "Hollywood", "PayPal", 5, 0, "SUV", 7, "driver", bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())),
    ("Rider", "rider@ron.com", "Chicago", "Downtown", "Venmo", 3, 1, "Compact", 4, "rider", bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()))
]

c.executemany("INSERT INTO users (name, email, city, current_location, payment_mode, reputation, violations, car_type, seats, role, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entries)

conn.commit()

# Create the messages table
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              date_time TEXT NOT NULL,
              message TEXT NOT NULL)''')
conn.commit()

# Create the messages table
c.execute('''CREATE TABLE IF NOT EXISTS approved_list
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              email TEXT NOT NULL)''')
conn.commit()

# Login
def authenticate(email, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[11]):
        return user
    return None


@app.route('/login', methods=['POST'])
@cross_origin()  # Allow CORS for this endpoint
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = authenticate(email, password)
    if user:
        access_token = create_access_token(identity=email)
        return jsonify({"access_token": access_token})
    return jsonify({"message": "Invalid credentials"}), 401


# View all Users
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()

    users = []
    for row in rows:
        user = {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "city": row[3],
            "current_location": row[4],
            "payment_mode": row[5],
            "reputation": row[6],
            "violations": row[7],
            "car_type": row[8],
            "seats": row[9],
            "role": row[10]
            # Removed password from the response
        }
        users.append(user)

    return jsonify(users)


# View Single User
@app.route('/users/<string:email>', methods=['GET'])
@jwt_required()
def get_user(email):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    row = c.fetchone()

    if row:
        user = {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "city": row[3],
            "current_location": row[4],
            "payment_mode": row[5],
            "reputation": row[6],
            "violations": row[7],
            "car_type": row[8],
            "seats": row[9],
            "role": row[10]
            # Removed password from the response
        }
        return jsonify(user)
    else:
        return jsonify({"message": "User not found"}), 404


# All users
@app.route('/users')
@jwt_required()
def users():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()

    users = []
    for row in rows:
        user = {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "city": row[3],
            "current_location": row[4],
            "payment_mode": row[5],
            "reputation": row[6],
            "violations": row[7],
            "car_type": row[8],
            "seats": row[9],
            "role": row[10]
            # Removed password from the response
        }
        users.append(user)

    return jsonify(users)


## Add user
@app.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    city = data['city']
    current_location = data['current_location']
    payment_mode = data['payment_mode']
    reputation = int(data['reputation'])
    violations = int(data['violations'])
    car_type = data['car_type']
    seats = int(data['seats'])
    role = data['role']
    password = data['password']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Check if email already exists in the database
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    existing_user = c.fetchone()
    if existing_user:
        return jsonify({"message": "Email already exists in the database"}), 409

    # Insert the new user into the database
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    c.execute("INSERT INTO users (name, email, city, current_location, payment_mode, reputation, violations, car_type, seats, role, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (name, email, city, current_location, payment_mode, reputation, violations, car_type, seats, role, hashed_password))
    conn.commit()

    return jsonify({"message": "User created successfully!"})


## Edit User
@app.route('/users/<string:email>', methods=['PUT'])
@jwt_required()
def update_user(email):
    data = request.get_json()
    name = data.get('name')
    city = data.get('city')
    current_location = data.get('current_location')
    payment_mode = data.get('payment_mode')
    reputation = data.get('reputation')
    violations = data.get('violations')
    car_type = data.get('car_type')
    seats = data.get('seats')
    role = data.get('role')
    password = data.get('password')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    row = c.fetchone()

    if row:
        # Update only the provided fields
        updated_fields = {}
        if name:
            updated_fields['name'] = name
        if city:
            updated_fields['city'] = city
        if current_location:
            updated_fields['current_location'] = current_location
        if payment_mode:
            updated_fields['payment_mode'] = payment_mode
        if reputation is not None:
            updated_fields['reputation'] = int(reputation)
        if violations is not None:
            updated_fields['violations'] = int(violations)
        if car_type:
            updated_fields['car_type'] = car_type
        if seats is not None:
            updated_fields['seats'] = int(seats)
        if role:
            updated_fields['role'] = role
        if password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            updated_fields['password'] = hashed_password

        # Perform the update
        update_query = "UPDATE users SET " + ", ".join([f"{key} = ?" for key in updated_fields.keys()]) + " WHERE email = ?"
        c.execute(update_query, (*updated_fields.values(), email))
        conn.commit()

        return jsonify({"message": "User updated successfully"})
    else:
        return jsonify({"message": "User not found"}), 404


## Delete User
@app.route('/users/<string:email>', methods=['DELETE'])
@jwt_required()
def delete_user(email):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    row = c.fetchone()

    if row:
        c.execute("DELETE FROM users WHERE email=?", (email,))
        conn.commit()
        return jsonify({"message": "User deleted successfully"})
    else:
        return jsonify({"message": "User not found"}), 404


# Driver Route
@app.route('/driver', methods=['GET'])
@jwt_required()
def get_drivers():
    data = request.get_json()
    city = data.get('city')
    current_location = data.get('current_location')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE role='driver' AND city=? AND current_location=?", (city, current_location))
    rows = c.fetchall()

    riders = []
    for row in rows:
        rider = {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "city": row[3],
            "current_location": row[4],
            "payment_mode": row[5],
            "reputation": row[6],
            "violations": row[7],
            "car_type": row[8],
            "seats": row[9],
            "role": row[10]
        }
        riders.append(rider)

    return jsonify(riders)

# Rider Route
@app.route('/rider', methods=['GET'])
@jwt_required()
def get_riders():
    data = request.get_json()
    city = data.get('city')
    current_location = data.get('current_location')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE role='rider' AND city=? AND current_location=?", (city, current_location))
    rows = c.fetchall()

    riders = []
    for row in rows:
        rider = {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "city": row[3],
            "current_location": row[4],
            "payment_mode": row[5],
            "reputation": row[6],
            "violations": row[7],
            "car_type": row[8],
            "seats": row[9],
            "role": row[10]
        }
        riders.append(rider)

    return jsonify(riders)


# Add comment
@app.route('/comments', methods=['POST'])
@jwt_required()
def add_comment():
    data = request.get_json()
    name = get_jwt_identity()  # Get the current user's name from the JWT token
    message = data.get('message')
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current date and time

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Insert the comment into the database
    c.execute("INSERT INTO messages (name, date_time, message) VALUES (?, ?, ?)",
              (name, date_time, message))
    conn.commit()

    return jsonify({"message": "Comment added successfully!"})


# View all comments
@app.route('/comments', methods=['GET'])
@jwt_required()
def view_all_comments():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM messages")
    rows = c.fetchall()

    comments = []
    for row in rows:
        comment = {
            "id": row[0],
            "name": row[1],
            "date_time": row[2],
            "message": row[3]
        }
        comments.append(comment)

    return jsonify(comments)


# Add email to approved list
@app.route('/add_email', methods=['POST'])
@jwt_required()
def add_email():
    data = request.get_json()
    email = data.get('email')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Insert the email into the approved_list table
    c.execute("INSERT INTO approved_list (email) VALUES (?)", (email,))
    conn.commit()

    return jsonify({"message": "Email added to the approved list!"})


# Delete email from approved list
@app.route('/delete_email/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_email(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Get the email based on the provided ID
    c.execute("SELECT * FROM approved_list WHERE id=?", (id,))
    row = c.fetchone()

    if row:
        c.execute("DELETE FROM approved_list WHERE id=?", (id,))
        conn.commit()
        return jsonify({"message": "Email deleted from the approved list"})
    else:
        return jsonify({"message": "Email not found"}), 404


# View all emails in approved list
@app.route('/approved_list', methods=['GET'])
@jwt_required()
def view_approved_list():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM approved_list")
    rows = c.fetchall()

    emails = []
    for row in rows:
        email = {
            "id": row[0],
            "email": row[1]
        }
        emails.append(email)

    return jsonify(emails)


@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    city = data['city']
    current_location = data['current_location']
    payment_mode = data['payment_mode']
    reputation = int(data['reputation'])
    violations = int(data['violations'])
    car_type = data['car_type']
    seats = int(data['seats'])
    role = data['role']
    password = data['password']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Check if email exists in the approved list
    c.execute("SELECT * FROM approved_list WHERE email=?", (email,))
    approved_user = c.fetchone()
    if not approved_user:
        return jsonify({"message": "Email not approved. User registration not allowed."}), 403

    # Check if email already exists in the database
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    existing_user = c.fetchone()
    if existing_user:
        return jsonify({"message": "Email already exists in the database"}), 409

    # Insert the new user into the database
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    c.execute("INSERT INTO users (name, email, city, current_location, payment_mode, reputation, violations, car_type, seats, role, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (name, email, city, current_location, payment_mode, reputation, violations, car_type, seats, role, hashed_password))
    conn.commit()

    return jsonify({"message": "User created successfully!"})


@app.route('/')
def hello_world():
    return jsonify({"message": "Hello, World!"})

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"message": "This is a protected route."})



if __name__ == '__main__':
    # app.run()
    app.run(host="0.0.0.0", port=5000)