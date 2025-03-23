from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database Configuration
config = {
    "host": "localhost",  # Change if your MySQL server is hosted elsewhere
    "user": "your_username",
    "password": "your_password",
    "database": "your_database"
}

def get_db_connection():
    return mysql.connector.connect(**config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_message', methods=['POST'])
def add_message():
    data = request.json
    message = data.get("message")
    
    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (content) VALUES (%s)", (message,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": message})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM messages")
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify([{"id": msg[0], "content": msg[1]} for msg in messages])

@app.route('/delete_message/<int:msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE id = %s", (msg_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
