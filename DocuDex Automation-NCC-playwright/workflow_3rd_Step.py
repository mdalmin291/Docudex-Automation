from common import (
    new_page,
    login,
    read_tracking_no,
    open_groups_list_and_search,
    accept_and_confirm,
    fill_observation,
    click_proceed_forward,
    search_workflow_by_tracking_no,
)

with new_page() as page:
    login(page, "2025", "Ncc@1234")

    tracking_no = read_tracking_no()
    open_groups_list_and_search(page, tracking_no)

    accept_and_confirm(page)

    fill_observation(page, "Checked Proceed forward to Step - 3 (HO Checker)")
    click_proceed_forward(page)

    search_workflow_by_tracking_no(page, tracking_no)

    input("Check UI. Press Enter to close browser...")
