from datetime import datetime

from common import new_page, login, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD, PDF_DIR

with new_page() as page:
    # Step 1: Login
    login(page, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD)

    # Step 3: Click Documents menu
    page.locator("xpath=//a[contains(., 'Documents')]").click()

    # Step 4: Click Upload Document
    page.locator("xpath=//a[contains(@href, '/documents/upload')]").click()

    # Step 5: Confirm upload page loaded
    page.wait_for_url("**/documents/upload")

    file_path = PDF_DIR / "file-sample_150kB.pdf"

    file_input = page.locator("input[type='file'][name='files[]']")
    file_input.set_input_files(str(file_path))

    # ---------- Generate dynamic value ----------
    today = datetime.now().strftime("%d.%m.%Y")
    value_text = f"test_document_pdf_{today}"

    # ---------- Fill Document ID ----------
    page.locator("[name='localId']").fill(value_text)
    print("✅ Document ID filled")

    # ---------- Fill Document Name ----------
    page.locator("[name='title']").fill(value_text)
    print("✅ Document Name filled")

    # ---------- Select Department ----------
    page.select_option("#category_0", label="Centralised Unit for GB")

    # Click on save button
    save_button = page.locator("xpath=//button[contains(@class,'document-upload')]")
    save_button.scroll_into_view_if_needed()
    save_button.click()

    print("✅ Upload and Save clicked successfully")

    input("Check UI. Press Enter to close browser...")
