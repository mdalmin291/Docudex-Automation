from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

# Open login page
driver.get("http://203.76.124.126:5058/login")

# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("2979")

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

from selenium.webdriver.support.ui import Select

# 1️⃣ Wait for the Document Type dropdown container
doc_type_select = wait.until(
    EC.element_to_be_clickable((By.ID, "metafield"))
)

# 2️⃣ Use Select class to pick "Account Opening Form (AOF)"
Select(doc_type_select).select_by_visible_text("Account Opening Form (AOF)")
print("✅ Document Type selected: Account Opening Form (AOF)")

# Wait for the Done button to be present
done_button = wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'view-active-step') and contains(@class,'btn')]"))
)

# Scroll into view
driver.execute_script("arguments[0].scrollIntoView(true);", done_button)

# Click using JS to bypass overlay
driver.execute_script("arguments[0].click();", done_button)

print("✅ Done button clicked via JS")



# Wait for any modal overlay to disappear
wait.until(EC.invisibility_of_element((By.CSS_SELECTOR, "div.modal-scrollable")))

# Now wait for the Done button to appear
done_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'view-active-step') and contains(@class,'btn')]"))
)

# Scroll into view just in case
driver.execute_script("arguments[0].scrollIntoView(true);", done_button)

# Click using JS to avoid overlay issues
driver.execute_script("arguments[0].click();", done_button)

print("✅ Done button clicked via JS")

input("Check UI. Press Enter to close browser...")