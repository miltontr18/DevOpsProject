from flask import Flask, request, jsonify # Not sure if we can use jsonify?
import pymysql
import pydoc

# Database connection details
schema_name = 'mydb'
conn = pymysql.connect(host='127.0.0.1', port=3306, user='user', passwd='password', db=schema_name)
conn.autocommit(True)

app = Flask(__name__)


@app.route('/users/<user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def users(user_id):
    """Handle requests based on method"""
    if request.method == 'GET':
        return get_user(user_id)
    elif request.method == 'POST':
        return create_user(user_id)
    elif request.method == 'PUT':
        return update_user(user_id)
    elif request.method == 'DELETE':
        return delete_user(user_id)
    else:
        return jsonify({'error': 'Unsupported method'}), 405


def get_user(user_id):
    """Retrieves user data from the database."""
    cursor = conn.cursor()  # Create a database cursor object
    db_user = "SELECT user_name FROM users WHERE user_id = %s"  # SQL query to retrieve user_name
    cursor.execute(db_user, (user_id,))  # Execute the query with user_id as a parameter
    result = cursor.fetchone()  # Fetch the first (and only expected) row from the result

    if result:  # Checking if a user with the given ID was found
        return jsonify({'status': "ok", 'user_name': result[0]}), 200  # Return user_name and success status
    else:
        return jsonify({'status': "error", 'reason': "no such id"}), 500  # Return error for non-existent user

def create_user(user_id):
    """Creates a new user in the database."""
    request_data = request.get_json()  # Get data from the request body (in JSON format)
    if not request_data or not request_data.get('user_name'):
        return jsonify({'error': 'Missing required field: user_name'}), 400  # Return error if user_name is missing

    user_name = request_data['user_name']

    cursor = conn.cursor()
    db_user = "SELECT * FROM users WHERE user_id = %s"
    cursor.execute(db_user, (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({'status': "error", 'reason': "id already exists"}), 409  # Return error if user ID already exists

    db_user = "INSERT INTO users (user_id, user_name) VALUES (%s, %s)"
    cursor.execute(db_user, (user_id, user_name))
    return jsonify({'status': "ok", 'user_added': user_name}), 200  # Return success message and newly added user_name


# def create_user(user_id):
#     """Creates a new user in the database."""
#     """When user_id already exists, allocates new user_id."""
#     request_data = request.get_json()  # Get data from the request body (in JSON format)
#     if not request_data or not request_data.get('user_name'):
#         return jsonify({'error': 'Missing required field: user_name'}), 400  # Return error if user_name is missing
#
#     user_name = request_data['user_name'] # Extract the username from the request data
#
#     cursor = conn.cursor() # Create a database cursor object
#
#     # Find the highest existing user_id
#     cursor.execute("SELECT MAX(user_id) FROM users2") # Executing a query to find the maximum user_id
#     result = cursor.fetchone() # Fetching the result of the query
#     if result[0] is None:  # No users yet, start at 1
#         user_id = 1 # If no users exist, set the new user_id to 1
#     else:
#         user_id = int(result[0]) + 1  # Increment the highest ID to get the next available ID
#
#     db_user = "INSERT INTO users2 (user_id, user_name) VALUES (%s, %s)" # Defining the SQL insert statement
#     try:
#         cursor.execute(db_user, (user_id, user_name)) # Executing the insert statement with the new user data
#         conn.commit() # Commiting the changes to the database
#         cursor.close() # Closing the database cursor
#         return jsonify({'status': "ok", 'user_added': user_name, 'user_id': user_id}), 200 # Returning a success response with the user details
#     except Exception as e:  # To Catch potential database errors
#         conn.rollback()  # No idea what this does.............. will look into it
#         cursor.close() # Close the database cursor
#         return jsonify({'status': "error", 'reason': str(e)}), 500  # Returning a 500 error with the error message

def update_user(user_id):
    """Updates an existing user in the database."""
    request_data = request.get_json()
    if not request_data or not request_data.get('user_name'):
        return jsonify({'error': 'Missing required field: user_name'}), 400

    user_name = request_data['user_name']

    cursor = conn.cursor()
    db_user = "SELECT * FROM users WHERE user_id = %s"
    cursor.execute(db_user, (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        return jsonify({'status': "error", 'reason': "no such id"}), 500

    db_user = "UPDATE users SET user_name = %s WHERE user_id = %s"
    cursor.execute(db_user, (user_name, user_id))
    return jsonify({'status': "ok", 'user_updated': user_name}), 200


def delete_user(user_id):
    """Deletes a user from the database."""
    cursor = conn.cursor()
    sql = "DELETE FROM users WHERE user_id = %s"
    cursor.execute(sql, (user_id,))

    cursor.execute("SELECT FOUND_ROWS()")
    rows_deleted = cursor.fetchone()[0]

    if rows_deleted == 0:
        return jsonify({'status': "error", 'reason': "no such id"}), 500
    else:
        return jsonify({'status': "ok", 'user_deleted': user_id}), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)