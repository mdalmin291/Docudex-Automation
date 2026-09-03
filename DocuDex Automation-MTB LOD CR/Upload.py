from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

# Helper function to safely fill input fields using JavaScript (prevents stale element issues)
def safe_fill_input(driver, element_id, value):
    """Safely fill an input field using JavaScript by ID - completely bypasses stale element issues"""
    driver.execute_script(f"""
        var elem = document.getElementById('{element_id}');
        if (elem) {{
            elem.value = '{value}';
            elem.dispatchEvent(new Event('input', {{ bubbles: true }}));
            elem.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    """)

# Step 1: Login
driver.get("http://27.147.184.165:8082/")

wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("alamin")
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Mtb@12345678910")

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
file_path = r"C:\Users\Devnet\Desktop\DocuDex-Automation\DocuDex Automation-MTB LOD CR\Demo file Upload for Testing\PDF Folder\file-sample_150kB.pdf"

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
select.select_by_visible_text("AML and CFTD")

#--------- Bypass Select2 for Group Documents ----------
real_dropdown = wait.until(
    EC.presence_of_element_located((By.ID, "category_1"))
)

Select(real_dropdown).select_by_visible_text("Documents")

print("✅ Group Documents selected (bypassed Select2)")


# ---------- Select Category ----------

category_dropdown = wait.until(
    EC.presence_of_element_located((By.ID, "category_2"))
)

Select(category_dropdown).select_by_visible_text("STR")

print("✅ STR category selected (stable method)")

# Type selection - CHO Forwarding Letter
type_dropdown = wait.until(
    EC.presence_of_element_located((By.ID, "category_3"))
)

Select(type_dropdown).select_by_visible_text("CHO Forwarding Letter")

print("✅ CHO Forwarding Letter selected (stable method)")

# Wait for the tag input to be clickable
#tag_input = wait.until(
    #EC.element_to_be_clickable((By.XPATH, "//ul[@class='select2-choices']//input[@class='select2-input']"))
#)

# Click to focus
#tag_input.click()

# Type your tag
#tag_name = "test"
#tag_input.send_keys(tag_name)

# Press Enter to select
#tag_input.send_keys(Keys.ENTER)

#print(f"✅ Tag '{tag_name}' selected successfully")

#input("Check UI. Press Enter to close browser...")

# Fill GO AML Report ID using JavaScript only (bypasses stale element issues)
driver.execute_script("""
    var elem = document.getElementById('meta_1800142721587875840');
    if (elem) {
        elem.value = 'T-123';
        elem.dispatchEvent(new Event('input', { bubbles: true }));
        elem.dispatchEvent(new Event('change', { bubbles: true }));
    }
""")

print("✅ 'go AML, Report ID' filled with T-123")

# Fill Report Entity Reference
safe_fill_input(driver, "meta_1800142829456986112", "T-123")
print("✅ 'Report Entity Reference' filled with T-123")

# Fill Customer Name
safe_fill_input(driver, "meta_1800142927863746560", "Test Customer")
print("✅ 'Customer Name' filled with Test Customer")

# Fill Account Number
safe_fill_input(driver, "meta_1800143057413214208", "A-321")
print("✅ 'Account Number' filled with A-321")

# Fill STR File Number
safe_fill_input(driver, "meta_1800143105861619712", "STR-123")
print("✅ 'STR File Number' filled with STR-123")


# Type selection - Branch Name Code
branch_name_code_dropdown = wait.until(
    EC.presence_of_element_located((By.ID, "meta_1800143269716299776"))
)

Select(branch_name_code_dropdown).select_by_visible_text("MTB Center Corporate")

print("✅ MTB Center Corporate selected (stable method)")


# Fill AML/CFT/RM
safe_fill_input(driver, "meta_1800143451572932608", "AML-CFT-RM-123")
print("✅ 'AML/CFT/RM' filled with AML-CFT-RM-123")

# Wait for the input to be present
bfiu_date_input = wait.until(
    EC.presence_of_element_located((By.ID, "meta_1800143491985051648"))
)

# Get today's date in YYYY-MM-DD format (adjust if your system uses another format)
today = datetime.today().strftime('%Y-%m-%d')

# Set the value using JavaScript
driver.execute_script("arguments[0].value = arguments[1];", bfiu_date_input, today)

print(f"✅ 'BFIU Submission Date' set to today's date: {today}")


# Fill File Barcode Number
safe_fill_input(driver, "meta_1699735364442263552", "FILE-123")
print("✅ 'File Barcode Number' filled with FILE-123")

# Fill Box Barcode Number
safe_fill_input(driver, "meta_1699735453730607104", "BOX-123")
print("✅ 'Box Barcode Number' filled with BOX-123")

# Fill Shelf Number
safe_fill_input(driver, "meta_1699735586996228096", "SHELF-123")
print("✅ 'Shelf Number' filled with SHELF-123")

# Fill Rack Number
safe_fill_input(driver, "meta_1699735640637181952", "RACK-123")
print("✅ 'Rack Number' filled with RACK-123")


# Type selection - Branch Name
branch_name_dropdown = wait.until(
    EC.presence_of_element_located((By.ID, "meta_1699738415639040000"))
)

Select(branch_name_dropdown).select_by_visible_text("MTB Center Corporate")

print("✅ MTB Center Corporate selected (stable method)")

# Type selection - Warehouse Location
warehouse_location_dropdown = wait.until(
    EC.presence_of_element_located((By.ID, "meta_1699738415639040000"))
)

Select(warehouse_location_dropdown).select_by_visible_text("MTB Center Corporate")

print("✅ MTB Center Corporate selected (stable method)")


# Type selection - Digital Archival Type
digital_archival_type_dropdown = wait.until(
    EC.presence_of_element_located((By.ID, "meta_1699739217724182528"))
)

Select(digital_archival_type_dropdown).select_by_visible_text("Scan")

print("✅ Scan selected (stable method)")

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




