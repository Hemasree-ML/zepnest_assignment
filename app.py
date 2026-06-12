# 1. IMPORTS (top)
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

# 2. APP SETUP
app = Flask(__name__)
CORS(app)

# 3. DB CONNECTION
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Govindahema@123",
        database="zepnest"
    )

# 4. OLD ROUTES
@app.route("/")
def home():
    return "Backend Working Successfully"

@app.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return "DB Connected Successfully"
    except Exception as e:
        return str(e)

# 5. NEW CODE (REGISTER API) 👇 ADD HERE
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    name = data[""]
    email = data[""]
    password = data[""]

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, email, password))

        conn.commit()
        conn.close()

        return jsonify({"message": "User registered successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

# 6. RUN SERVER (bottom)
if __name__ == "__main__":
    app.run(debug=True)