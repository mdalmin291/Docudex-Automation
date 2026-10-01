from datetime import datetime, timedelta
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
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("sayoduzaman")

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
        "//tr[td[contains(text(),'Loan Document Approval Process')]]"
    ))
)

print("✅ Workflow row found")

# Find the Start button inside this row
start_button = row.find_element(By.XPATH, ".//a[contains(@class,'start')]")

# Click using JS (more reliable than normal click)
driver.execute_script("arguments[0].click();", start_button)

print("✅ Start button clicked for Loan Document Approval Process")

# Wait for Bootbox modal to appear
yes_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-bb-handler='confirm' and normalize-space()='Yes']"))
)

# Click using JS to avoid overlay issues
driver.execute_script("arguments[0].click();", yes_button)

print("✅ Clicked YES to initiate workflow")

# Wait for form container to load
wait.until(EC.presence_of_element_located((By.ID, "form_instance_data")))



# Entry "CIF No" 
cif_no = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1059166284765204480"))
)
cif_no.clear()
cif_no.send_keys("1234567891012")
print("✅ CIF No filled: 1234567891012")


# Select "Workflow Created for" from dropdown
select_element = driver.find_element(By.ID, "form_instance_data_1637800332073373696")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'Clients of WBD';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'Clients of WBD' from Workflow Created for dropdown")


# Link Tracking No selection
link_tracking_no = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1059165558903148544"))
)
link_tracking_no.clear()
link_tracking_no.send_keys("1234567891012")
print("✅ Link Tracking No filled: 1234567891012")


# Entry date - fill with today's current date
today_date = datetime.now().strftime("%d-%m-%Y") 
Entry_date = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1059165624732749824"))
)
Entry_date.clear()
Entry_date.send_keys(today_date)
print(f"✅ Entry Date filled: {today_date}")



# Branch Name selection
branch_name = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1059165684027625472"))
)
branch_name.clear()
branch_name.send_keys("Dhanmondi")
print("✅ Branch Name filled: Dhanmondi")



# Hub Name selection
hub_name = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1059165768286998528"))
)
hub_name.clear()
hub_name.send_keys("Dhanmondi hub")
print("✅ Hub Name filled: Dhanmondi hub")


# Select "Loan account Status" In dropdown
select_element = driver.find_element(By.ID, "form_instance_data_1059165818337628160")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'Live';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'Live' from Loan account Status dropdown")

#Sanction Ref No selection
sanction_ref_no = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1059165908682936320"))
)
sanction_ref_no.clear()
sanction_ref_no.send_keys("1234567891012")
print("✅ Sanction Ref No filled: 1234567891012")



# Select "Sanction Date" In dropdown
today_date = datetime.now().strftime("%d-%m-%Y") 
sanction_date = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1059165966786629632"))
)
sanction_date.clear()
sanction_date.send_keys(today_date)
print(f"✅ Sanction Date filled: {today_date}")


# Select "Approval Authority" In dropdown
select_element = driver.find_element(By.ID, "form_instance_data_1059166140128825344")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'Management';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'Management' from Approval Authority dropdown")

# Entry "Name of the Client" 
name_of_client = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1059166266847137792"))
)
name_of_client.clear()
name_of_client.send_keys("alamin")
print("✅ Name of the Client filled: alamin")


# Select "Type of Facility" In dropdown
select_element = driver.find_element(By.ID, "form_instance_data_1059167015228411904")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'SBL';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'SBL' from Type of Facility dropdown")

# Entry "Total Limit(Funded+Non Funded)" 
total_limit = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1059167159617327104"))
)
total_limit.clear()
total_limit.send_keys("100000")
print("✅ Total Limit filled: 100000")



# Entry "Total Funded Limit" 
total_funded_limit = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1059167169893371904"))
)
total_funded_limit.clear()
total_funded_limit.send_keys("120000")
print("✅ Total Funded Limit filled: 120000")


# Entry "RM Name, Designation & RM Code" 
rm_info = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1059167289166794752"))
)
rm_info.clear()
rm_info.send_keys("test RM")
print("✅ RM Info filled: test RM")


#Select "Types of Client" from Dropdown 
select_element = driver.find_element(By.ID, "form_instance_data_1059167546172772352")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'Proprietorship Firm';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'Proprietorship Firm' from Types of Client dropdown")



#Select "Categories of loan" from Dropdown 
select_element = driver.find_element(By.ID, "form_instance_data_1059167667333632000")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'Bai-Muajjal';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'Bai-Muajjal' from Categories of loan dropdown")


#Select "Security Type" from Dropdown 
select_element = driver.find_element(By.ID, "form_instance_data_1059167676514963456")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'Lien  FDR';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'Lien  FDR' from Security Type dropdown")


# Entry "CL Status" 
cl_status = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_data_1059167923672715264"))
)
cl_status.clear()
cl_status.send_keys("Yes")
print("✅ CL Status filled: Yes")


#Select "Sanction Status" from Dropdown 
select_element = driver.find_element(By.ID, "form_instance_data_1059168673106759680")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'Renewed at current level';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'Renewed at current level' from Sanction Status dropdown")

sleep(5)  # Optional: Wait a bit before proceeding

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

doc_type_select = driver.find_element(By.ID, "metafield")
driver.execute_script("""
    var select = arguments[0];
    select.value = '1059171107862482944';  // Value for "001. CHO Sanction Lettermarked by the BM."
    $(select).trigger('change');
""", doc_type_select)
print("✅ Document Type selected: 001. CHO Sanction Lettermarked by the BM.")

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

# 2nd & 3rd file: each file must be processed ONE at a time
# (SELECT opens a modal -> pick Document Type -> Create Document -> next file)
# NOTE: after each Create Document the processed row is REMOVED from the page
# (after a short delay), so the remaining buttons shift - always click the FIRST one.

SELECT_XPATH = "//a[contains(@class,'add') and contains(., 'SELECT')]"

def wait_for_count_to_drop(previous_count, timeout=15):
    """Waits until the SELECT button count falls below previous_count (row removed after create)."""
    waited = 0
    while waited < timeout:
        current = len(driver.find_elements(By.XPATH, SELECT_XPATH))
        if current < previous_count:
            return current
        sleep(1)
        waited += 1
    return None  # count never dropped

def create_document_for_first_file(doc_type_value, doc_type_label):
    """Clicks the FIRST remaining SELECT button, fills its document type and creates the document."""
    select_buttons = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, SELECT_XPATH))
    )
    print(f"Found {len(select_buttons)} SELECT button(s)")

    file_select = select_buttons[0]  # first remaining (unprocessed) file
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", file_select)
    driver.execute_script("arguments[0].click();", file_select)
    print("✅ SELECT clicked for next file")

    doc_type_select = driver.find_element(By.ID, "metafield")
    driver.execute_script("""
        var select = arguments[0];
        select.value = arguments[1];
        $(select).trigger('change');
    """, doc_type_select, doc_type_value)
    print(f"✅ Document Type selected: {doc_type_label}")

    create_button = wait.until(
        EC.element_to_be_clickable((By.ID, "create-document-button"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", create_button)
    driver.execute_script("arguments[0].click();", create_button)
    print("✅ Create Document button clicked")


# Wait for the 1st file's (001) row to be removed after its Create Document
remaining = wait_for_count_to_drop(3)
if remaining is None:
    remaining = len(driver.find_elements(By.XPATH, SELECT_XPATH))
print(f"ℹ {remaining} SELECT button(s) remaining after 1st file")

# Process the remaining files (2nd & 3rd) - all with Document Type 002
while remaining:
    create_document_for_first_file(
        "1059171167266410496",
        "002. Branch Sanction Letter accepted by the client/borrower (signature verified by RM/BM)."
    )
    remaining = wait_for_count_to_drop(remaining)
    if remaining is None:
        break  # no more rows being removed - all files processed

print("✅ All remaining files processed with Document Type 002")



# ok_button = wait.until(
#     EC.element_to_be_clickable((By.XPATH, "//button[@data-bb-handler='main' and normalize-space()='OK']"))
# )

# driver.execute_script("arguments[0].click();", ok_button)

# print("✅ Success modal OK clicked")


# Wait for the Done button to be present
done_button = wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'view-active-step') and contains(@class,'btn')]"))
)

# Scroll into view
driver.execute_script("arguments[0].scrollIntoView(true);", done_button)

# Click using JS to bypass overlay
driver.execute_script("arguments[0].click();", done_button)

print("✅ Done button clicked via JS")



# ===================== Deferral Section =====================

# Select "Deferral Applicable" = Yes
select_element = driver.find_element(By.ID, "deferral_applicable_status")
driver.execute_script("""
    var select = arguments[0];
    select.value = 'yes';
    $(select).trigger('change');
""", select_element)
print("✅ Selected 'Yes' from Deferral Applicable dropdown")

sleep(2)

# Click "+ Add More" until 6 deferral rows exist (row 0 already exists, so 5 more needed)
# Verify each click actually created a row - retry the click if it didn't.
TARGET_DEFERRAL_ROWS = 6

def deferral_row_count():
    return len(driver.find_elements(
        By.XPATH, "//select[starts-with(@id, 'deferral_deferral_type_')]"
    ))

while deferral_row_count() < TARGET_DEFERRAL_ROWS:
    rows_before = deferral_row_count()

    add_more_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "btn_add_more_deferral"))
    )
    driver.execute_script("arguments[0].click();", add_more_btn)

    # wait up to 10s for the new row to appear
    for _ in range(10):
        if deferral_row_count() > rows_before:
            break
        sleep(1)
    else:
        raise RuntimeError(
            f"'+ Add More' did not create a new deferral row "
            f"(stuck at {rows_before} rows - the page may cap the row count)"
        )

print(f"✅ {deferral_row_count()} deferral rows ready")

# ---- Fill all 6 deferral rows ----
deferral_types = ["Mortgage", "Land Documents", "PPSSA", "Charge", "PG", "Others"]

today_date = datetime.now().strftime("%d-%m-%Y")
expiry_date = (datetime.now() + timedelta(days=5)).strftime("%d-%m-%Y")

# Use the row ids that actually exist (data-row-id on each type dropdown),
# instead of assuming they are 0..5
row_ids = [
    el.get_attribute("data-row-id")
    for el in driver.find_elements(
        By.XPATH, "//select[starts-with(@id, 'deferral_deferral_type_')]"
    )
]

for i, deferral_type in zip(row_ids, deferral_types):
    # Deferral Type (dropdown)
    type_select = driver.find_element(By.ID, f"deferral_deferral_type_{i}")
    driver.execute_script("""
        var select = arguments[0];
        select.value = arguments[1];
        $(select).trigger('change');
    """, type_select, deferral_type)
    print(f"✅ Deferral Type selected: {deferral_type}")

    # Deferral Approval Authority (text input)
    authority_input = driver.find_element(By.ID, f"deferral_approval_authority_{i}")
    authority_input.clear()
    authority_input.send_keys("Yes")

    # Date of Deferral (current date)
    date_of_deferral = driver.find_element(By.ID, f"date_of_deferral_{i}")
    date_of_deferral.clear()
    date_of_deferral.send_keys(today_date)
    date_of_deferral.send_keys(Keys.ESCAPE)  # close datepicker popup

    # Deferral Expiry Date (current date + 5 days)
    deferral_expiry = driver.find_element(By.ID, f"deferral_expiry_date_{i}")
    deferral_expiry.clear()
    deferral_expiry.send_keys(expiry_date)
    deferral_expiry.send_keys(Keys.ESCAPE)  # close datepicker popup

    # Present Status of Deferral (dropdown) - "Obtainted"
    status_select = driver.find_element(By.ID, f"deferral_present_status_{i}")
    driver.execute_script("""
        var select = arguments[0];
        select.value = arguments[1];
        $(select).trigger('change');
    """, status_select, "Obtainted")

    print(f"✅ Deferral row {i} filled: {deferral_type} | Deferral: {today_date} | Expiry: {expiry_date} | Status: Obtainted")


# ===================== Mouza Name & Jote No / Corresponding Dag No / Land Office Address Sections =====================

def add_and_fill_row(table_id, onclick_fn, values):
    """Clicks '+ Add More' once (via its onclick function), then fills the
    newly created (last) row by column order. Pass None for a column to leave it empty."""
    fn_name = onclick_fn.rstrip("()")

    # 1. Does the JS function even exist on this page?
    if not driver.execute_script(f"return typeof {fn_name} === 'function';"):
        raise RuntimeError(
            f"JS function {fn_name}() does not exist on this page - "
            f"the '{table_id}' section may not be loaded here"
        )

    # Count DATA rows (tr containing td cells) - these tables put the first
    # data row inside <thead> like the deferral table, so don't filter by tbody
    rows_before = driver.execute_script(f"""
        var t = document.getElementById('{table_id}');
        return t
            ? Array.from(t.querySelectorAll('tr')).filter(r => r.querySelector('td')).length
            : -1;
    """)

    # 2. Call it directly so JS errors are not swallowed silently
    js_result = driver.execute_script(f"""
        try {{
            {fn_name}();
            return 'ok';
        }} catch (e) {{
            return 'error: ' + e.message;
        }}
    """)

    if js_result != 'ok':
        raise RuntimeError(f"{fn_name}() threw a JavaScript error: {js_result}")

    # 3. Wait up to 10s for the new row to appear
    for _ in range(10):
        rows_now = driver.execute_script(f"""
            var t = document.getElementById('{table_id}');
            return t
                ? Array.from(t.querySelectorAll('tr')).filter(r => r.querySelector('td')).length
                : -1;
        """)
        if rows_now > rows_before:
            break
        sleep(1)
    else:
        # dump the table HTML so we can see what the function actually did
        table_html = driver.execute_script(
            f"var t = document.getElementById('{table_id}');"
            f"return t ? t.outerHTML : 'TABLE NOT FOUND';"
        )
        print(f"⚠ {table_id} HTML after click:\n{table_html}")
        raise RuntimeError(
            f"{fn_name}() ran without JS errors but added no row to {table_id} "
            f"(rows before: {rows_before})"
        )

    # last data row (tr containing td cells), wherever it lives (thead or tbody)
    row = driver.find_element(
        By.XPATH,
        f"(//table[@id='{table_id}']//tr[td])[last()]"
    )

    # visible inputs, selects and textareas in column order (hidden id inputs excluded)
    fields = row.find_elements(
        By.XPATH, ".//input[not(@type='hidden')] | .//select | .//textarea"
    )

    for field, value in zip(fields, values):
        if value is None:
            continue
        if field.tag_name == "select":
            driver.execute_script("""
                var select = arguments[0];
                select.value = arguments[1];
                $(select).trigger('change');
            """, field, value)
        else:
            driver.execute_script("arguments[0].value = arguments[1];", field, value)
            driver.execute_script("""
                var el = arguments[0];
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            """, field)


# ---- Mouza Name & Jote No table ----
# Columns: Land Area | Mouza Name | Jot No | Mutation No | Remarks
add_and_fill_row("MouzaJoteTable", "addMoreMouzaJote()", ["Dhaka", "Dhaka", "12", "M-12", "Jote No added"])
print("✅ Mouza Name & Jote No row filled: Dhaka | Dhaka | 12 | M-12 | Jote No added")

# ---- Corresponding Dag No table ----
# Columns: Mutation No | Land Area | CS | SA | RS | Others | Remarks  (RS & Others left empty)
add_and_fill_row("CorrespondingDagTable", "addMoreCorrespondingDag()", ["M-12", "Dhaka", "1980", "M-12", None, None, "Jote No added"])
print("✅ Corresponding Dag No row filled: M-12 | Dhaka | 1980 | M-12 | Remarks: Jote No added")

# ---- Land Office Address table ----
# Columns: Title Deed No. | Land Area | Address | Remarks
add_and_fill_row("LandOfficeTable", "addMoreLandOffice()", ["TD-21", "Dhaka", "Dhaka", "Land Office address added"])
print("✅ Land Office Address row filled: TD-21 | Dhaka | Dhaka | Land Office address added")

# ---- Rent Paid (Up to) table ----
# Columns: Mutation No./Jot No. | Land Area | Year up to | Remarks
add_and_fill_row("RendPaidUpToTable", "addMoreRendPaidUpTo()", ["M/J-34", "34", "2028", "rent added"])
print("✅ Rent Paid row filled: M/J-34 | 34 | 2028 | rent added")

# ---- Holding Tax Up To And Date table ----
# Columns: Owner of Land | Land/Flat Area | Paid Up to | Remarks
add_and_fill_row("HoldingTaxUpToDateTable", "addMoreHoldingTaxUpToDate()", ["Kabir", "34", "2028", "holding tax added"])
print("✅ Holding Tax row filled: Kabir | 34 | 2028 | holding tax added")

# ---- Types of Deed (Having SRO Token No), Deed No. & Date table ----
# Columns: SRO Token No | Deed Number | Date | Remarks
add_and_fill_row("TypeDeedTable", "addMoreTypeDeed()", ["258", "34", today_date, "types of Deed added"])
print(f"✅ Types of Deed row filled:  258 | 34 | {today_date} | types of Deed added")

# ---- Name of SRO table ----
# Columns: SRO Token No | Address/Name | Remarks
add_and_fill_row("SROTable", "addMoreSRO()", [" 258", "Dhaka, Bangladesh", "name of SRO added"])
print("✅ Name of SRO row filled: 258 | Dhaka, Bangladesh | name of SRO added")

# ---- Aging (Year) of SRO Token table ----
# Columns: SRO Token No | Deed Number | Year | Remarks
add_and_fill_row("AgingSROTokenTable", "addMoreSROToken()", ["258", "DN.89", "2026", "Aging added"])
print("✅ Aging of SRO Token row filled: 258 | DN.89 | 2026 | Aging added")



# doc_link = wait.until(
#     EC.element_to_be_clickable((
#         By.XPATH, "//a[contains(@class,'checklist-document-view') and contains(., '001. CHO Sanction Lettermarked by the BM.(1)')]"
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


# Try to find Close button with multiple selectors
# modal_closed = False
# try:
#     # Try exact match first
#     close_button = wait.until(
#         EC.element_to_be_clickable((
#             By.XPATH, "//button[@data-dismiss='modal' and normalize-space()='Close']"
#         ))
#     )
#     driver.execute_script("arguments[0].click();", close_button)
#     modal_closed = True
#     print("✅ Modal closed via Close button (exact match)")
# except TimeoutException:
#     try:
#         # Try button containing "Close" text
#         close_button = WebDriverWait(driver, 5).until(
#             EC.element_to_be_clickable((
#                 By.XPATH, "//button[@data-dismiss='modal' and contains(text(), 'Close')]"
#             ))
#         )
#         driver.execute_script("arguments[0].click();", close_button)
#         modal_closed = True
#         print("✅ Modal closed via Close button (contains)")
#     except TimeoutException:
#         try:
#             # Try generic modal close button (X icon)
#             close_button = WebDriverWait(driver, 5).until(
#                 EC.element_to_be_clickable((
#                     By.XPATH, "//button[contains(@class, 'close')]"
#                 ))
#             )
#             driver.execute_script("arguments[0].click();", close_button)
#             modal_closed = True
#             print("✅ Modal closed via X button")
#         except TimeoutException:
#             # Last resort: Press Escape key or use JS to hide modal
#             print("⚠ Close button not found, trying Escape key...")
#             from selenium.webdriver.common.keys import Keys
#             webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
#             sleep(1)

# if not modal_closed:
#     # Fallback: Use JavaScript to remove modal from DOM
#     driver.execute_script("""
#         if (arguments[0]) {
#             arguments[0].remove();
#         }
#     """, modal)
#     print("✅ Modal closed via JavaScript")

# print("✅ Modal closed successfully")

# Wait for the observation textarea to be present
observation_box = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_observation"))
)

# Scroll into view and focus
driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].focus();", observation_box)

# Clear and set the comment safely using JS
driver.execute_script("arguments[0].value = 'Document added. Proceed forward to Step - 2 Branch Checker(CAD)';", observation_box)

# Trigger input/change events so the system recognizes it
driver.execute_script("""
arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
""", observation_box)

print("✅ Comment added in observation box")

sleep(10)  # Optional: Wait a bit to ensure the comment is registered

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


input("Press Enter to continue...")  # Pause for user input


def force_logout():
    driver.get("http://27.147.184.165:8082/logout")
    wait.until(EC.url_contains("/login"))
    print("✅ Forced logout completed")

force_logout()


# Open login page
driver.get("http://27.147.184.165:8082/")


# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("anup.kumer")

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

sleep(5)

# Wait for the observation textarea to be present
observation_box = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_observation"))
)


# Scroll into view and focus
driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].focus();", observation_box)

# Clear and set the comment safely using JS
driver.execute_script("arguments[0].value = 'Proced forward to Branch Manager(CAD)';", observation_box)

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
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("Shaila")

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

sleep(5)

# Wait for the observation textarea to be present
observation_box = wait.until(
    EC.presence_of_element_located((By.ID, "form_instance_observation"))
)


# Scroll into view and focus
driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].focus();", observation_box)

# Clear and set the comment safely using JS
driver.execute_script("arguments[0].value = 'Proced forward to HO Checker(CAD)';", observation_box)

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
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("Shaila")

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
driver.execute_script("arguments[0].value = 'Proced forward to Ho Authorizer(CAD)';", observation_box)

# Trigger input/change events so the system recognizes it
driver.execute_script("""
arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
""", observation_box)

print("✅ Comment added in observation box")

sleep(2)  # Optional: Wait a bit to ensure the comment is registered

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

input("Check UI. Press Enter to close browser...")


force_logout()

print("✅ Paused")


# Open login page
driver.get("http://27.147.184.165:8082/")


# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("Shaila")

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
    print("✅ 'OK' clicked on Proceed Forward confirmation")

except TimeoutException:
    print("ℹ No confirmation alert appeared")

input("Check UI. Press Enter to close browser...")

