import requests


url = 'http://127.0.0.1:5000/users/40'
name = 'bricks'
# 1. POST the data
post_user = requests.post(url, json={"user_name": name})

if post_user.ok:
    print(post_user.json())
else:
    print(f"POST request failed: {post_user.status_code} - {post_user.text}")
    exit()

# 2. GET the data for the SAME user
get_user = requests.get(url)

if get_user.status_code == 200:
    get_data = get_user.json()
    print(get_data)

    # 3. Assert that the retrieved data matches the posted data
    if get_data.get('user_name') == name:  # expected name
        print("Data matches the posted data!")
    else:
        print(f"Data mismatch! Expected 'timmmy', got '{get_data.get('user_name')}'")
else:
    print(f"GET request failed: {get_user.status_code} - {get_user.text}") #Handle the GET error

