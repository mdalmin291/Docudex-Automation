from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

# Open login page
driver.get("http://203.76.124.126:5058/login")


# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("4948")

# Enter password
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Ncc@1234")

# Click login button (important)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Wait until homepage/dashboard loads
wait.until(EC.url_changes("http://203.76.124.126:5058/login"))

print("✅ Successfully logged in")

# Wait for Workflow menu
workflow_menu = wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Workflow')]"))
)

# Force open dropdown using JavaScript
driver.execute_script("arguments[0].click();", workflow_menu)
print("✅ Workflow menu opened via JS")

# Now wait for New Workflow link
new_workflow = wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/workflow/template/active-list')]"))
)

# Force click again using JS
driver.execute_script("arguments[0].click();", new_workflow)

print("✅ Clicked on New Workflow")

# Wait for the workflow row to appear
row = wait.until(
    EC.presence_of_element_located((
        By.XPATH,
        "//tr[td[contains(text(),'Account Opening Process (Non-Individual)')]]"
    ))
)

print("✅ Workflow row found")

# Find the Start button inside this row
start_button = row.find_element(By.XPATH, ".//a[contains(@class,'start')]")

# Click using JS (more reliable than normal click)
driver.execute_script("arguments[0].click();", start_button)

print("✅ Start button clicked for Account Opening Process")

# Wait for Bootbox modal to appear
yes_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-bb-handler='confirm' and normalize-space()='Yes']"))
)

# Click using JS to avoid overlay issues
driver.execute_script("arguments[0].click();", yes_button)

print("✅ Clicked YES to initiate workflow")

# Wait for form container to load
wait.until(EC.presence_of_element_located((By.ID, "form_instance_data")))

# Fill Customer Name
customer_name = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1850493788523335680"))
)
customer_name.clear()
customer_name.send_keys("Test Customer alamin")

# Fill Customer ID (CIF)
customer_id = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1850493830621564928"))
)
customer_id.clear()
customer_id.send_keys("CIF-1234")

# Fill Account Number
account_number = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1850493914163712000"))
)
account_number.clear()
account_number.send_keys("AC-6543")

# Fill Account Title
account_title = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1850494046993125376"))
)
account_title.clear()
account_title.send_keys("Savings Account")

print("✅ Workflow initiate form filled successfully")

# Wait for Upload button to be clickable
upload_button = wait.until(
    EC.element_to_be_clickable((By.ID, "btn_upload_to_staging"))
)

# Click using JS (safer for complex UIs)
driver.execute_script("arguments[0].click();", upload_button)

print("✅ Clicked Upload button (Go to staging)")

# Handle potential alert
try:
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    print("⚠ Alert appeared:", alert.text)

    alert.accept()   # Clicks OK
    print("✅ Alert accepted (OK clicked)")

except TimeoutException:
    print("ℹ No browser alert appeared")

# Wait until Upload File(s) button is clickable
upload_modal_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Upload File') or contains(., 'Upload File')]"))
)

# Click using JS (safer in modals)
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", upload_modal_button)
driver.execute_script("arguments[0].click();", upload_modal_button)

print("✅ Upload modal opened")

# Wait until the file input is present in DOM
file_input = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='file' and @name='files[]']"))
)

# Prepare multiple file paths
base_path = r"C:\Users\Devnet\Desktop\DocuDex Automation\Demo file Upload for Testing\PDF Folder"
files = [
    fr"{base_path}\file-example_PDF_1MB.pdf",
    fr"{base_path}\file-example_PDF_500_kB.pdf",
    fr"{base_path}\file-sample_150kB.pdf"
]

# Attach multiple files
file_input.send_keys("\n".join(files))

print("✅ Files attached successfully")

final_upload_button = wait.until(
    EC.element_to_be_clickable((By.ID, "fileupload-save-button"))
)

# Scroll into view and click via JS
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", final_upload_button)
driver.execute_script("arguments[0].click();", final_upload_button)

print("✅ Final upload button clicked")

# Wait until at least one SELECT button is present
select_buttons = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class,'add') and contains(., 'SELECT')]"))
)

print(f"Found {len(select_buttons)} SELECT button(s)")

first_select = select_buttons[0]  # pick the first file
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_select)
driver.execute_script("arguments[0].click();", first_select)

print("✅ First file SELECT clicked")

# Wait for Document ID input
doc_id_input = wait.until(
    EC.presence_of_element_located((By.NAME, "localId"))
)
doc_id_input.clear()  # Clear any existing text
doc_id_input.send_keys("Aof")

print("✅ Document ID filled")

# Wait for Document Name input
doc_name_input = wait.until(
    EC.presence_of_element_located((By.ID, "document-title"))
)
doc_name_input.clear()
doc_name_input.send_keys("Aof")

print("✅ Document Name filled")

# from selenium.webdriver.support.ui import Select

# 1️⃣ Wait for the Document Type dropdown container
doc_type_select = wait.until(
    EC.element_to_be_clickable((By.ID, "metafield"))
)

# 2️⃣ Use Select class to pick "Account Opening Form (AOF)"
Select(doc_type_select).select_by_visible_text("Account Opening Form (AOF)")
print("✅ Document Type selected: Account Opening Form (AOF)")

create_button = wait.until(
    EC.element_to_be_clickable((By.ID, "create-document-button"))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", create_button)
driver.execute_script("arguments[0].click();", create_button)

print("✅ Create Document button clicked")

ok_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-bb-handler='main' and normalize-space()='OK']"))
)

driver.execute_script("arguments[0].click();", ok_button)

print("✅ Success modal OK clicked")

# Wait for the Done button to be present
done_button = wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'view-active-step') and contains(@class,'btn')]"))
)

# Scroll into view
driver.execute_script("arguments[0].scrollIntoView(true);", done_button)

# Click using JS to bypass overlay
driver.execute_script("arguments[0].click();", done_button)

print("✅ Done button clicked via JS")

doc_link = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, "//a[contains(@class,'checklist-document-view') and contains(., 'Account Opening Form')]"
    ))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", doc_link)
driver.execute_script("arguments[0].click();", doc_link)

print("✅ Document clicked (preview modal opened)")

modal = wait.until(
    EC.visibility_of_element_located((By.ID, "document-preview"))
)

print("✅ Document modal opened")

driver.execute_script("""
    let modalBody = arguments[0].querySelector('.modal-body');
    modalBody.scrollTop = modalBody.scrollHeight;
""", modal)

print("✅ Modal scrolled to bottom")

close_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH, "//button[@data-dismiss='modal' and normalize-space()='Close']"
    ))
)

driver.execute_script("arguments[0].click();", close_button)

print("✅ Modal closed successfully")

# Wait for the observation textarea to be present
observation_box = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_observation"))
)

# Scroll into view and focus
driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].focus();", observation_box)

# Clear and set the comment safely using JS
driver.execute_script("arguments[0].value = 'Document added. Proceed forward to Step - 2 (Branch Checker)';", observation_box)

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

# Wait for the Workflow Successfully Started table to appear
workflow_table = wait.until(
    EC.presence_of_element_located((By.XPATH, "//h3[text()='Workflow Successfully Started']/following-sibling::table"))
)

# Locate the Tracking Number cell
tracking_no_element = workflow_table.find_element(
    By.XPATH, ".//tr[th[text()='Tracking Number:']]/td/span"
)

# Get the text
tracking_no = tracking_no_element.text
print(f"✅ Tracking Number extracted: {tracking_no}")

# Save to file
with open("tracking_no.txt", "w") as f:
    f.write(tracking_no)

print("💾 Tracking number saved to tracking_no.txt")

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

def login(username, password):
    driver.get("http://203.76.124.126:5058/login")

    wait.until(EC.presence_of_element_located((By.NAME, "_username"))).clear()
    wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys(username)

    wait.until(EC.presence_of_element_located((By.NAME, "_password"))).clear()
    wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys(password)

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    login_button.click()

    # ✅ Wait for Workflow menu instead of just URL
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Workflow')]"))
    )

    print(f"✅ Logged in as user {username}")


def force_logout():
    driver.get("http://203.76.124.126:5058/logout")
    wait.until(EC.url_contains("/login"))
    print("✅ Forced logout completed")

force_logout()

login("3817", "Ncc@1234")


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
driver.execute_script("arguments[0].value = 'Proced forward to Step 3';", observation_box)

# Trigger input/change events so the system recognizes it
driver.execute_script("""
arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
""", observation_box)

print("✅ Comment added in observation box")


# Wait for the 'Send Backward' button to be clickable
proced_forward_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Proceed Forward')]"))
)

# Scroll into view and click via JS
driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].click();", proced_forward_button)

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

force_logout()


login("2025", "Ncc@1234")

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
driver.execute_script("arguments[0].value = 'Reassign to Step -1';", observation_box)

# Trigger input/change events so the system recognizes it
driver.execute_script("""
arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
""", observation_box)

print("✅ Comment added in observation box")

# 1️⃣ Click the Re-assign dropdown button
reassign_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@id='btn-re-assign-to']//a[contains(@class,'btn')]"))
)

driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
    reassign_button
)

print("✅ Re-assign dropdown opened")


# 2️⃣ Click "Branch Maker (Step-1)"
branch_maker_option = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//a[contains(@class,'move-workflow') and contains(., 'Branch Maker')]"
    ))
)

driver.execute_script("arguments[0].click();", branch_maker_option)

print("✅ Re-assigned to Branch Maker (Step-1)")

sleep(2)  # wait for the action to complete and reflect in UI

# Wait for the Select button inside modal
select_button = wait.until(
    EC.element_to_be_clickable((By.ID, "select-step-branch"))
)

# Scroll into view (important for modals)
driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
    select_button
)

print("✅ Select button clicked successfully")

# Handle potential alert
try:
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    print("⚠ Alert appeared:", alert.text)

    alert.accept()   # Clicks OK
    print("✅ Alert accepted (OK clicked)")

except TimeoutException:
    print("ℹ No browser alert appeared")

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

force_logout()

login("4948", "Ncc@1234")

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
driver.execute_script("arguments[0].value = 'Proced Forward to Step-2';", observation_box)

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

