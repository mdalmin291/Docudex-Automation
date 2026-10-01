from common import (
    new_page,
    login,
    force_logout,
    initiate_account_opening_workflow,
    open_groups_list_and_search,
    accept_and_confirm,
    fill_observation,
    click_proceed_forward,
    search_workflow_by_tracking_no,
    open_reassign_dropdown,
    click_move_workflow_option,
    confirm_select_branch,
)

with new_page() as page:
    # Step 1: Initiate the Account Opening Process (Non-Individual) workflow as user 4948
    tracking_no = initiate_account_opening_workflow(page)

    # Step 2: Branch Checker (user 3817) proceeds forward
    force_logout(page)
    login(page, "3817", "Ncc@1234")

    open_groups_list_and_search(page, tracking_no)
    accept_and_confirm(page)

    fill_observation(page, "Proced forward to Step 3")
    click_proceed_forward(page)

    search_workflow_by_tracking_no(page, tracking_no)

    # Step 3: HO Checker (user 2025) re-assigns back to Branch Maker (Step-1)
    force_logout(page)
    login(page, "2025", "Ncc@1234")

    open_groups_list_and_search(page, tracking_no)
    accept_and_confirm(page)

    fill_observation(page, "Reassign to Step -1")

    open_reassign_dropdown(page)
    click_move_workflow_option(page, "Branch Maker")
    page.wait_for_timeout(2000)
    confirm_select_branch(page)

    search_workflow_by_tracking_no(page, tracking_no)

    # Step 4: Branch Maker (user 4948) proceeds forward again to Step-2
    force_logout(page)
    login(page, "4948", "Ncc@1234")

    open_groups_list_and_search(page, tracking_no)
    accept_and_confirm(page)

    fill_observation(page, "Proced Forward to Step-2")
    click_proceed_forward(page)

    search_workflow_by_tracking_no(page, tracking_no)

    input("Check UI. Press Enter to close browser...")
