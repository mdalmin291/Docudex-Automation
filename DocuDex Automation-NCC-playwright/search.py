from datetime import datetime

from common import new_page, login, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD

with new_page() as page:
    # Step 1: Login
    login(page, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD)

    page.locator("xpath=//a[contains(., 'Documents')]").click()

    # Step 4: Click Upload Document (actually the Documents search link)
    page.locator("xpath=//a[contains(@href, '/documents/')]").first.click()

    # Generate same dynamic value used during upload
    today = datetime.now().strftime("%d.%m.%Y")
    search_text = f"test_document_pdf_{today}"

    search_input = page.locator("[name='localId']")
    search_input.fill(search_text)

    search_button = page.locator("xpath=//button[@type='submit' and contains(@class,'green')]")
    search_button.scroll_into_view_if_needed()
    search_button.click()

    print("✅ Search button clicked successfully")

    input("Check UI. Press Enter to close browser...")
