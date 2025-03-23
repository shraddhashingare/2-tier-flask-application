from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database Configuration
config = {
    "host": "localhost",  # Change if your MySQL server is hosted elsewhere
    "user": "your_username",  # Update with your MySQL username
    "password": "your_password",  # Update with your MySQL password
    "database": "your_database"  # Update with your MySQL database name
}

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**config)

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/add_message', methods=['POST'])
def add_message():
    """Handles adding a new message to the database."""
    data = request.json
    message = data.get("message")
    
    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (content) VALUES (%s)", (message,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": message})
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route('/get_messages', methods=['GET'])
def get_messages():
    """Retrieves all messages from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, content FROM messages")
        messages = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([{"id": msg[0], "content": msg[1]} for msg in messages])
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route('/delete_message/<int:msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    """Deletes a message by its ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE id = %s", (msg_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Deleted successfully"})
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
