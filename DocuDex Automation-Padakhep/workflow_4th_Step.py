from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

# Open login page
driver.get("http://203.76.124.126:5058/login")

# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("3524")

# Enter password
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Ncc@1234")

# Click login button (important)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Wait until homepage/dashboard loads
wait.until(EC.url_changes("http://203.76.124.126:5058/login"))

print("✅ Successfully logged in")

driver.get("http://203.76.124.126:5058/workflow/groups-list")
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
print("✅ Groups Workflow page loaded")

# Load tracking number from file
with open("tracking_no.txt", "r") as f:
    tracking_no = f.read().strip()

print(f"📥 Loaded Tracking Number: {tracking_no}")

# Wait for Tracking input
tracking_input = wait.until(
    EC.element_to_be_clickable((By.ID, "form_workflow_filter_workflow"))
)

tracking_input.clear()
tracking_input.send_keys(tracking_no)
print("✅ Tracking number entered")

# Click Search
search_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//button[contains(text(),'Search') or contains(text(),'Filter')]"
    ))
)

driver.execute_script("arguments[0].click();", search_button)
print("✅ Search executed successfully")


accept_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'accept') and contains(text(),'Accept')]"))
)

driver.execute_script("arguments[0].click();", accept_button)
print("✅ Accept button clicked")


# Click Confirm inside modal
confirm_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'confirm')]"))
)
driver.execute_script("arguments[0].click();", confirm_button)
print("✅ Confirm button clicked")



# Wait for the observation textarea to be present
observation_box = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_observation"))
)

# Scroll into view and focus
driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].focus();", observation_box)

# Clear and set the comment safely using JS
driver.execute_script("arguments[0].value = 'Checked Everything looks okay.Workflow Completed';", observation_box)

# Trigger input/change events so the system recognizes it
driver.execute_script("""
arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
""", observation_box)

print("✅ Comment added in observation box")


# Wait for the 'Complete Workflow' button to be clickable
Complete_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Complete Workflow')]"))
)

# Scroll into view and click via JS
driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].click();", Complete_button)

print("✅ 'Complete Workflow' button clicked successfully")
# Wait for the confirmation alert
try:
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    print("⚠ Confirmation alert appeared:", alert.text)

    # Click OK
    alert.accept()
    print("✅ 'OK' clicked on Proceed Forward confirmation")

except TimeoutException:
    print("ℹ No confirmation alert appeared")

# Open Workflow menu
workflow_menu = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'dropdown-toggle') and contains(., 'Workflow')]"))
)
driver.execute_script("arguments[0].click();", workflow_menu)

# Click All Workflow
all_workflow_link = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[@href='/workflow/list/all']"))
)
driver.execute_script("arguments[0].click();", all_workflow_link)
print("✅ Navigated to All Workflow page")

toggle_yes = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//label[@for='form_workflow_filter_completed']"
    ))
)

driver.execute_script("arguments[0].click();", toggle_yes)
print("✅ Archived toggle switched to YES")



# Wait for Tracking No input
tracking_input = wait.until(
    EC.presence_of_element_located((By.ID, "form_workflow_filter_workflow"))
)

# Fill Tracking Number
tracking_input.clear()
tracking_input.send_keys(tracking_no)
print(f"✅ Tracking Number '{tracking_no}' entered in search box")

# Click Search / Filter button
search_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Search') or contains(text(),'Filter')]"))
)
driver.execute_script("arguments[0].click();", search_button)
print("✅ Search executed, workflow filtered by Tracking Number")

# Wait until at least one result row appears after search
row = wait.until(
    EC.presence_of_element_located((
        By.XPATH,
        "//table//tr[.//a[contains(@href,'/workflow/')]]"
    ))
)

print("✅ Result row loaded")


tracking_no = tracking_no.strip()

tracking_link = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        f"//a[@href and normalize-space(text())='{tracking_no}']"
    ))
)

driver.execute_script("arguments[0].click();", tracking_link)
print(f"✅ Clicked tracking number: {tracking_no}")

# Navigate to Document Search page
driver.get("http://203.76.124.126:5058/documents/")
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
print("✅ Search Document page loaded")


# Load tracking number from file
with open("tracking_no.txt", "r") as f:
    tracking_no = f.read().strip()

print(f"📥 Loaded Tracking Number: {tracking_no}")

# Wait for Tracking input of Completed Workflow Document Search
tracking_input = wait.until(
    EC.element_to_be_clickable((By.ID, "typeahead_example_3"))
)

tracking_input.clear()
tracking_input.send_keys(tracking_no)
print("✅ Tracking number entered")

# Click Search
search_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//button[contains(text(),'Search') or contains(text(),'Filter')]"
    ))
)

driver.execute_script("arguments[0].click();", search_button)
print("✅ Search executed successfully")


input("Check UI. Press Enter to close browser...")