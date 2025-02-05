from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'Click here for Rest API: <a href="http://127.0.0.1:5001/users/get_user_data/">http://127.0.0.1:5001/users/get_user_data/</a>'

@app.route('/users/get_user_data/<user_id>')
def get_user_data(user_id): # function takes the user_id from the URL as an argument.
    users_api = f"http://127.0.0.1:5000/users/{user_id}" # compiles the URL for the users API by adding the provided user_id.
    user_name = requests.get(users_api).json().get('user_name') # makes a GET request to the users API and extracts the 'user_name' from the JSON response.
    if user_name:
        return f"<h1 id='user'>{user_name}</h1>", 200 # If a user_name is found (i.e., the API request was successful and returned a name), this line returns an HTML showing the user's name
    else:
        return f"<h1 id='error'>User not found: User ID {user_id}</h1>", 404
    # If the user_name is not found, line returns an HTML showiing the user was not found

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
