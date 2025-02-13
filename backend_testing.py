import requests
import db_connector

test_id = 8
url = f'http://127.0.0.1:5000/users/{test_id}'
name = 'Jake'
# 1. POST the data
post_user = requests.post(url, json={"user_name": name})
if not post_user.ok:
    print(f"POST request failed: {post_user.status_code} - {post_user.text}")
    exit()

# 2. GET the data for the SAME user.
get_user = requests.get(url)
if get_user.status_code == 200:
    get_data = get_user.json()
    print(get_data)

    # 3. Assert that the retrieved data matches the posted data
    if get_data.get('user_name') == name:  # expected name
        print("Data matches the posted data!")
    else:
        print(f"Data mismatch! Expected {name}, got '{get_data.get('user_name')}'")
else:
    print(f"GET request failed: {get_user.status_code} - {get_user.text}") #Handle the GET error
conn =db_connector.mysql_users()

try:
    with conn.cursor() as cursor:
        db_user = f"SELECT user_name FROM users WHERE user_id = {test_id}" # Assumes 'id' is the primary key
        cursor.execute(db_user)
        result = cursor.fetchone()

        if result:
            db_user_name = result[0]
            print("Database check: User name in DB:", db_user_name)
            if db_user_name == name:
                print("Database check: Data matches posted data!")
            else:
                print(f"Database check: Data mismatch! Expected '{name}', got '{db_user_name}'")
        else:
            print("Database check: User not found in the database.")

# except pymysql.Error as e:
#     print(f"Database error: {e}")

finally:
    if conn:
        conn.close()

