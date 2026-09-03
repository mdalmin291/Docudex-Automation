from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

# Step 1: Login
driver.get("http://203.76.124.126:5058/login")

wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("superadmin")
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("password")

wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

documents_menu = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Documents')]"))
)
documents_menu.click()

# Step 4: Click Upload Document
stagging_link = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/documents/staging/jobs')]"))    
)
stagging_link.click()

# ---------- Click New Job ----------
new_job_button = wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[@title='New Job' and contains(@href,'/documents/staging/create-job')]"))
)

# Use JS click to avoid overlay issues
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", new_job_button)
driver.execute_script("arguments[0].click();", new_job_button)

print("✅ New Job page opened")

# ---------- Click Upload (open modal) ----------
upload_modal_button = wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@class,'upload') and contains(text(),'Upload')]"))
)

driver.execute_script("arguments[0].click();", upload_modal_button)
print("✅ Upload modal opened")


# ---------- Attach multiple files ----------
file_input = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='file' and @name='files[]']"))
)

# Folder path
base_path = r"C:\Users\Devnet\Desktop\DocuDex Automation\Demo file Upload for Testing\PDF Folder"

# Multiple files (each path separated by newline)
files = [
    fr"{base_path}\file-example_PDF_1MB.pdf",
    fr"{base_path}\file-example_PDF_500_kB.pdf",
    fr"{base_path}\file-sample_150kB.pdf"
]

file_input.send_keys("\n".join(files))

print("✅ Files attached successfully")


# ---------- Click final Upload button ----------
final_upload_button = wait.until(
    EC.presence_of_element_located((By.ID, "fileupload-save-button"))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", final_upload_button)
driver.execute_script("arguments[0].click();", final_upload_button)

print("✅ Final upload button clicked")

# ---------- Click ALL SELECT buttons ----------
select_buttons = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class,'add') and contains(., 'SELECT')]"))
)

print(f"Found {len(select_buttons)} files to select")

for btn in select_buttons:
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    driver.execute_script("arguments[0].click();", btn)

print("✅ All files selected successfully")

# ---------- Fill metadata ----------
value_text = "test_doc_stagging_merged"

# Document ID
doc_id_input = wait.until(
    EC.presence_of_element_located((By.NAME, "localId"))
)
doc_id_input.clear()
doc_id_input.send_keys(value_text)

# Document Name
doc_name_input = wait.until(
    EC.presence_of_element_located((By.NAME, "title"))
)
doc_name_input.clear()
doc_name_input.send_keys(value_text)

print("✅ Document ID and Name filled")

# ---------- Select Department ----------
department_select = wait.until(
    EC.presence_of_element_located((By.ID, "category_0"))
)

Select(department_select).select_by_visible_text("Centralised Unit for GB")
print("✅ Department selected")

# ---------- Click Create Document ----------
create_btn = wait.until(
    EC.element_to_be_clickable((By.ID, "create-document-button"))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", create_btn)
create_btn.click()

print("✅ Create Document clicked")

# Accept alert
alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
print("⚠ Alert appeared:", alert.text)
alert.accept()
print("✅ Alert accepted")

# Now handle Bootbox success modal
success_text = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "bootbox-body"))
)

print("✅ Success message:", success_text.text)

ok_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'bootbox')]//button[text()='OK']"))
)

driver.execute_script("arguments[0].click();", ok_button)
print("✅ Success modal OK clicked")



input("Check UI. Press Enter to close browser...")