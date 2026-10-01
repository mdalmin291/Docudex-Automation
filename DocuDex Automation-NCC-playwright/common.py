"""
Shared config and helpers for the DocuDex (NCC) Playwright automation scripts.

This mirrors what every original Selenium script in "DocuDex Automation-NCC"
was doing by hand (login, logout, alert handling, tracking-number file I/O,
demo file paths) so each converted script can stay short and focused on its
own workflow.
"""

from pathlib import Path
from contextlib import contextmanager
from datetime import datetime, timedelta

from playwright.sync_api import sync_playwright, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_URL = "http://203.76.124.126:5058"

# Default super-admin account used by login/search/upload/staging/branch/user scripts
SUPERADMIN_USERNAME = "superadmin"
SUPERADMIN_PASSWORD = "password"

DEFAULT_TIMEOUT_MS = 20_000

SCRIPT_DIR = Path(__file__).resolve().parent
DEMO_DIR = SCRIPT_DIR / "Demo file Upload for Testing"
PDF_DIR = DEMO_DIR / "PDF Folder"
OCR_DIR = DEMO_DIR / "OCR Test"

TRACKING_NO_FILE = SCRIPT_DIR / "tracking_no.txt"


# ---------------------------------------------------------------------------
# Browser / page setup
# ---------------------------------------------------------------------------

@contextmanager
def new_page(headless: bool = False):
    """Launch Chromium and yield a ready-to-use Page with dialogs auto-accepted."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(accept_downloads=True)
        context.set_default_timeout(DEFAULT_TIMEOUT_MS)
        page = context.new_page()
        auto_accept_dialogs(page)
        try:
            yield page
        finally:
            browser.close()


def auto_accept_dialogs(page: Page):
    """Auto-accept any JS alert/confirm (equivalent to the Selenium alert.accept() blocks)."""

    def _handler(dialog):
        print(f"⚠ Alert appeared: {dialog.message}")
        dialog.accept()
        print("✅ Alert accepted (OK clicked)")

    page.on("dialog", _handler)


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def login(page: Page, username: str, password: str, base_url: str = BASE_URL):
    page.goto(f"{base_url}/login")

    page.locator("[name='_username']").fill(username)
    page.locator("[name='_password']").fill(password)
    page.locator("button[type='submit']").click()

    # Wait for the Workflow menu (proof the dashboard loaded) instead of just the URL changing
    page.wait_for_selector("xpath=//a[contains(., 'Workflow')]")
    print(f"✅ Logged in as user {username}")


def force_logout(page: Page, base_url: str = BASE_URL):
    page.goto(f"{base_url}/logout")
    page.wait_for_url("**/login")
    print("✅ Forced logout completed")


# ---------------------------------------------------------------------------
# Tracking number file I/O
# ---------------------------------------------------------------------------

def save_tracking_no(tracking_no: str, path: Path = TRACKING_NO_FILE):
    path.write_text(tracking_no)
    print(f"💾 Tracking number saved to {path.name}")


def read_tracking_no(path: Path = TRACKING_NO_FILE) -> str:
    tracking_no = path.read_text().strip()
    print(f"📥 Loaded Tracking Number: {tracking_no}")
    return tracking_no


# ---------------------------------------------------------------------------
# Common workflow page actions (reused across workflow_*.py scripts)
# ---------------------------------------------------------------------------

def _js_click(locator):
    """Scroll into view + force click, mirroring the original scripts' JS-click-to-bypass-overlay pattern."""
    locator.scroll_into_view_if_needed()
    locator.click(force=True)


def search_workflow_by_tracking_no(page: Page, tracking_no: str):
    """Open 'All Workflow' from the Workflow menu and filter by tracking number."""
    _js_click(page.locator("xpath=//a[contains(@class,'dropdown-toggle') and contains(., 'Workflow')]"))
    _js_click(page.locator("xpath=//a[@href='/workflow/list/all']"))
    print("✅ Navigated to All Workflow page")

    tracking_input = page.locator("#form_workflow_filter_workflow")
    tracking_input.fill(tracking_no)
    print(f"✅ Tracking Number '{tracking_no}' entered in search box")

    _js_click(page.locator("xpath=//button[contains(text(),'Search') or contains(text(),'Filter')]"))
    print("✅ Search executed, workflow filtered by Tracking Number")


def open_groups_list_and_search(page: Page, tracking_no: str, base_url: str = BASE_URL):
    """Go to /workflow/groups-list and filter by tracking number."""
    page.goto(f"{base_url}/workflow/groups-list")
    page.wait_for_selector("body")
    print("✅ Groups Workflow page loaded")

    tracking_input = page.locator("#form_workflow_filter_workflow")
    tracking_input.fill(tracking_no)
    print("✅ Tracking number entered")

    _js_click(page.locator("xpath=//button[contains(text(),'Search') or contains(text(),'Filter')]"))
    print("✅ Search executed successfully")


def accept_and_confirm(page: Page):
    """Click the Accept link in the groups list row, then Confirm in the popup."""
    _js_click(page.locator("xpath=//a[contains(@class,'accept') and contains(text(),'Accept')]"))
    print("✅ Accept button clicked")

    _js_click(page.locator("xpath=//a[contains(@class,'confirm')]"))
    print("✅ Confirm button clicked")


def fill_observation(page: Page, comment: str):
    """Fill the workflow observation/comment textarea (it's populated via JS in the UI)."""
    observation_box = page.locator("#form_instance_observation")
    observation_box.scroll_into_view_if_needed()
    observation_box.fill(comment)
    print("✅ Comment added in observation box")


# ---------------------------------------------------------------------------
# Full "Account Opening Process (Non-Individual)" initiation flow
# ---------------------------------------------------------------------------
# Shared by workflow_initiate.py, workflow_reassign.py, workflow_releaseToGroup.py,
# workflow_sendBack.py and workflow_skip.py, which all start with this exact
# sequence (start workflow -> fill form -> upload AOF document -> proceed
# forward to Step-2) before branching into their own step-specific actions.

def initiate_account_opening_workflow(page: Page, username: str = "4948", password: str = "Ncc@1234") -> str:
    login(page, username, password)

    # Open Workflow menu -> New Workflow
    _js_click(page.locator("xpath=//a[contains(., 'Workflow')]"))
    print("✅ Workflow menu opened via JS")

    _js_click(page.locator("xpath=//a[contains(@href, '/workflow/template/active-list')]"))
    print("✅ Clicked on New Workflow")

    row = page.locator(
        "xpath=//tr[td[contains(text(),'Account Opening Process (Non-Individual)')]]"
    )
    row.wait_for()
    print("✅ Workflow row found")

    _js_click(row.locator("xpath=.//a[contains(@class,'start')]"))
    print("✅ Start button clicked for Account Opening Process")

    _js_click(page.locator("xpath=//button[@data-bb-handler='confirm' and normalize-space()='Yes']"))
    print("✅ Clicked YES to initiate workflow")

    page.wait_for_selector("#form_instance_data")

    page.locator("#form_instance_data_1850493788523335680").fill("Test Customer alamin")
    page.locator("#form_instance_data_1850493830621564928").fill("CIF-1234")
    page.locator("#form_instance_data_1850493914163712000").fill("AC-6543")
    page.locator("#form_instance_data_1850494046993125376").fill("Savings Account")
    print("✅ Workflow initiate form filled successfully")

    _js_click(page.locator("#btn_upload_to_staging"))
    print("✅ Clicked Upload button (Go to staging)")

    _js_click(page.locator("xpath=//a[contains(text(), 'Upload File') or contains(., 'Upload File')]"))
    print("✅ Upload modal opened")

    files = [
        PDF_DIR / "file-example_PDF_1MB.pdf",
        PDF_DIR / "file-example_PDF_500_kB.pdf",
        PDF_DIR / "file-sample_150kB.pdf",
    ]
    page.locator("input[type='file'][name='files[]']").set_input_files([str(f) for f in files])
    print("✅ Files attached successfully")

    _js_click(page.locator("#fileupload-save-button"))
    print("✅ Final upload button clicked")

    select_buttons = page.locator("xpath=//a[contains(@class,'add') and contains(., 'SELECT')]")
    select_buttons.first.wait_for()
    print(f"Found {select_buttons.count()} SELECT button(s)")
    _js_click(select_buttons.first)
    print("✅ First file SELECT clicked")

    page.locator("[name='localId']").fill("Aof")
    print("✅ Document ID filled")

    page.locator("#document-title").fill("Aof")
    print("✅ Document Name filled")

    page.select_option("#metafield", label="Account Opening Form (AOF)")
    print("✅ Document Type selected: Account Opening Form (AOF)")

    _js_click(page.locator("#create-document-button"))
    print("✅ Create Document button clicked")

    _js_click(page.locator("xpath=//button[@data-bb-handler='main' and normalize-space()='OK']"))
    print("✅ Success modal OK clicked")

    done_button = page.locator("xpath=//a[contains(@href,'view-active-step') and contains(@class,'btn')]")
    done_button.wait_for()
    _js_click(done_button)
    print("✅ Done button clicked via JS")

    doc_link = page.locator(
        "xpath=//a[contains(@class,'checklist-document-view') and contains(., 'Account Opening Form')]"
    )
    _js_click(doc_link)
    print("✅ Document clicked (preview modal opened)")

    modal = page.locator("#document-preview")
    modal.wait_for(state="visible")
    print("✅ Document modal opened")

    modal.evaluate(
        "el => { const b = el.querySelector('.modal-body'); if (b) b.scrollTop = b.scrollHeight; }"
    )
    print("✅ Modal scrolled to bottom")

    _js_click(page.locator("xpath=//button[@data-dismiss='modal' and normalize-space()='Close']"))
    print("✅ Modal closed successfully")

    fill_observation(page, "Document added. Proceed forward to Step - 2 (Branch Checker)")

    _js_click(page.locator("xpath=//button[contains(text(),'Proceed Forward')]"))
    print("✅ 'Proceed Forward' button clicked successfully")

    workflow_table = page.locator(
        "xpath=//h3[text()='Workflow Successfully Started']/following-sibling::table"
    )
    workflow_table.wait_for()

    tracking_no = workflow_table.locator(
        "xpath=.//tr[th[text()='Tracking Number:']]/td/span"
    ).inner_text()
    print(f"✅ Tracking Number extracted: {tracking_no}")

    save_tracking_no(tracking_no)
    search_workflow_by_tracking_no(page, tracking_no)

    return tracking_no


# ---------------------------------------------------------------------------
# Step-action helpers shared across workflow_2nd_Step / 3rd_Step / reassign /
# releaseToGroup / sendBack / skip
# ---------------------------------------------------------------------------

def click_proceed_forward(page: Page):
    _js_click(page.locator("xpath=//button[contains(text(),'Proceed Forward')]"))
    print("✅ 'Proceed Forward' button clicked successfully")


def click_send_backward(page: Page):
    _js_click(page.locator("xpath=//button[contains(text(),'Send Backward')]"))
    print("✅ 'Send Backward' button clicked successfully")


def click_complete_workflow(page: Page):
    _js_click(page.locator("xpath=//button[contains(text(),'Complete Workflow')]"))
    print("✅ 'Complete Workflow' button clicked successfully")


def click_release_to_group(page: Page):
    _js_click(page.locator("xpath=//button[contains(text(),'Release to group')]"))
    print("✅ 'Released To Group' button clicked successfully")


def upload_and_create_tp_document(page: Page, observation_comment: str):
    """Upload the attached file and create it as a 'Transaction Profile (TP)' document
    for the currently active workflow step, then fill the observation comment
    (the caller clicks whichever action button follows: Proceed Forward / Release to group / ...)."""
    _js_click(page.locator("#btn_upload_to_staging"))
    print("✅ Clicked Upload button (Go to staging)")

    select_buttons = page.locator("xpath=//a[contains(@class,'add') and contains(., 'SELECT')]")
    select_buttons.first.wait_for()
    print(f"Found {select_buttons.count()} SELECT button(s)")
    _js_click(select_buttons.first)
    print("✅ First file SELECT clicked")

    page.locator("[name='localId']").fill("TP")
    print("✅ Document ID filled")

    page.locator("#document-title").fill("TP")
    print("✅ Document Name filled")

    page.select_option("#metafield", label="Transaction Profile (TP)")
    print("✅ Document Type selected: Transaction Profile (TP)")

    _js_click(page.locator("#create-document-button"))
    print("✅ Create Document button clicked")

    _js_click(page.locator("xpath=//button[@data-bb-handler='main' and normalize-space()='OK']"))
    print("✅ Success modal OK clicked")

    done_button = page.locator("xpath=//a[contains(@href,'view-active-step') and contains(@class,'btn')]")
    done_button.wait_for()
    _js_click(done_button)
    print("✅ Done button clicked via JS")

    doc_link = page.locator(
        "xpath=//a[contains(@class,'checklist-document-view') and contains(., 'Transaction Profile (TP) (TP)')]"
    )
    _js_click(doc_link)
    print("✅ Document clicked (preview modal opened)")

    modal = page.locator("#document-preview")
    modal.wait_for(state="visible")
    print("✅ Document modal opened")

    modal.evaluate(
        "el => { const b = el.querySelector('.modal-body'); if (b) b.scrollTop = b.scrollHeight; }"
    )
    print("✅ Modal scrolled to bottom")

    _js_click(page.locator("xpath=//button[@data-dismiss='modal' and normalize-space()='Close']"))
    print("✅ Modal closed successfully")

    fill_observation(page, observation_comment)


# ---------------------------------------------------------------------------
# Re-assign / Skip-to-step helpers (workflow_reassign.py, workflow_skip.py)
# ---------------------------------------------------------------------------

def open_reassign_dropdown(page: Page):
    _js_click(page.locator("xpath=//div[@id='btn-re-assign-to']//a[contains(@class,'btn')]"))
    print("✅ Re-assign dropdown opened")


def open_skip_to_step_dropdown(page: Page):
    _js_click(page.locator("xpath=//a[contains(@class,'btn') and contains(., 'Skip to step')]"))
    print("✅ Skip to step dropdown opened")


def click_move_workflow_option(page: Page, step_text: str):
    option = page.locator(
        f"xpath=//a[contains(@class,'move-workflow') and contains(., '{step_text}')]"
    )
    _js_click(option)
    print(f"✅ Moved workflow to: {step_text}")


def confirm_select_branch(page: Page):
    select_button = page.locator("#select-step-branch")
    _js_click(select_button)
    print("✅ Select button clicked successfully")


# ---------------------------------------------------------------------------
# Document property / version-update helpers
# ---------------------------------------------------------------------------
# Shared by the three document_property_action_and_version_update_*.py scripts.

DOCUMENT_USER = "2979"
DOCUMENT_PASSWORD = "Ncc@1234"


def upload_and_search_test_document(page: Page) -> str:
    """Upload a fresh test PDF, then search for and open it from the Documents list.
    Returns the generated document name (also used as the Document ID)."""
    page.goto(f"{BASE_URL}/documents/upload")
    page.wait_for_selector("body")

    file_path = PDF_DIR / "file-sample_150kB.pdf"
    page.locator("input[type='file'][name='files[]']").set_input_files(str(file_path))

    today = datetime.now().strftime("%d.%m.%Y")
    value_text = f"test_document_pdf_{today}"

    page.locator("[name='localId']").fill(value_text)
    print("✅ Document ID filled")

    page.locator("[name='title']").fill(value_text)
    print("✅ Document Name filled")

    page.select_option("#category_0", label="Centralised Unit for GB")

    save_button = page.locator("xpath=//button[contains(@class,'document-upload')]")
    _js_click(save_button)
    print("✅ Upload and Save clicked successfully")

    try:
        ok_button = page.locator(
            "xpath=//div[contains(@class,'bootbox')]//button[normalize-space()='OK']"
        )
        ok_button.wait_for(state="visible", timeout=10_000)
        _js_click(ok_button)
        print("✅ Bootbox OK clicked")
    except PlaywrightTimeoutError:
        print("ℹ Bootbox modal did not appear")

    page.locator("xpath=//a[contains(., 'Documents')]").click()
    page.locator("xpath=//a[contains(@href, '/documents/')]").first.click()

    search_input = page.locator("[name='localId']")
    search_input.fill(value_text)

    search_button = page.locator("xpath=//button[@type='submit' and contains(@class,'green')]")
    _js_click(search_button)
    print("✅ Search button clicked successfully")

    document_link = page.locator(
        f"xpath=//tr[contains(@class,'doc')]//a[normalize-space()='{value_text}']"
    )
    _js_click(document_link)
    print("✅ Document opened successfully")

    return value_text


def download_and_send_for_review(page: Page):
    download_button = page.locator("xpath=//a[contains(@href, '/documents/file-download/')]")
    _js_click(download_button)
    print("✅ Download button clicked")

    send_for_review = page.locator("#send-for-review-button")
    _js_click(send_for_review)
    print("✅ Review action confirmed")

    page.select_option("#review_form_request_for", label="Rajib Kumar Chakraborty")
    print("✅ User selected: Rajib Kumar Chakraborty")

    page.locator("#review_form_note").fill("Please Review this Document")
    print("✅ Description added")

    send_button = page.locator(
        "xpath=//div[contains(@class,'modal-footer')]"
        "//button[contains(@class,'update-document-data') and contains(text(),'Send')]"
    )
    _js_click(send_button)
    print("✅ Send button clicked")


def edit_properties_and_extend_expiry(page: Page, description: str, extend_days: int = 7):
    _js_click(page.locator("#edit-Properties-button"))
    print("✅ Edit Properties clicked")

    edit_modal = page.locator("#Edit-Properties")
    edit_modal.wait_for(state="visible")
    print("✅ Edit Properties modal opened")

    page.locator("#document_version_description").fill(description)
    print("✅ Description updated")

    create_date_input = page.locator("#document_document_createDate")
    create_date_str = create_date_input.input_value()
    create_date = datetime.strptime(create_date_str, "%Y-%m-%d")
    print(f"📅 Create Date: {create_date_str}")

    expire_date_str = (create_date + timedelta(days=extend_days)).strftime("%Y-%m-%d")
    print(f"📅 Expire Date (calculated): {expire_date_str}")

    expire_input = page.locator("#document_document_expireDate")
    expire_input.evaluate(
        "(el, value) => { el.removeAttribute('readonly'); el.value = value; }",
        expire_date_str,
    )
    print("✅ Expire Date updated")

    save_button = page.locator(
        "xpath=//div[contains(@class,'modal') and contains(@class,'in')]"
        "//button[@data-form='#form-update-document-property' and normalize-space()='Save']"
    )
    save_button.scroll_into_view_if_needed()
    save_button.evaluate(
        "el => el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }))"
    )
    print("✅ Save triggered correctly")

    try:
        edit_modal.wait_for(state="hidden", timeout=10_000)
        print("✅ Modal closed — Save confirmed")
    except PlaywrightTimeoutError:
        print("⚠ Modal did not close — closing manually")
        page.evaluate(
            """
            () => {
                const modal = document.getElementById('Edit-Properties');
                if (modal) { modal.classList.remove('in'); modal.style.display = 'none'; }
                const backdrop = document.querySelector('.modal-backdrop');
                if (backdrop) backdrop.remove();
                document.body.classList.remove('modal-open');
            }
            """
        )
        print("✅ Modal force-closed")


def upload_new_version(page: Page, file_path, notes: str):
    """Click 'Upload New Version', attach a file, add a comment and Save."""
    upload_version_btn = page.locator("xpath=//a[.//text()[contains(., 'Upload New Version')]]")
    _js_click(upload_version_btn)
    print("✅ Upload New Version clicked")

    page.locator("#fileupload").set_input_files(str(file_path))
    print("✅ File uploaded successfully")

    page.locator("[name='notes']").fill(notes)
    print("✅ Comment added")

    save_button = page.locator("xpath=//button[contains(., 'Save')]")
    _js_click(save_button)
    print("✅ Save clicked for new version")


def upload_second_version_for_merge(page: Page, file_path):
    """Click 'Upload New Version' again, attach the second file, and select 'Merge with latest version'."""
    upload_version_btn = page.locator("xpath=//a[.//text()[contains(., 'Upload New Version')]]")
    _js_click(upload_version_btn)
    print("✅ Upload 2nd New Version clicked")

    page.locator("#fileupload").set_input_files(str(file_path))
    print("✅ 2nd File uploaded successfully")

    merge_radio = page.locator("xpath=//label[contains(normalize-space(),'Merge this with latest version')]")
    merge_radio.wait_for(state="visible", timeout=60_000)
    _js_click(merge_radio)
    print("✅ Selected merge via label")


def choose_merge_position(page: Page, position_label_text: str):
    position_radio = page.locator(f"xpath=//label[contains(normalize-space(),'{position_label_text}')]")
    position_radio.wait_for(state="visible", timeout=60_000)
    _js_click(position_radio)
    print(f"✅ Selected '{position_label_text}'")


def choose_insert_after_page(page: Page, page_number: str):
    all_pages_label = page.locator("xpath=//label[contains(normalize-space(), 'All Pages')]")
    all_pages_label.wait_for(state="visible", timeout=30_000)
    _js_click(all_pages_label)
    print("✅ Selected 'All Pages'")

    after_page_label = page.locator("xpath=//label[contains(normalize-space(), 'After page')]")
    after_page_label.wait_for(state="visible", timeout=30_000)
    _js_click(after_page_label)
    print("✅ Selected 'After page'")

    page_input = page.locator("[name='insert_after_page']")
    page_input.fill(page_number)
    print(f"✅ Page number entered: {page_number}")


def choose_minor_changes_and_save(page: Page, notes: str):
    minor_radio = page.locator("xpath=//label[contains(normalize-space(),'Minor changes')]")
    minor_radio.wait_for(state="visible", timeout=60_000)
    _js_click(minor_radio)
    print("✅ Selected 'Minor changes (2.1)'")

    page.locator("[name='notes']").fill(notes)
    print("✅ 2nd Comment added")

    save_button = page.locator("xpath=//button[contains(., 'Save')]")
    _js_click(save_button)
    print("✅ Save clicked for new version")
