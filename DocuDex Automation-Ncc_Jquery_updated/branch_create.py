from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from datetime import datetime
import time
import random
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
driver.get("http://203.76.124.126:5058/configuration/branch")
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
print("✅ Search Document page loaded")
time.sleep(2)

# Branch Create 
create_user_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[.//text()[contains(.,'Add User')]]"))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", create_user_btn)
driver.execute_script("arguments[0].click();", create_user_btn)

print("✅ Create Branch clicked")

upazilas = [
    "Dhanmondi", "Mirpur", "Uttara", "Gulshan", "Banani",
    "Mohammadpur", "Savar", "Keraniganj", "Narayanganj",
    "Gazipur", "Tongi", "Pabna Sadar", "Ishwardi",
    "Rajshahi Sadar", "Boalia", "Motijheel", "Tejgaon",
    "Coxs Bazar Sadar", "Teknaf", "Ukhiya",
    "Chattogram Sadar", "Pahartali", "Panchlaish",
    "Sylhet Sadar", "Beanibazar", "Golapganj",
    "Cumilla Sadar", "Debidwar", "Daudkandi",
    "Khulna Sadar", "Sonadanga", "Khalishpur"
]

selected_upazila = random.choice(upazilas)
# timestamp = datetime.now().strftime("%H%M%S")
branch_name = f"{selected_upazila}"

# Generate Branch Code (6 digit realistic format)
branch_code = str(random.randint(100000, 999999))

print(f"🏷 Generated Branch Name: {branch_name}")
print(f"🔢 Branch Code: {branch_code}")


branch_input = wait.until(
    EC.visibility_of_element_located((By.ID, "docudex_bundle_branchbundle_branch_name"))
)

branch_input.clear()
branch_input.send_keys(branch_name)

print("✅ Branch name entered successfully")


# Fill Branch Code
branch_code_input = wait.until(
    EC.visibility_of_element_located((By.ID, "docudex_bundle_branchbundle_branch_code"))
)
branch_code_input.clear()
branch_code_input.send_keys(branch_code)

print("✅ Branch code entered successfully")

# Wait for Create Branch button to be clickable
create_branch_btn = wait.until(
    EC.element_to_be_clickable((By.ID, "docudex_bundle_branchbundle_branch_submit"))
)

# Scroll to button
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", create_branch_btn)
time.sleep(1)

# Click using JavaScript (more reliable for hidden/overlay buttons)
driver.execute_script("arguments[0].click();", create_branch_btn)
print("✅ Create Branch button clicked")

# Short wait for server processing
time.sleep(3)

# Reload page
driver.refresh()

# Wait until page fully loads again (example element)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
print("🔄 Page refreshed and ready")





input("Check UI. Press Enter to close browser...")
