from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service = Service(""))

driver.get("http://127.0.0.1:5001/users/get_user_data/2")
time.sleep(5)
user_name = driver.find_element(By.ID, value= "user")
print(user_name.text)
time.sleep(5)
driver.close()