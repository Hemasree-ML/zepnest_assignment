from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Govindahema@123",
    database="zepnest"
)

# Home Route
@app.route("/")
def home():
    return "Backend working successfully"


# Register
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    name = data["name"]
    email = data["email"]
    password = data["password"]

    cursor = db.cursor()

    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, password))

    db.commit()

    return jsonify({"message": "User registered successfully"})


# Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    email = data["email"]
    password = data["password"]

    cursor = db.cursor(dictionary=True)

    sql = "SELECT * FROM users WHERE email=%s AND password=%s"
    cursor.execute(sql, (email, password))

    user = cursor.fetchone()

    if user:
        return jsonify({
            "message": "Login successful",
            "user": user
        })
    else:
        return jsonify({
            "message": "Invalid credentials"
        }), 401


# Get Users
@app.route("/users", methods=["GET"])
def get_users():
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    return jsonify(users)


# Create Request
@app.route("/requests", methods=["POST"])
def create_request():
    data = request.json

    cursor = db.cursor()

    sql = """
    INSERT INTO requests
    (user_id, title, description, category, address, preferred_time, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data["user_id"],
        data["title"],
        data["description"],
        data["category"],
        data["address"],
        data["preferred_time"],
        "Pending"
    )

    cursor.execute(sql, values)
    db.commit()

    return jsonify({"message": "Request created successfully"})


# Get Requests
@app.route("/requests", methods=["GET"])
def get_requests():
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM requests")
    requests = cursor.fetchall()

    return jsonify(requests)


# Update Request
@app.route("/requests/<int:id>", methods=["PUT"])
def update_request(id):
    data = request.json

    cursor = db.cursor()

    sql = "UPDATE requests SET status=%s WHERE id=%s"
    cursor.execute(sql, (data["status"], id))

    db.commit()

    return jsonify({"message": "Request updated successfully"})


# Delete Request
@app.route("/requests/<int:id>", methods=["DELETE"])
def delete_request(id):
    cursor = db.cursor()

    sql = "DELETE FROM requests WHERE id=%s"
    cursor.execute(sql, (id,))

    db.commit()

    return jsonify({"message": "Request deleted successfully"})


if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)