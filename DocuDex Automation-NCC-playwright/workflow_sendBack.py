from common import (
    new_page,
    login,
    force_logout,
    initiate_account_opening_workflow,
    open_groups_list_and_search,
    accept_and_confirm,
    fill_observation,
    click_send_backward,
    click_proceed_forward,
    search_workflow_by_tracking_no,
)

with new_page() as page:
    # Step 1: Initiate the Account Opening Process (Non-Individual) workflow as user 4948
    tracking_no = initiate_account_opening_workflow(page)

    # Step 2: Branch Checker (user 3817) sends it backward to Step 1
    force_logout(page)
    login(page, "3817", "Ncc@1234")

    open_groups_list_and_search(page, tracking_no)
    accept_and_confirm(page)

    fill_observation(page, "Send Backward to Step 1")
    click_send_backward(page)

    search_workflow_by_tracking_no(page, tracking_no)

    # Step 3: Branch Maker (user 4948) proceeds forward to Step - 2
    force_logout(page)
    login(page, "4948", "Ncc@1234")

    open_groups_list_and_search(page, tracking_no)
    accept_and_confirm(page)

    fill_observation(page, "Proceed forward to Step - 2")
    click_proceed_forward(page)

    search_workflow_by_tracking_no(page, tracking_no)

    # Step 4: Branch Checker (user 3817) proceeds forward to Step-3
    force_logout(page)
    login(page, "3817", "Ncc@1234")

    open_groups_list_and_search(page, tracking_no)
    accept_and_confirm(page)

    fill_observation(page, "Proced Forward to Step-3")
    click_proceed_forward(page)

    search_workflow_by_tracking_no(page, tracking_no)

    # Step 5: HO Checker (user 2025) sends it back to step 2
    force_logout(page)
    login(page, "2025", "Ncc@1234")

    open_groups_list_and_search(page, tracking_no)
    accept_and_confirm(page)

    fill_observation(page, "Send back to step 2")
    click_send_backward(page)

    search_workflow_by_tracking_no(page, tracking_no)

    # Step 6: Branch Checker (user 3817) accepts it again
    force_logout(page)
    login(page, "3817", "Ncc@1234")

    open_groups_list_and_search(page, tracking_no)
    accept_and_confirm(page)

    input("Check UI. Press Enter to close browser...")
