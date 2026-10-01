from common import new_page, initiate_account_opening_workflow

with new_page() as page:
    tracking_no = initiate_account_opening_workflow(page)

    input("Check UI. Press Enter to close browser...")
