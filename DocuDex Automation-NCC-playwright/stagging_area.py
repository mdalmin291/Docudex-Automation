from common import new_page, login, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD, PDF_DIR

with new_page() as page:
    # Step 1: Login
    login(page, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD)

    page.locator("xpath=//a[contains(., 'Documents')]").click()

    # Step 4: Click Staging Area
    page.locator("xpath=//a[contains(@href, '/documents/staging/jobs')]").click()

    # ---------- Click New Job ----------
    new_job_button = page.locator(
        "xpath=//a[@title='New Job' and contains(@href,'/documents/staging/create-job')]"
    )
    new_job_button.scroll_into_view_if_needed()
    new_job_button.click()

    print("✅ New Job page opened")

    # ---------- Click Upload (open modal) ----------
    upload_modal_button = page.locator(
        "xpath=//a[contains(@class,'upload') and contains(text(),'Upload')]"
    )
    upload_modal_button.click()
    print("✅ Upload modal opened")

    # ---------- Attach multiple files ----------
    files = [
        PDF_DIR / "file-example_PDF_1MB.pdf",
        PDF_DIR / "file-example_PDF_500_kB.pdf",
        PDF_DIR / "file-sample_150kB.pdf",
    ]

    file_input = page.locator("input[type='file'][name='files[]']")
    file_input.set_input_files([str(f) for f in files])

    print("✅ Files attached successfully")

    # ---------- Click final Upload button ----------
    final_upload_button = page.locator("#fileupload-save-button")
    final_upload_button.scroll_into_view_if_needed()
    final_upload_button.click()

    print("✅ Final upload button clicked")

    # ---------- Click ALL SELECT buttons ----------
    select_buttons = page.locator("xpath=//a[contains(@class,'add') and contains(., 'SELECT')]")
    count = select_buttons.count()
    print(f"Found {count} files to select")

    for i in range(count):
        btn = select_buttons.nth(i)
        btn.scroll_into_view_if_needed()
        btn.click()

    print("✅ All files selected successfully")

    # ---------- Fill metadata ----------
    value_text = "test_doc_stagging_merged"

    page.locator("[name='localId']").fill(value_text)
    page.locator("[name='title']").fill(value_text)
    print("✅ Document ID and Name filled")

    # ---------- Select Department ----------
    page.select_option("#category_0", label="Centralised Unit for GB")
    print("✅ Department selected")

    # ---------- Click Create Document ----------
    create_btn = page.locator("#create-document-button")
    create_btn.scroll_into_view_if_needed()
    create_btn.click()

    print("✅ Create Document clicked")

    # Alert is auto-accepted by common.auto_accept_dialogs()

    # Now handle Bootbox success modal
    success_text = page.locator(".bootbox-body")
    success_text.wait_for(state="visible")
    print("✅ Success message:", success_text.inner_text())

    ok_button = page.locator("xpath=//div[contains(@class,'bootbox')]//button[text()='OK']")
    ok_button.click()
    print("✅ Success modal OK clicked")

    input("Check UI. Press Enter to close browser...")
