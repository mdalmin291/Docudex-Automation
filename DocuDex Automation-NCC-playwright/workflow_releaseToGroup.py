from common import (
    new_page,
    login,
    force_logout,
    initiate_account_opening_workflow,
    open_groups_list_and_search,
    accept_and_confirm,
    fill_observation,
    upload_and_create_tp_document,
    click_release_to_group,
    click_proceed_forward,
    search_workflow_by_tracking_no,
)

with new_page() as page:
    # Step 1: Initiate the Account Opening Process (Non-Individual) workflow as user 4948
    tracking_no = initiate_account_opening_workflow(page)

    # Step 2: Branch Checker (user 3769) uploads the TP document and releases it to group
    force_logout(page)
    login(page, "3769", "Ncc@1234")

    open_groups_list_and_search(page, tracking_no)
    accept_and_confirm(page)

    upload_and_create_tp_document(page, "Released to Group")
    click_release_to_group(page)

    search_workflow_by_tracking_no(page, tracking_no)

    # Step 3: HO Checker (user 3817) proceeds forward to Step - 3 (HO Checker)
    force_logout(page)
    login(page, "3817", "Ncc@1234")

    open_groups_list_and_search(page, tracking_no)
    accept_and_confirm(page)

    fill_observation(page, "Proceed forward to Step - 3 (HO Checker)")
    click_proceed_forward(page)

    search_workflow_by_tracking_no(page, tracking_no)

    input("Check UI. Press Enter to close browser...")
