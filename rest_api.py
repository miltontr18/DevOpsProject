from flask import Flask, request
import db_connector  # Import the database connector module
import datetime

app = Flask(__name__)  # Creates a Flask app instance

@app.route('/')
def index():
    return 'Click here for Rest API: <a href="http://127.0.0.1:5000/users/">http://127.0.0.1:5000/users/</a>'

@app.route('/users/<user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])  # Define the route for users, accepting listed HTTP methods
def users(user_id):
    """Handle requests based on method"""
    conn = db_connector.mysql_users()  # database connection
    if conn is None:  # Check if the connection was successful
        return {'error': 'Database connection failed'}, 500  # Return an error response if connection fails

    try:  # Use a try-finally block to ensure the connection is closed
        if request.method == 'GET':  # Handle GET requests
            return get_user(conn, user_id)
        elif request.method == 'POST':
            return create_user(conn, user_id)
        elif request.method == 'PUT':
            return update_user(conn, user_id)
        elif request.method == 'DELETE':
            return delete_user(conn, user_id)
    finally:
        conn.close()  # Closes db connection

# Defining the get user function
def get_user(conn, user_id):
    cursor = conn.cursor()  # Creating a database cursor
    try:
        db_user = f"SELECT user_name FROM users WHERE user_id = {user_id}"  # SQL query to select user name
        cursor.execute(db_user)  # Executing the query
        result = cursor.fetchone()  # Fetching the result

        if result:  # Checking if a user was found
            return {'status': "ok", 'user_name': result[0]}, 200  # Returning the user name
        else:
            return {'status': "500: error", 'reason': "no such id"}, 500  # Return an error if user not found
    finally:
        cursor.close()  # Closing the cursor


def create_user(conn, user_id):
    date = datetime.datetime.now() # Calling datetime
    date = date.strftime("%d-%m-%Y") # formatting date
    request_user = request.get_json()  # Getting the JSON data from the request
    if not request_user or not request_user.get('user_name'):  # Checking if user_name is provided
        return {'error': 'Missing required field: user_name'}, 400  # Returning an error if user_name is missing

    user_name = request_user['user_name']  # Extracting the user name
    creation_date = date
    cursor = conn.cursor()  # Creating a database cursor
    try:
        db_user = f"SELECT * FROM users WHERE user_id = {user_id}"  # Checking if the user_id already exists
        cursor.execute(db_user)  # Execute the query
        existing_user = cursor.fetchone()  # Fetch the result

        if existing_user:  # Checking if a user with that ID already exists
            return {'status': "error", 'reason': "id already exists"}, 409  # Return an error if user_id exists

        db_user = "INSERT INTO users (user_id, user_name, creation_date) VALUES (%s, %s, %s)"  # SQL query to insert a new user
        cursor.execute(db_user, (user_id, user_name, creation_date))  # Executing the insert query
        return {'status': "ok", 'user_added': user_name}, 200
    finally:
        cursor.close()  # Close the cursor

# def create_user(conn, user_id):  # create_user function (with auto-incrementing ID)
#     """Creates a new user in the database, allocating a new user_id if needed."""
#     date = datetime.datetime.now()
#     date = date.strftime("%d-%m-%Y")
#     if not request_user or not request_user.get('user_name'):  # Check for user_name
#         return {'error': 'Missing required field: user_name'}, 400
#
#     user_name = request_user['user_name']  # Get user name
#     creation_date = date
#
#     cursor = conn.cursor()  # Create cursor
#     try:
#         # Find the highest existing user_id (or start at 1 if no users)
#         cursor.execute("SELECT MAX(user_id) FROM users")
#         result = cursor.fetchone()  # Fetch the result
#         if result[0] is None:  # No users yet
#             user_id = 1  # Start at 1
#         else:
#             user_id = int(result[0]) + 1  # Increment the max id
#
#         db_user = "INSERT INTO users (user_id, user_name, creation_date) VALUES (%s, %s, %s)"  # Inserting new user
#         cursor.execute(db_user, (user_id, user_name, creation_date))  # Executing query
#         conn.commit()
#         return {'status': "ok", 'user_added': user_name, 'user_id': user_id}, 200
#     finally:
#         cursor.close()  # Close cursor

def update_user(conn, user_id):
    request_user = request.get_json()  # Getting the JSON data from the request
    if not request_user or not request_user.get('user_name'):  # Checking if user_name is provided
        return {'error': 'Missing required field: user_name'}, 400

    user_name = request_user['user_name']  # Extracting the user name
    cursor = conn.cursor()  # Creating a database cursor
    try:
        db_user = "SELECT * FROM users WHERE user_id = %s"  # Checking if the user exists
        cursor.execute(db_user, (user_id,))  # Executing the query
        existing_user = cursor.fetchone()  # Fetching the result

        if not existing_user:  # Checking if the user exists
            return {'status': "error", 'reason': "no such id"}, 500  # Return an error if user not found

        db_user = "UPDATE users SET user_name = %s WHERE user_id = %s"  # updating the user
        cursor.execute(db_user, (user_name, user_id))  # Executing the update query
        return {'status': "ok", 'user_updated': user_name}, 200
    finally:
        cursor.close()


def delete_user(conn, user_id):  # Function to delete a user
    cursor = conn.cursor()
    try:
        user_in_db = "DELETE FROM users WHERE user_id = %s"
        cursor.execute(user_in_db, (user_id,))

        cursor.execute("SELECT FOUND_ROWS()")
        rows_deleted = cursor.fetchone()[0]

        if rows_deleted == 0:
            return {'status': "error", 'reason': "no such id"}, 500
        else:
            return {'status': "ok", 'user_deleted': user_id}, 200
    finally:
        cursor.close()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)