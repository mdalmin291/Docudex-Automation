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
    open_skip_to_step_dropdown,
    click_move_workflow_option,
    confirm_select_branch,
)

with new_page() as page:
    # Step 1: Initiate the Account Opening Process (Non-Individual) workflow as user 4948
    tracking_no = initiate_account_opening_workflow(page)

    # Step 2: Branch Checker (user 3817) skips straight to Ho Authorizer (Step-4)
    force_logout(page)
    login(page, "3817", "Ncc@1234")

    open_groups_list_and_search(page, tracking_no)
    accept_and_confirm(page)

    fill_observation(page, "Skip to Ho Authorizer (Step-4)")

    open_skip_to_step_dropdown(page)
    click_move_workflow_option(page, "Ho Authorizer")

    page.locator("#workflow-step-branch").wait_for(state="visible")
    print("✅ Select Branch modal is visible")

    confirm_select_branch(page)
    print("✅ Select button clicked — workflow skipped successfully")

    search_workflow_by_tracking_no(page, tracking_no)

    # Step 3: HO Authorizer (user 3524) proceeds forward, then re-assigns back to Branch Maker (Step-1)
    force_logout(page)
    login(page, "3524", "Ncc@1234")

    open_groups_list_and_search(page, tracking_no)
    accept_and_confirm(page)

    fill_observation(page, "Reassign to Step -1")
    click_proceed_forward(page)

    click_move_workflow_option(page, "Branch Maker")
    page.wait_for_timeout(2000)
    confirm_select_branch(page)

    search_workflow_by_tracking_no(page, tracking_no)

    # Step 4: Branch Maker (user 4948) proceeds forward to Step-2
    force_logout(page)
    login(page, "4948", "Ncc@1234")

    open_groups_list_and_search(page, tracking_no)
    accept_and_confirm(page)

    fill_observation(page, "Proced Forward to Step-2")
    click_proceed_forward(page)

    input("Check UI. Press Enter to close browser...")
