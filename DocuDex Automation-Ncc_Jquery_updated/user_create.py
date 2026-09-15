from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support.ui import Select
from datetime import datetime
import time
import random
import string
from datetime import datetime, timedelta
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

# Step 1: Login
driver.get("http://203.76.124.126:5058/login")

wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("superadmin")
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("password")

wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
time.sleep(2)

# Navigate to Branch page
driver.get("http://203.76.124.126:5058/configuration/users")
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
print("✅ Users page loaded")
time.sleep(2)

# User Create 
create_user_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[.//text()[contains(.,'Add User')]]"))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", create_user_btn)
driver.execute_script("arguments[0].click();", create_user_btn)
print("✅ Create User clicked")

def generate_user_id():
    return str(random.randint(10000, 99999))

def generate_name():
    names = ["Akash", "Rafi", "Tanvir", "Nayeem", "Fahim", "Imran", "Shuvo", "Hasan"]
    return random.choice(names) + str(random.randint(10, 99))

wait = WebDriverWait(driver, 15)

# Generate dynamic data
user_id = generate_user_id()
full_name = generate_name()
email = f"{full_name.lower()}@gmail.com"

print("Generated:", user_id, full_name, email)

# Username
wait.until(EC.visibility_of_element_located((By.ID, "manage_user_username"))).send_keys(user_id)

# Full name
driver.find_element(By.ID, "manage_user_fullName").send_keys(full_name)

# Scroll down
driver.execute_script("window.scrollBy(0, 400);")

# Email
driver.find_element(By.ID, "manage_user_email").send_keys(email)
time.sleep(2)


# Scroll more to force UI render
driver.execute_script("window.scrollBy(0, 600);")
time.sleep(1)

# Wait for department section container first
wait.until(
    EC.presence_of_element_located((By.ID, "manage_user_profile_memberOfDepartments"))
)

# Now find checkbox safely
dept_checkbox = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@name='manage_user[profile][memberOfDepartments][]']"))
)

driver.execute_script("arguments[0].click();", dept_checkbox)

print("✅ Department selected")

# Password
driver.find_element(By.ID, "manage_user_plainPassword_first").send_keys("Ncc@1234")
driver.find_element(By.ID, "manage_user_plainPassword_second").send_keys("Ncc@1234")

# Select all department groups
select_box = Select(driver.find_element(By.ID, "department-groups"))

for option in select_box.options:
    select_box.select_by_value(option.get_attribute("value"))

print("✅ All groups selected")

# Scroll to Create button
create_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Create User')]")))
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", create_btn)

# Click Create
driver.execute_script("arguments[0].click();", create_btn)

time.sleep(3)  # Wait for server processing

print("✅ User created successfully")

input("Check UI. Press Enter to close browser...")



