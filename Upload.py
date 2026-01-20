from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

# Step 1: Login
driver.get("http://203.76.124.126:5058/login")

wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("superadmin")
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("password")

wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

# # Step 2: Wait for home page
# wait.until(EC.url_contains("/dashboard"))

# print("Logged in successfully")

# Step 3: Click Documents menu
documents_menu = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Documents')]"))
)
documents_menu.click()

# Step 4: Click Upload Document
upload_link = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/documents/upload')]"))
)
upload_link.click()

# Step 5: Confirm upload page loaded
wait.until(EC.url_contains("/documents/upload"))
# File full path (Windows path must be raw string or double backslashes)
file_path = r"C:\Users\Devnet\Desktop\DocuDex Automation\Demo file Upload for Testing\PDF Folder\file-sample_150kB.pdf"

# Wait until file input is present
file_input = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='file' and @name='files[]']"))
)

# Upload file directly
file_input.send_keys(file_path)


# ---------- Generate dynamic value ----------
today = datetime.now().strftime("%d.%m.%Y")
value_text = f"test_document_pdf_{today}"

# ---------- Fill Document ID ----------
doc_id_input = wait.until(
    EC.presence_of_element_located((By.NAME, "localId"))
)
doc_id_input.clear()
doc_id_input.send_keys(value_text)

print("✅ Document ID filled")

# ---------- Fill Document Name ----------
doc_name_input = wait.until(
    EC.presence_of_element_located((By.NAME, "title"))
)
doc_name_input.clear()
doc_name_input.send_keys(value_text)

print("✅ Document Name filled")

# ---------- Select Department ----------
department_dropdown = wait.until(
    EC.presence_of_element_located((By.ID, "category_0"))
)

select = Select(department_dropdown)
select.select_by_visible_text("Centralised Unit for GB")

# Click on save button
save_button = wait.until(
    EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'document-upload')]"))
)

# Scroll to button
driver.execute_script("arguments[0].scrollIntoView(true);", save_button)

# Click using JavaScript (bypasses overlay issue)
driver.execute_script("arguments[0].click();", save_button)

print("✅ Upload and Save clicked successfully")

input("Check UI. Press Enter to close browser...")




