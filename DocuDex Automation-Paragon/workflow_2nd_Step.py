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
driver.get("http://203.76.124.126:9093/")

# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("ABL000001")

# Enter password
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Paragon@1234")

# Click login button (important)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Wait until homepage/dashboard loads
wait.until(EC.url_changes("http://203.76.124.126:9093/login"))

print("✅ Successfully logged in")

driver.get("http://203.76.124.126:9093/workflow/groups-list")
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

# upload_button = wait.until(
#     EC.element_to_be_clickable((By.ID, "btn_upload_to_staging"))
# )

# # Click using JS (safer for complex UIs)
# driver.execute_script("arguments[0].click();", upload_button)

# print("✅ Clicked Upload button (Go to staging)")

# # Handle potential alert
# try:
#     alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
#     print("⚠ Alert appeared:", alert.text)

#     alert.accept()   # Clicks OK
#     print("✅ Alert accepted (OK clicked)")

# except TimeoutException:
#     print("ℹ No browser alert appeared")

# # Wait until at least one SELECT button is present
# select_buttons = wait.until(
#     EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class,'add') and contains(., 'SELECT')]"))
# )

# print(f"Found {len(select_buttons)} SELECT button(s)")

# first_select = select_buttons[0]  # pick the first file
# driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_select)
# driver.execute_script("arguments[0].click();", first_select)

# print("✅ First file SELECT clicked")

# # Wait for Document ID input
# doc_id_input = wait.until(
#     EC.presence_of_element_located((By.NAME, "localId"))
# )
# doc_id_input.clear()  # Clear any existing text
# doc_id_input.send_keys("TP")

# print("✅ Document ID filled")

# # Wait for Document Name input
# doc_name_input = wait.until(
#     EC.presence_of_element_located((By.ID, "document-title"))
# )
# doc_name_input.clear()
# doc_name_input.send_keys("TP")

# print("✅ Document Name filled")

# #  1️⃣ Wait for the Document Type dropdown container
# doc_type_select = wait.until(
#     EC.element_to_be_clickable((By.ID, "metafield"))
# )

# # 2️⃣ Use Select class to pick "Account Opening Form (AOF)"
# Select(doc_type_select).select_by_visible_text("Transaction Profile (TP)")
# print("✅ Document Type selected: Transaction Profile (TP)")

# create_button = wait.until(
#     EC.element_to_be_clickable((By.ID, "create-document-button"))
# )

# driver.execute_script("arguments[0].scrollIntoView({block:'center'});", create_button)
# driver.execute_script("arguments[0].click();", create_button)

# print("✅ Create Document button clicked")

# ok_button = wait.until(
#     EC.element_to_be_clickable((By.XPATH, "//button[@data-bb-handler='main' and normalize-space()='OK']"))
# )

# driver.execute_script("arguments[0].click();", ok_button)

# print("✅ Success modal OK clicked")

# # Wait for the Done button to be present
# done_button = wait.until(
#     EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'view-active-step') and contains(@class,'btn')]"))
# )

# # Scroll into view
# driver.execute_script("arguments[0].scrollIntoView(true);", done_button)

# # Click using JS to bypass overlay
# driver.execute_script("arguments[0].click();", done_button)

# print("✅ Done button clicked via JS")

# doc_link = wait.until(
#     EC.element_to_be_clickable((
#         By.XPATH, "//a[contains(@class,'checklist-document-view') and contains(., 'Transaction Profile (TP) (TP)')]"
#     ))
# )

# driver.execute_script("arguments[0].scrollIntoView({block:'center'});", doc_link)
# driver.execute_script("arguments[0].click();", doc_link)

# print("✅ Document clicked (preview modal opened)")

# modal = wait.until(
#     EC.visibility_of_element_located((By.ID, "document-preview"))
# )

# print("✅ Document modal opened")

# driver.execute_script("""
#     let modalBody = arguments[0].querySelector('.modal-body');
#     modalBody.scrollTop = modalBody.scrollHeight;
# """, modal)

# print("✅ Modal scrolled to bottom")

# close_button = wait.until(
#     EC.element_to_be_clickable((
#         By.XPATH, "//button[@data-dismiss='modal' and normalize-space()='Close']"
#     ))
# )

# driver.execute_script("arguments[0].click();", close_button)

# print("✅ Modal closed successfully")

# Wait for the observation textarea to be present
observation_box = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_observation"))
)

# Scroll into view and focus
driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].focus();", observation_box)

# Clear and set the comment safely using JS
driver.execute_script("arguments[0].value = 'Proceed forward to Step - 3 (Sector Authorizer)';", observation_box)

# Trigger input/change events so the system recognizes it
driver.execute_script("""
arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
""", observation_box)

print("✅ Comment added in observation box")

# Wait for the 'Proceed Forward' button to be clickable
proceed_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Proceed Forward')]"))
)

# Scroll into view and click via JS
driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].click();", proceed_button)

print("✅ 'Proceed Forward' button clicked successfully")
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
input("Check UI. Press Enter to close browser...")