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
driver.get("http://27.147.184.165:8082/")


# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("aoo-nibw-bab_test")

# Enter password
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Mtb@12345678910")

# Click login button (important)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Wait until homepage/dashboard loads
wait.until(EC.url_changes("http://27.147.184.165:8082/login"))

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
        "//tr[td[contains(text(),'Term deposit : Individual (NIBW)_{LOU-6}')]]"
    ))
)

print("✅ Workflow row found")

# Find the Start button inside this row
start_button = row.find_element(By.XPATH, ".//a[contains(@class,'start')]")

# Click using JS (more reliable than normal click)
driver.execute_script("arguments[0].click();", start_button)

print("✅ Start button clicked for Term deposit : Individual (NIBW)_{LOU-6}')")

# Wait for Bootbox modal to appear
yes_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-bb-handler='confirm' and normalize-space()='Yes']"))
)

# Click using JS to avoid overlay issues
driver.execute_script("arguments[0].click();", yes_button)

print("✅ Clicked YES to initiate workflow")

# Wait for form container to load
wait.until(EC.presence_of_element_located((By.ID, "form_instance_data")))

# Select "New Customer" from Application For dropdown
select_element = driver.find_element(By.ID, "form_instance_data_1921323463151194112")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'New Customer';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'New Customer' from Application For dropdown")

# Select "Quick Account" from Account Type dropdown
select_element = driver.find_element(By.ID, "form_instance_data_1921325044156338176")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'Quick Account';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'Quick Account' from Account Type dropdown")



# Account number selection
account_number = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1921324770419281920"))
)
account_number.clear()
account_number.send_keys("1234567891012")
print("✅ Account Number filled: 1234567891012")

# Account title selection
account_title = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1921324468530057216"))
)
account_title.clear()
account_title.send_keys("ABC Group")
print("✅ Account Title filled: ABC Group")


# Select "Customer Type" In dropdown
select_element = driver.find_element(By.ID, "form_instance_data_1921325345902956544")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'WBD';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'WBD' from Customer Type dropdown")

# Select "Account Product Type" In dropdown
select_element = driver.find_element(By.ID, "form_instance_data_1921325992010321920")
driver.execute_script("""
    var select = arguments[0];
    select.value = '132 - MTB Islamic Current Account (Non-Individual)';
    $(select).trigger('change');
""", select_element)
print("✅ Selected '132 - MTB Islamic Current Account (Non-Individual)' from Account Product Type dropdown")



# Select "Debit Card Requisition" In dropdown
select_element = driver.find_element(By.ID, "form_instance_data_1921343723304652800")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'Yes';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'Yes' from Debit Card Requisition dropdown")

# Select "Check Book Requisition" In dropdown
select_element = driver.find_element(By.ID, "form_instance_data_1921343908231516160")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'Yes';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'Yes' from Check Book Requisition dropdown")

# Select "Allow Internet Banking" In dropdown
select_element = driver.find_element(By.ID, "form_instance_data_1921344288847826944")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'Yes';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'Yes' from Allow Internet Banking dropdown")


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
base_path = r"C:\Users\Administrator\Desktop\Docudex-Automation\DocuDex Automation-MTB LOD CR\Demo file Upload for Testing\PDF Folder"
files = [
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

doc_type_select = driver.find_element(By.ID, "metafield")
driver.execute_script("""
    var select = arguments[0];
    select.value = '1922688930394673152';
    $(select).trigger('change');
""", doc_type_select)
print("✅ Document Type selected: aof (Account Opening Form)")

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
        By.XPATH, "//a[contains(@class,'checklist-document-view') and contains(., 'AOF (Account Opening Form)')]"
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

# Try to find Close button with multiple selectors
modal_closed = False
try:
    # Try exact match first
    close_button = wait.until(
        EC.element_to_be_clickable((
            By.XPATH, "//button[@data-dismiss='modal' and normalize-space()='Close']"
        ))
    )
    driver.execute_script("arguments[0].click();", close_button)
    modal_closed = True
    print("✅ Modal closed via Close button (exact match)")
except TimeoutException:
    try:
        # Try button containing "Close" text
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[@data-dismiss='modal' and contains(text(), 'Close')]"
            ))
        )
        driver.execute_script("arguments[0].click();", close_button)
        modal_closed = True
        print("✅ Modal closed via Close button (contains)")
    except TimeoutException:
        try:
            # Try generic modal close button (X icon)
            close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((
                    By.XPATH, "//button[contains(@class, 'close')]"
                ))
            )
            driver.execute_script("arguments[0].click();", close_button)
            modal_closed = True
            print("✅ Modal closed via X button")
        except TimeoutException:
            # Last resort: Press Escape key or use JS to hide modal
            print("⚠ Close button not found, trying Escape key...")
            from selenium.webdriver.common.keys import Keys
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            sleep(1)

if not modal_closed:
    # Fallback: Use JavaScript to remove modal from DOM
    driver.execute_script("""
        if (arguments[0]) {
            arguments[0].remove();
        }
    """, modal)
    print("✅ Modal closed via JavaScript")

print("✅ Modal closed successfully")

# Wait for the observation textarea to be present
observation_box = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_observation"))
)

# Scroll into view and focus
driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].focus();", observation_box)

# Clear and set the comment safely using JS
driver.execute_script("arguments[0].value = 'Document added. Proceed forward to Step - 2 (Authorizer-Branch)';", observation_box)

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
# Directly wait for the tracking number element
try:
    tracking_no_element = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//th[contains(.,'Tracking Number')]/following-sibling::td//span"
        ))
    )
    tracking_no = tracking_no_element.text
    print("Tracking No:", tracking_no)

    # Save to file
    with open("tracking_no.txt", "w") as f:
        f.write(tracking_no)
except TimeoutException:
    print("⚠ Could not find tracking number element")
    # Try alternative selector
    try:
        tracking_no_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//td[preceding-sibling::th[contains(.,'Tracking Number')]]//span"
            ))
        )
        tracking_no = tracking_no_element.text
        print("Tracking No (alternative):", tracking_no)

        # Save to file
        with open("tracking_no.txt", "w") as f:
            f.write(tracking_no)
    except:
        print("⚠ All tracking number selectors failed")
        # Try to load from file if it exists
        try:
            with open("tracking_no.txt", "r") as f:
                tracking_no = f.read().strip()
            if tracking_no:
                print(f"✅ Loaded tracking number from file: {tracking_no}")
            else:
                tracking_no = input("Please enter the tracking number manually: ").strip()
        except:
            tracking_no = input("Please enter the tracking number manually: ").strip()

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


def force_logout():
    driver.get("http://27.147.184.165:8082/logout")
    wait.until(EC.url_contains("/login"))
    print("✅ Forced logout completed")

force_logout()


# Open login page
driver.get("http://27.147.184.165:8082/")


# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("aob-nibw-bab")

# Enter password
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Mtb@12345678910")

# Click login button (important)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Wait until homepage/dashboard loads
wait.until(EC.url_changes("http://27.147.184.165:8082/login"))

print("✅ Successfully logged in")

   
driver.get("http://27.147.184.165:8082/workflow/groups-list")
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
driver.execute_script("arguments[0].value = 'Proced forward to ICSU (HO)';", observation_box)

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


print("✅ Logged out successfully")


# Open login page
driver.get("http://27.147.184.165:8082/")


# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("icsu--ibw-nibw")

# Enter password
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Mtb@12345678910")

# Click login button (important)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Wait until homepage/dashboard loads
wait.until(EC.url_changes("http://27.147.184.165:8082/login"))

print("✅ Successfully logged in")

driver.get("http://27.147.184.165:8082/workflow/groups-list")
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
driver.execute_script("arguments[0].value = 'Proced forward to Distributor (HO)';", observation_box)

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

force_logout()

print("✅ Paused")


# Open login page
driver.get("http://27.147.184.165:8082/")


# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("distributor-nibw")

# Enter password
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Mtb@12345678910")

# Click login button (important)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Wait until homepage/dashboard loads
wait.until(EC.url_changes("http://27.147.184.165:8082/login"))

print("✅ Successfully logged in")

driver.get("http://27.147.184.165:8082/workflow/groups-list")
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
driver.execute_script("arguments[0].value = 'Proced forward to Assessor (HO)';", observation_box)

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

force_logout()


# Open login page
driver.get("http://27.147.184.165:8082/")


# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("assessor-nibw")

# Enter password
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Mtb@12345678910")

# Click login button (important)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Wait until homepage/dashboard loads
wait.until(EC.url_changes("http://27.147.184.165:8082/login"))

print("✅ Successfully logged in")

driver.get("http://27.147.184.165:8082/workflow/groups-list")
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


# CIF number selection
Cif_number = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1921324091780894720"))
)
Cif_number.clear()
Cif_number.send_keys("12345")
print("✅ CIF Number filled: 12345")


# Confirm CIF number selection
Cif_number = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1921324318051012608"))
)
Cif_number.clear()
Cif_number.send_keys("12345")
print("✅ CIF Number filled: 12345")


# Confirm Account number selection
Cif_number = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1921324924367015936"))
)
Cif_number.clear()
Cif_number.send_keys("1234567891012")
print("✅ CIF Number filled: 1234567891012")

# Wait for the observation textarea to be present
observation_box = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_observation"))
)


# Scroll into view and focus
driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].focus();", observation_box)

# Clear and set the comment safely using JS
driver.execute_script("arguments[0].value = 'Proced forward to Data Entry Officer (HO)';", observation_box)

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

force_logout()

#Open login page
driver.get("http://27.147.184.165:8082/")


# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("dee-lod-nibw")

# Enter password
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Mtb@12345678910")

# Click login button (important)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Wait until homepage/dashboard loads
wait.until(EC.url_changes("http://27.147.184.165:8082/login"))

print("✅ Successfully logged in")

driver.get("http://27.147.184.165:8082/workflow/groups-list")
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

# CIF number selection
Cif_number = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1921211990232010752"))
)
Cif_number.clear()
Cif_number.send_keys("12345")
print("✅ CIF Number filled: 12345")


# Confirm Customer entry
Confirm_customer_number = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1921212482626523136"))
)
Confirm_customer_number.clear()
Confirm_customer_number.send_keys("1234567891012")
print("✅ Customer Number filled: 1234567891012")

# Wait for the observation textarea to be present
observation_box = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_observation"))
)


# Scroll into view and focus
driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].focus();", observation_box)

# Clear and set the comment safely using JS
driver.execute_script("arguments[0].value = 'Proced forward to Authorizer (HO)';", observation_box)

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

force_logout()

#Open login page
driver.get("http://27.147.184.165:8082/")


# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("ao-nibw")

# Enter password
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Mtb@12345678910")

# Click login button (important)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Wait until homepage/dashboard loads
wait.until(EC.url_changes("http://27.147.184.165:8082/login"))

print("✅ Successfully logged in")

driver.get("http://27.147.184.165:8082/workflow/groups-list")
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

# Confirm CIF number selection
Cif_number = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1921212088601022464"))
)
Cif_number.clear()
Cif_number.send_keys("12345")
print("✅ CIF Number filled: 12345")


# Wait for the observation textarea to be present
observation_box = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_observation"))
)


# Scroll into view and focus
driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].focus();", observation_box)

# Clear and set the comment safely using JS
driver.execute_script("arguments[0].value = 'Proced forward to DEE(Correspondence Unit)(HO)';", observation_box)

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

force_logout()

#Open login page
driver.get("http://27.147.184.165:8082/")


# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("dee-cor-unit-nibw")

# Enter password
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Mtb@12345678910")

# Click login button (important)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Wait until homepage/dashboard loads
wait.until(EC.url_changes("http://27.147.184.165:8082/login"))

print("✅ Successfully logged in")

driver.get("http://27.147.184.165:8082/workflow/groups-list")
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
driver.execute_script("arguments[0].value = 'Proced forward to Authorizer (HO)';", observation_box)

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

force_logout()

#Open login page
driver.get("http://27.147.184.165:8082/")


# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("ao-cor-unit-nibw")

# Enter password
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Mtb@12345678910")

# Click login button (important)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Wait until homepage/dashboard loads
wait.until(EC.url_changes("http://27.147.184.165:8082/login"))

print("✅ Successfully logged in")

driver.get("http://27.147.184.165:8082/workflow/groups-list")
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
driver.execute_script("arguments[0].value = 'Workflow Completed';", observation_box)

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
    print("✅ 'OK' clicked on Complete Workflow confirmation")

except TimeoutException:
    print("ℹ No confirmation alert appeared")

input("Check UI. Press Enter to close browser...")

