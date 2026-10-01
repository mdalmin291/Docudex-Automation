import random

from common import new_page, login, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD, BASE_URL

with new_page() as page:
    # Step 1: Login
    login(page, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD)

    # Navigate to Branch page
    page.goto(f"{BASE_URL}/configuration/branch")
    page.wait_for_selector("body")
    print("✅ Search Document page loaded")

    # Branch Create
    create_user_btn = page.locator("xpath=//a[.//text()[contains(.,'Add User')]]")
    create_user_btn.scroll_into_view_if_needed()
    create_user_btn.click()

    print("✅ Create Branch clicked")

    upazilas = [
        "Dhanmondi", "Mirpur", "Uttara", "Gulshan", "Banani",
        "Mohammadpur", "Savar", "Keraniganj", "Narayanganj",
        "Gazipur", "Tongi", "Pabna Sadar", "Ishwardi",
        "Rajshahi Sadar", "Boalia", "Motijheel", "Tejgaon",
        "Coxs Bazar Sadar", "Teknaf", "Ukhiya",
        "Chattogram Sadar", "Pahartali", "Panchlaish",
        "Sylhet Sadar", "Beanibazar", "Golapganj",
        "Cumilla Sadar", "Debidwar", "Daudkandi",
        "Khulna Sadar", "Sonadanga", "Khalishpur",
    ]

    selected_upazila = random.choice(upazilas)
    branch_name = f"{selected_upazila}"

    # Generate Branch Code (6 digit realistic format)
    branch_code = str(random.randint(100000, 999999))

    print(f"🏷 Generated Branch Name: {branch_name}")
    print(f"🔢 Branch Code: {branch_code}")

    branch_input = page.locator("#docudex_bundle_branchbundle_branch_name")
    branch_input.fill(branch_name)
    print("✅ Branch name entered successfully")

    branch_code_input = page.locator("#docudex_bundle_branchbundle_branch_code")
    branch_code_input.fill(branch_code)
    print("✅ Branch code entered successfully")

    create_branch_btn = page.locator("#docudex_bundle_branchbundle_branch_submit")
    create_branch_btn.scroll_into_view_if_needed()
    create_branch_btn.click()
    print("✅ Create Branch button clicked")

    # Reload page
    page.reload()
    page.wait_for_selector("body")
    print("🔄 Page refreshed and ready")

    input("Check UI. Press Enter to close browser...")
