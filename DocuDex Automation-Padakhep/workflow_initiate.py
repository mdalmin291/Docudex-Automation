from datetime import datetime

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
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException
from time import sleep

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

LOREM_TEXT = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride Printing Library in London, took a 1914 Cicero translation and scrambled it to make dummy text for Letraset's Body Type sheets. It has survived not only many decades, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised thanks to these sheets and more recently with desktop publishing software like Aldus PageMaker and Microsoft Word including versions of Lorem Ipsum."


def fill_text_field(field_id, text):
    """Fill a form text field; falls back to JS if the element is hidden/not interactable."""
    el = wait.until(EC.presence_of_element_located((By.ID, field_id)))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    try:
        el.clear()
        el.send_keys(text)
    except Exception:
        # Element hidden (e.g. inside a collapsed tab) - set value directly via JS
        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, el, text)

# Open login page
# driver.get("http://203.76.124.126:5058/login")
driver.get("http://203.76.124.126:5057/login")


# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("0109180115")

# Enter password
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Padakhep@1234")

# Click login button (important)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Wait until homepage/dashboard loads
wait.until(EC.url_changes("http://203.76.124.126:5057/login"))

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
        "//tr[td[contains(text(),'ICT Purchase Requisition (President Office)')]]"
    ))
)

print("✅ Workflow row found")

# Find the Start button inside this row
start_button = row.find_element(By.XPATH, ".//a[contains(@class,'start')]")

# Click using JS (more reliable than normal click)
driver.execute_script("arguments[0].click();", start_button)

print("✅ Start button clicked for ICT Purchase Requisition (President Office)")

# Wait for Bootbox modal to appear
yes_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-bb-handler='confirm' and normalize-space()='Yes']"))
)

# Click using JS to avoid overlay issues
driver.execute_script("arguments[0].click();", yes_button)

print("✅ Clicked YES to initiate workflow")

# Wait for form container to load
wait.until(EC.presence_of_element_located((By.ID, "form_instance_data")))

# Fill Activity Name
activity_name = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1816427144725663744"))
)
activity_name.clear()
activity_name.send_keys("ICT Purchase Requisition")

# Fill Activity No
activity_no = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1816427148869636096"))
)
activity_no.clear()
activity_no.send_keys("Activity_no-1234")

#Fill date - fill with today's current date
today_date = datetime.now().strftime("%d-%m-%Y") 
account_opening_date = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1816427159661580288"))
)
account_opening_date.clear()
account_opening_date.send_keys(today_date)
print(f"✅ Account Opening Date filled: {today_date}")


# Fill File Note
fill_text_field("form_instance_data_1816427165550383104", LOREM_TEXT)
print("✅ File Note filled")



# Fill Top Sheet
fill_text_field("form_instance_data_1816427171061698560", LOREM_TEXT)
print("✅ Top Sheet filled")


# Fill Letter
fill_text_field("form_instance_data_1816427236367011840", LOREM_TEXT)
print("✅ Letter filled")

# Select "Initiator Work Group" In dropdown
select_element = driver.find_element(By.ID, "form_instance_workGroup")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'System & Support Unit';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'System & Support Unit' from Initiator Work Group dropdown")


sleep(3)  # Wait for any dependent fields to load

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
base_path = r"C:\Users\Administrator\Desktop\Docudex-Automation\DocuDex Automation-Padakhep\Demo file Upload for Testing\PDF Folder"
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
Select(doc_type_select).select_by_visible_text("Attachement")
print("✅ Document Type selected: Attachement")

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
        By.XPATH, "//a[contains(@class,'checklist-document-view') and contains(., 'Attachement')]"
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
driver.execute_script("arguments[0].value = 'Document added. Proceed forward to Step - 2 Division Head (ICT) Access Group';", observation_box)

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