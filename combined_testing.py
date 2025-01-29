import pymysql
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

from db_connector import schema_name

test_id =36 # The ID of the test data in the config table

def get_test_data(test_id):  # Use test_id for clarity
    try:
        with pymysql.connect(host='127.0.0.1', port=3306, user='user', passwd='password', db='mydb') as conn:
            with conn.cursor() as cursor:
                query = "SELECT user_name, backend_url, frontend_url FROM config WHERE id = %s"  # Select all needed columns
                cursor.execute(query, (test_id,))
                result = cursor.fetchone()
                if result:
                    return {
                        'user_name': result[0],
                        'backend_url': result[1],
                        'frontend_url': result[2]
                    }
                else:
                    return None
    except pymysql.Error as e:
        print(f"Error fetching test data: {e}")
        return None

# --- Test Execution ---

test_data = get_test_data(test_id)

if test_data is None:
    print("Test data not found. Exiting.")
    exit()

new_user = test_data['user_name']
url = test_data['backend_url'] + str(test_id)  # Combine base URL and ID
test_url = test_data['frontend_url'] + str(test_id) # Combine base URL and ID

# 1. POST the data
post_user = requests.post(url, json={"user_name": new_user})

if post_user.ok:
    print("POST request successful:", post_user.json())  # More descriptive output
else:
    print(f"POST request failed: {post_user.status_code} - {post_user.text}")
    exit()  # Exit if POST fails; subsequent tests rely on it.

# 2. GET the data for the SAME user
get_user = requests.get(url)

if get_user.status_code == 200:
    get_data = get_user.json()
    print("GET request successful:", get_data)

    # 3. Assert that the retrieved data matches the posted data
    if get_data.get('user_name') == new_user:
        print("API test: Data matches the posted data!")
    else:
        print(f"API test: Data mismatch! Expected '{new_user}', got '{get_data.get('user_name')}'")
else:
    print(f"GET request failed: {get_user.status_code} - {get_user.text}")
    exit() # Exit if GET fails, as the comparison is pointless

# --- Database Check ---
try:
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='user', passwd='password', db='mydb') # Replace with your DB credentials
    with connection.cursor() as cursor:
        db_user = "SELECT user_name FROM users WHERE user_id = %s" # Assumes 'id' is the primary key
        cursor.execute(db_user, (test_id))
        result = cursor.fetchone()

        if result:
            db_user_name = result[0]
            print("Database check: User name in DB:", db_user_name)
            if db_user_name == new_user:
                print("Database check: Data matches posted data!")
            else:
                print(f"Database check: Data mismatch! Expected '{new_user}', got '{db_user_name}'")
        else:
            print("Database check: User not found in the database.")

except pymysql.Error as e:
    print(f"Database error: {e}")

finally:
    if connection:
        connection.close()


# --- Selenium UI Test ---
try:  # Use a try-except block for better error handling
    driver = webdriver.Chrome(service=Service(""))  # You'll likely need to specify the path to your ChromeDriver
    driver.get(test_url)  # Different URL and user ID for Selenium test
    time.sleep(5)  # Adjust sleep time as need.

    user_name_element = driver.find_element(By.ID, value="user") # More descriptive variable name
    ui_user_name = user_name_element.text # Store text in variable
    print("UI user name:", ui_user_name) # Print the value

    # Example assertion (adapt as needed based on your UI and expected data)
    expected_ui_name = new_user # Replace with the actual expected name
    if ui_user_name == expected_ui_name:
        print("Selenium test: UI name matches expected value!")
    else:
        print(f"Selenium test: UI name mismatch! Expected '{expected_ui_name}', got '{ui_user_name}'")

    time.sleep(2) # Small delay before closing
    driver.close()
except Exception as e:  # Catch potential Selenium errors
    print(f"Selenium test error: {e}")
finally: # Ensure driver is closed even if exception occurs
    try:
        driver.quit() # Use quit to close all associated windows and the webdriver process.
    except:
        pass # If driver is not initialized, then do nothing
