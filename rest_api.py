from flask import Flask, request
import db_connector  # Import the database connector module

app = Flask(__name__)  # Creates a Flask app instance

@app.route('/')
def index():
    return 'Click here for Rest API: <a href="http://127.0.0.1:5000/users/">http://127.0.0.1:5000/users/</a>'

@app.route('/users/<user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])  # Define the route for users, accepting various HTTP methods
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


def get_user(conn, user_id):  # Function to retrieve a user
    cursor = conn.cursor()  # Create a database cursor
    try:
        db_user = "SELECT user_name FROM users WHERE user_id = %s"  # SQL query to select user name
        cursor.execute(db_user, (user_id,))  # Execute the query
        result = cursor.fetchone()  # Fetch the result

        if result:  # Check if a user was found
            return {'status': "ok", 'user_name': result[0]}, 200  # Return the user name
        else:
            return {'status': "error", 'reason': "no such id"}, 500  # Return an error if user not found
    finally:
        cursor.close()  # Close the cursor


def create_user(conn, user_id):
    request_data = request.get_json()  # Get the JSON data from the request
    if not request_data or not request_data.get('user_name'):  # Check if user_name is provided
        return {'error': 'Missing required field: user_name'}, 400  # Return an error if user_name is missing

    user_name = request_data['user_name']  # Extract the user name

    cursor = conn.cursor()  # Create a database cursor
    try:
        db_user = "SELECT * FROM users WHERE user_id = %s"  # Check if the user_id already exists
        cursor.execute(db_user, (user_id,))  # Execute the query
        existing_user = cursor.fetchone()  # Fetch the result

        if existing_user:  # Check if a user with that ID already exists
            return {'status': "error", 'reason': "id already exists"}, 409  # Return an error if user_id exists

        db_user = "INSERT INTO users (user_id, user_name) VALUES (%s, %s)"  # SQL query to insert a new user
        cursor.execute(db_user, (user_id, user_name))  # Execute the insert query
        return {'status': "ok", 'user_added': user_name}, 200
    finally:
        cursor.close()  # Close the cursor


def update_user(conn, user_id):
    request_data = request.get_json()  # Get the JSON data from the request
    if not request_data or not request_data.get('user_name'):  # Check if user_name is provided
        return {'error': 'Missing required field: user_name'}, 400

    user_name = request_data['user_name']  # Extract the user name

    cursor = conn.cursor()  # Create a database cursor
    try:
        db_user = "SELECT * FROM users WHERE user_id = %s"  # Check if the user exists
        cursor.execute(db_user, (user_id,))  # Execute the query
        existing_user = cursor.fetchone()  # Fetch the result

        if not existing_user:  # Check if the user exists
            return {'status': "error", 'reason': "no such id"}, 500  # Return an error if user not found

        db_user = "UPDATE users SET user_name = %s WHERE user_id = %s"  # SQL query to update the user
        cursor.execute(db_user, (user_name, user_id))  # Execute the update query
        return {'status': "ok", 'user_updated': user_name}, 200
    finally:
        cursor.close()  # Close the cursor


def delete_user(conn, user_id):  # Function to delete a user
    cursor = conn.cursor()  # Create a database cursor
    try:
        sql = "DELETE FROM users WHERE user_id = %s"  # SQL query to delete the user
        cursor.execute(sql, (user_id,))  # Execute the delete query

        cursor.execute("SELECT FOUND_ROWS()")  # Get the number of rows deleted
        rows_deleted = cursor.fetchone()[0]  # Fetch the result

        if rows_deleted == 0:  # Check if any rows were deleted
            return {'status': "error", 'reason': "no such id"}, 500  # Return an error if user not found
        else:
            return {'status': "ok", 'user_deleted': user_id}, 200  # Return success message
    finally:
        cursor.close()  # Close the cursor

# from flask import Flask, request, jsonify
# import db_connector  # Import the database connector module
#
# app = Flask(__name__)  # Creates a Flask app instance
#
# @app.route('/')
# def index():
#     return 'Click here for Rest API: <a href="http://127.0.0.1:5000/users/">http://127.0.0.1:5000/users/</a>'
#
# @app.route('/users/<user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])  # Define the route for users, accepting various HTTP methods
# def users(user_id):
#     """Handle requests based on method"""
#     conn = db_connector.mysql_users()  # database connection
#     if conn is None:  # Check if the connection was successful
#         return jsonify({'error': 'Database connection failed'}), 500  # Return an error response if connection fails
#
#     try:  # Use a try-finally block to ensure the connection is closed
#         if request.method == 'GET':  # Handle GET requests
#             return get_user(conn, user_id)
#         elif request.method == 'POST':
#             return create_user(conn, user_id)
#         elif request.method == 'PUT':
#             return update_user(conn, user_id)
#         elif request.method == 'DELETE':
#             return delete_user(conn, user_id)
#     finally:
#         conn.close()  # Closes db connection
#
#
# def get_user(conn, user_id):  # Function to retrieve a user
#     cursor = conn.cursor()  # Create a database cursor
#     try:
#         db_user = "SELECT user_name FROM users WHERE user_id = %s"  # SQL query to select user name
#         cursor.execute(db_user, (user_id,))  # Execute the query
#         result = cursor.fetchone()  # Fetch the result
#
#         if result:  # Check if a user was found
#             return jsonify({'status': "ok", 'user_name': result[0]}), 200  # Return the user name
#         else:
#             return jsonify({'status': "error", 'reason': "no such id"}), 500  # Return an error if user not found
#     finally:
#         cursor.close()  # Close the cursor
#
#
# def create_user(conn, user_id):
#     request_data = request.get_json()  # Get the JSON data from the request
#     if not request_data or not request_data.get('user_name'):  # Check if user_name is provided
#         return jsonify({'error': 'Missing required field: user_name'}), 400  # Return an error if user_name is missing
#
#     user_name = request_data['user_name']  # Extract the user name
#
#     cursor = conn.cursor()  # Create a database cursor
#     try:
#         db_user = "SELECT * FROM users WHERE user_id = %s"  # Check if the user_id already exists
#         cursor.execute(db_user, (user_id,))  # Execute the query
#         existing_user = cursor.fetchone()  # Fetch the result
#
#         if existing_user:  # Check if a user with that ID already exists
#             return jsonify({'status': "error", 'reason': "id already exists"}), 409  # Return an error if user_id exists
#
#         db_user = "INSERT INTO users (user_id, user_name) VALUES (%s, %s)"  # SQL query to insert a new user
#         cursor.execute(db_user, (user_id, user_name))  # Execute the insert query
#         return jsonify({'status': "ok", 'user_added': user_name}), 200
#     finally:
#         cursor.close()  # Close the cursor
#
#
# # def create_user(conn, user_id):  # create_user function (with auto-incrementing ID)
# #     """Creates a new user in the database, allocating a new user_id if needed."""
# #     request_data = request.get_json()  # Get request data
# #     if not request_data or not request_data.get('user_name'):  # Check for user_name
# #         return jsonify({'error': 'Missing required field: user_name'}), 400
# #
# #     user_name = request_data['user_name']  # Get user name
# #
# #     cursor = conn.cursor()  # Create cursor
# #     try:
# #         # Find the highest existing user_id (or start at 1 if no users)
# #         cursor.execute("SELECT MAX(user_id) FROM users")
# #         result = cursor.fetchone()  # Fetch the result
# #         if result[0] is None:  # No users yet
# #             user_id = 1  # Start at 1
# #         else:
# #             user_id = int(result[0]) + 1  # Increment the max id
# #
# #         db_user = "INSERT INTO users2 (user_id, user_name) VALUES (%s, %s)"  # Insert new user
# #         cursor.execute(db_user, (user_id, user_name))  # Execute query
# #         conn.commit()  # Commits
# #         return jsonify({'status': "ok", 'user_added': user_name, 'user_id': user_id}), 200
# #     finally:
# #         cursor.close()  # Close cursor
#
#
# def update_user(conn, user_id):
#     request_data = request.get_json()  # Get the JSON data from the request
#     if not request_data or not request_data.get('user_name'):  # Check if user_name is provided
#         return jsonify({'error': 'Missing required field: user_name'}), 400
#
#     user_name = request_data['user_name']  # Extract the user name
#
#     cursor = conn.cursor()  # Create a database cursor
#     try:
#         db_user = "SELECT * FROM users WHERE user_id = %s"  # Check if the user exists
#         cursor.execute(db_user, (user_id,))  # Execute the query
#         existing_user = cursor.fetchone()  # Fetch the result
#
#         if not existing_user:  # Check if the user exists
#             return jsonify({'status': "error", 'reason': "no such id"}), 500  # Return an error if user not found
#
#         db_user = "UPDATE users SET user_name = %s WHERE user_id = %s"  # SQL query to update the user
#         cursor.execute(db_user, (user_name, user_id))  # Execute the update query
#         return jsonify({'status': "ok", 'user_updated': user_name}), 200
#     finally:
#         cursor.close()  # Close the cursor
#
#
# def delete_user(conn, user_id):  # Function to delete a user
#     cursor = conn.cursor()  # Create a database cursor
#     try:
#         sql = "DELETE FROM users WHERE user_id = %s"  # SQL query to delete the user
#         cursor.execute(sql, (user_id,))  # Execute the delete query
#
#         cursor.execute("SELECT FOUND_ROWS()")  # Get the number of rows deleted
#         rows_deleted = cursor.fetchone()[0]  # Fetch the result
#
#         if rows_deleted == 0:  # Check if any rows were deleted
#             return jsonify({'status': "error", 'reason': "no such id"}), 500  # Return an error if user not found
#         else:
#             return jsonify({'status': "ok", 'user_deleted': user_id}), 200  # Return success message
#     finally:
#         cursor.close()  # Close the cursor

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)