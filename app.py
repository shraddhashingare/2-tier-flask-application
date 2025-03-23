from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connect to the MySQL Database
def get_db_connection():
    return mysql.connector.connect(
        host="your_mysql_host",  # e.g., "localhost"
        user="your_mysql_user",  # e.g., "root"
        password="your_mysql_password",  # your MySQL password
        database="your_database"  # name of the database
    )

# Route to display the messages and the form
@app.route("/", methods=["GET", "POST"])
def index():
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Handle the form submission
    if request.method == "POST":
        message = request.form['message']
        
        # Insert the new message into the database
        cursor.execute("INSERT INTO messages (message) VALUES (%s)", (message,))
        conn.commit()
        return redirect("/")

    # Retrieve all messages from the database
    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
