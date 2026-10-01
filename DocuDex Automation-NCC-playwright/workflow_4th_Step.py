from common import (
    new_page,
    login,
    read_tracking_no,
    open_groups_list_and_search,
    accept_and_confirm,
    fill_observation,
    click_complete_workflow,
    _js_click,
    BASE_URL,
)

with new_page() as page:
    login(page, "3524", "Ncc@1234")

    tracking_no = read_tracking_no()
    open_groups_list_and_search(page, tracking_no)

    accept_and_confirm(page)

    fill_observation(page, "Checked Everything looks okay.Workflow Completed")
    click_complete_workflow(page)

    # Open Workflow menu -> All Workflow
    _js_click(page.locator("xpath=//a[contains(@class,'dropdown-toggle') and contains(., 'Workflow')]"))
    _js_click(page.locator("xpath=//a[@href='/workflow/list/all']"))
    print("✅ Navigated to All Workflow page")

    # Switch the "Archived/Completed" toggle to YES
    _js_click(page.locator("xpath=//label[@for='form_workflow_filter_completed']"))
    print("✅ Archived toggle switched to YES")

    tracking_input = page.locator("#form_workflow_filter_workflow")
    tracking_input.fill(tracking_no)
    print(f"✅ Tracking Number '{tracking_no}' entered in search box")

    _js_click(page.locator("xpath=//button[contains(text(),'Search') or contains(text(),'Filter')]"))
    print("✅ Search executed, workflow filtered by Tracking Number")

    # Wait until at least one result row appears after search
    page.locator("xpath=//table//tr[.//a[contains(@href,'/workflow/')]]").first.wait_for()
    print("✅ Result row loaded")

    tracking_link = page.locator(f"xpath=//a[@href and normalize-space(text())='{tracking_no}']")
    _js_click(tracking_link)
    print(f"✅ Clicked tracking number: {tracking_no}")

    # Navigate to Document Search page
    page.goto(f"{BASE_URL}/documents/")
    page.wait_for_selector("body")
    print("✅ Search Document page loaded")

    tracking_no = read_tracking_no()

    tracking_input = page.locator("#typeahead_example_3")
    tracking_input.fill(tracking_no)
    print("✅ Tracking number entered")

    _js_click(page.locator("xpath=//button[contains(text(),'Search') or contains(text(),'Filter')]"))
    print("✅ Search executed successfully")

    input("Check UI. Press Enter to close browser...")
