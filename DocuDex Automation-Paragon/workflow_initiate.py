from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

# Open login page
# driver.get("http://203.76.124.126:5058/login")
driver.get("http://203.76.124.126:9093/")


# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("DPC000006")

# Enter password
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Paragon@1234")

# Click login button (important)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Wait until homepage/dashboard loads
wait.until(EC.url_changes("http://203.76.124.126:9093/login"))

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
        "//tr[td[contains(text(),'Canteen-Shop Advance Approval Process')]]"
    ))
)

print("✅ Workflow row found")

# Find the Start button inside this row
start_button = row.find_element(By.XPATH, ".//a[contains(@class,'start')]")

# Click using JS (more reliable than normal click)
driver.execute_script("arguments[0].click();", start_button)

print("✅ Start button clicked for Canteen-Shop Advance Approval Process")

# Wait for Bootbox modal to appear
yes_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-bb-handler='confirm' and normalize-space()='Yes']"))
)

# Click using JS to avoid overlay issues
driver.execute_script("arguments[0].click();", yes_button)

print("✅ Clicked YES to initiate workflow")

# Wait for form container to load
wait.until(EC.presence_of_element_located((By.ID, "form_instance_data")))
print("✅ Form loaded successfully")

# Select Division = "Aqua Breeders Limited (Breeder)"
division_dropdown = wait.until(
    EC.element_to_be_clickable((By.ID, "form_instance_paragonDivision"))
)
# Wait for options to be populated
wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='form_instance_paragonDivision']/option[@value='446']")))
Select(division_dropdown).select_by_value("446")
print("✅ Division selected: Aqua Breeders Limited (Breeder)")

# Small wait for department dropdown to load after division selection
time.sleep(1)

# Select Department = "Accounts"
department_dropdown = wait.until(
    EC.element_to_be_clickable((By.ID, "form_instance_paragonDepartment"))
)
# Wait for options to be populated
wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='form_instance_paragonDepartment']/option[@value='512']")))
Select(department_dropdown).select_by_value("512")
print("✅ Department selected: Accounts")

# Fill Advance For Year = 2026
advance_year = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1904972391612682240"))
)
advance_year.clear()
advance_year.send_keys("2026")
print("✅ Advance For Year filled: 2026")

# Fill Advance Amount = 10500
advance_amount = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1904972838385750016"))
)
advance_amount.clear()
advance_amount.send_keys("10500")
print("✅ Advance Amount filled: 10500")

# Fill Payment By (User name)
payment_by = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1904973018912788480"))
)
payment_by.clear()
payment_by.send_keys("DPC000006")
print("✅ Payment By filled: DPC000006")

# Select Duration = "6 Months"
duration_dropdown = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1904973222458167296"))
)
Select(duration_dropdown).select_by_visible_text("6 Months")
print("✅ Duration selected: 6 Months")

# Calculate date: 5 days before present date
advance_payment_date = (datetime.now() - timedelta(days=5)).strftime("%d-%m-%Y")
print(f"✅ Advance Payment Date calculated: {advance_payment_date}")

# Fill Advance Payment date
payment_date = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1904973486112116736"))
)
payment_date.clear()
payment_date.send_keys(advance_payment_date)
print(f"✅ Advance Payment Date filled: {advance_payment_date}")


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
base_path = r"C:\Users\Devnet\Desktop\DocuDex-Automation\DocuDex Automation-MTB LOD CR\Demo file Upload for Testing\PDF Folder"
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
doc_id_input.send_keys("Canteen-shop-Advance-Approval-Process-001")

print("✅ Document ID filled")

# Wait for Document Name input
doc_name_input = wait.until(
    EC.presence_of_element_located((By.ID, "document-title"))
)
doc_name_input.clear()
doc_name_input.send_keys("Canteen-shop-Advance-Approval-Process-001")

print("✅ Document Name filled")

# from selenium.webdriver.support.ui import Select

# 1️⃣ Wait for the Document Type dropdown container
doc_type_select = wait.until(
    EC.element_to_be_clickable((By.ID, "metafield"))
)

# 2️⃣ Use Select class to pick "Account Opening Form (AOF)"
Select(doc_type_select).select_by_visible_text("Canteen-Shop Advance payment documents")
print("✅ Document Type selected: Canteen-Shop Advance payment documents")

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
        By.XPATH, "//a[contains(@class,'checklist-document-view') and contains(., 'Canteen-Shop Advance payment documents')]"
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
time.sleep(4)  # Small wait to ensure modal is closed

# Wait for the observation textarea to be present
observation_box = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_observation"))
)

# Scroll into view and focus
driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].focus();", observation_box)

# Clear and set the comment safely using JS
driver.execute_script("arguments[0].value = 'Document added. Proceed forward to Step - 2 (Department In-charge)';", observation_box)

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

input("Check UI. Press Enter to close browser...")