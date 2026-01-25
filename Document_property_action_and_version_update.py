from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from datetime import datetime
import time
from datetime import datetime, timedelta
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

# Step 1: Login
driver.get("http://203.76.124.126:5058/login")

wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("2979")
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Ncc@1234")

wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

# # Step 2: Wait for home page
# wait.until(EC.url_contains("/dashboard"))

print("Logged in successfully")
time.sleep(2)


# Step 3: Click Documents menu
driver.get("http://203.76.124.126:5058/documents/upload")
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
time.sleep(2)

# File full path (Windows path must be raw string or double backslashes)
file_path = r"C:\Users\Devnet\Desktop\DocuDex Automation\Demo file Upload for Testing\PDF Folder\file-sample_150kB.pdf"

# Wait until file input is present
file_input = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='file' and @name='files[]']"))
)

# Upload file directly
file_input.send_keys(file_path)
time.sleep(2)



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
time.sleep(2)


# ---------- Fill Document Name ----------
doc_name_input = wait.until(
    EC.presence_of_element_located((By.NAME, "title"))
)
doc_name_input.clear()
doc_name_input.send_keys(value_text)

print("✅ Document Name filled")
time.sleep(2)


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
time.sleep(2)


# Scroll to button
driver.execute_script("arguments[0].scrollIntoView(true);", save_button)

# Click using JavaScript (bypasses overlay issue)
driver.execute_script("arguments[0].click();", save_button)

print("✅ Upload and Save clicked successfully")
time.sleep(2)


# Wait for Bootbox modal OK button and click it
try:
    ok_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'bootbox')]//button[normalize-space()='OK']"))
    )
    driver.execute_script("arguments[0].click();", ok_button)
    print("✅ Bootbox OK clicked")
except:
    print("ℹ Bootbox modal did not appear")
    time.sleep(2)



documents_menu = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Documents')]"))
)
documents_menu.click()


# Step 4: Click Upload Document
search_link = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/documents/')]"))    
)
search_link.click()



# Generate same dynamic value used during upload
today = datetime.now().strftime("%d.%m.%Y")
search_text = f"test_document_pdf_{today}"

search_button = wait.until(
    EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and contains(@class,'green')]"))
)

# Wait for input and type value
search_input = wait.until(
    EC.presence_of_element_located((By.NAME, "localId"))
)

search_input.clear()
search_input.send_keys(search_text)

# Scroll into view
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", search_button)

# Force click using JavaScript
driver.execute_script("arguments[0].click();", search_button)

print("✅ Search button clicked successfully")
time.sleep(2)


doc_name = f"test_document_pdf_{datetime.now().strftime('%d.%m.%Y')}"

document_link = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        f"//tr[contains(@class,'doc')]//a[normalize-space()='{doc_name}']"
    ))
)

driver.execute_script("arguments[0].click();", document_link)
print("✅ Document opened successfully")
time.sleep(2)


# Download the Document
download_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//a[contains(@href, '/documents/file-download/')]"
    ))
)

driver.execute_script("arguments[0].click();", download_button)
print("✅ Download button clicked")
time.sleep(2)


# Send for Review
send_for_review = wait.until(
    EC.presence_of_element_located((By.ID, "send-for-review-button"))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", send_for_review)
driver.execute_script("arguments[0].click();", send_for_review)

print("✅ Review action confirmed")
time.sleep(2)


# Rajib Kumar Chakraborty user selection for review
dropdown = wait.until(
    EC.presence_of_element_located((By.ID, "review_form_request_for"))
)

select = Select(dropdown)
select.select_by_visible_text("Rajib Kumar Chakraborty")

print("✅ User selected: Rajib Kumar Chakraborty")

# Description addition
description_box = wait.until(
    EC.element_to_be_clickable((By.ID, "review_form_note"))
)

description_box.clear()
description_box.send_keys("Please Review this Document")

print("✅ Description added")
time.sleep(2)


# Wait for the Send button inside the modal
send_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//div[contains(@class,'modal-footer')]//button[contains(@class,'update-document-data') and contains(text(),'Send')]"
    ))
)

# Scroll into view and click via JS
driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].click();", send_button)

print("✅ Send button clicked")
time.sleep(2)
# Edit Document Properties
edit_button = wait.until(
    EC.element_to_be_clickable((By.ID, "edit-Properties-button"))
)

driver.execute_script("arguments[0].click();", edit_button)
print("✅ Edit Properties clicked")
time.sleep(2)


# Wait until Edit Properties modal is visible
wait.until(EC.visibility_of_element_located((By.ID, "Edit-Properties")))
print("✅ Edit Properties modal opened")
time.sleep(2)

# 1. Fill Description
description_input = wait.until(
    EC.presence_of_element_located((By.ID, "document_version_description"))
)
description_input.clear()
description_input.send_keys("This Document Edited")
print("✅ Description updated")
time.sleep(2)

# 2. Get Create Date
create_date_input = wait.until(
    EC.presence_of_element_located((By.ID, "document_document_createDate"))
)

create_date_str = create_date_input.get_attribute("value")  # e.g. 2026-01-20
create_date = datetime.strptime(create_date_str, "%Y-%m-%d")

print(f"📅 Create Date: {create_date_str}")

# 3. Add 7 days
expire_date = create_date + timedelta(days=7)
expire_date_str = expire_date.strftime("%Y-%m-%d")

print(f"📅 Expire Date (calculated): {expire_date_str}")
time.sleep(2)

# 4. Set Expire Date using JS (because field is readonly)
expire_input = wait.until(
    EC.presence_of_element_located((By.ID, "document_document_expireDate"))
)

driver.execute_script(
    "arguments[0].removeAttribute('readonly'); arguments[0].value = arguments[1];",
    expire_input,
    expire_date_str
)

print("✅ Expire Date updated")
time.sleep(2)

save_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//div[contains(@class,'modal') and contains(@class,'in')]"
        "//button[@data-form='#form-update-document-property' and normalize-space()='Save']"
    ))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_button)
time.sleep(1)

driver.execute_script("""
arguments[0].dispatchEvent(new MouseEvent('click', {
    bubbles: true,
    cancelable: true,
    view: window
}));
""", save_button)

print("✅ Save triggered correctly")
time.sleep(2)
wait.until(EC.invisibility_of_element_located((By.ID, "Edit-Properties")))
print("✅ Modal closed — Save confirmed")


# Wait until DOM is stable after modal close
time.sleep(1)

# Re-locate fresh element
upload_version_btn = wait.until(
    EC.presence_of_element_located((
        By.XPATH, "//a[.//text()[contains(., 'Upload New Version')]]"
    ))
)

# Wait until clickable
wait.until(EC.element_to_be_clickable((
    By.XPATH, "//a[.//text()[contains(., 'Upload New Version')]]"
)))

# Click safely
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", upload_version_btn)
driver.execute_script("arguments[0].click();", upload_version_btn)

print("✅ Upload New Version clicked")

file_path = r"C:\Users\Devnet\Desktop\DocuDex Automation\Demo file Upload for Testing\OCR Test\ocr.pdf"

file_input = wait.until(
    EC.presence_of_element_located((By.ID, "fileupload"))
)

# Upload file (this automatically triggers selection)
file_input.send_keys(file_path)

print("✅ File uploaded successfully")
time.sleep(2)

comment_box = wait.until(
    EC.visibility_of_element_located((By.NAME, "notes"))
)

comment_box.clear()
comment_box.send_keys("Uploaded new Version of this document")

print("✅ Comment added")
time.sleep(1)

save_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save')]"))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_button)
time.sleep(1)

driver.execute_script("arguments[0].click();", save_button)

print("✅ Save clicked for new version")
time.sleep(2)

# Add New Version Upload for the second time
upload_version_btn_new = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//a[.//text()[contains(., 'Upload New Version')]]"
    ))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", upload_version_btn_new)
time.sleep(1)

driver.execute_script("arguments[0].click();", upload_version_btn_new)

print("✅ Upload 2nd New Version clicked")




# Provide full path of the second file
file_path_2 = r"C:\Users\Devnet\Desktop\DocuDex Automation\Demo file Upload for Testing\PDF Folder\file-example_PDF_1MB.pdf"

file_input_2 = wait.until(
    EC.presence_of_element_located((By.ID, "fileupload"))
)

file_input_2.send_keys(file_path_2)
print("✅ 2nd File uploaded successfully")
time.sleep(5)


merge_radio = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//label[contains(normalize-space(),'Merge this with latest version')]"
    ))
)

driver.execute_script("arguments[0].click();", merge_radio)
print("✅ Selected merge via label")


# 2️⃣ Select "End of the document"
end_radio = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@name='merge_position' and @value='end']"))
)
driver.execute_script("arguments[0].click();", end_radio)
print("✅ Selected 'End of the document'")
time.sleep(1)

# 3️⃣ Select "Minor changes (2.1)"
minor_radio = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@name='next_version' and @value='minor']"))
)
driver.execute_script("arguments[0].click();", minor_radio)
print("✅ Selected 'Minor changes (2.1)'")
time.sleep(1)



# 4️⃣ Add comment
comment_box_new = wait.until(
    EC.visibility_of_element_located((By.NAME, "notes"))
)
comment_box_new.clear()
comment_box_new.send_keys("Document has been mergered at the end of the document as Minor changes Version")
print("✅ 2nd Comment added")
time.sleep(1)


save_button_new = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save')]"))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_button_new)
time.sleep(1)

driver.execute_script("arguments[0].click();", save_button_new)

print("✅ Save clicked for new version")

input("Check UI. Press Enter to close browser...")




