import random

from common import new_page, login, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD, BASE_URL

with new_page() as page:
    # Step 1: Login
    login(page, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD)

    # Navigate to Users page
    page.goto(f"{BASE_URL}/configuration/users")
    page.wait_for_selector("body")
    print("✅ Users page loaded")

    # User Create
    create_user_btn = page.locator("xpath=//a[.//text()[contains(.,'Add User')]]")
    create_user_btn.scroll_into_view_if_needed()
    create_user_btn.click()
    print("✅ Create User clicked")

    def generate_user_id():
        return str(random.randint(10000, 99999))

    def generate_name():
        names = ["Akash", "Rafi", "Tanvir", "Nayeem", "Fahim", "Imran", "Shuvo", "Hasan"]
        return random.choice(names) + str(random.randint(10, 99))

    # Generate dynamic data
    user_id = generate_user_id()
    full_name = generate_name()
    email = f"{full_name.lower()}@gmail.com"

    print("Generated:", user_id, full_name, email)

    # Username
    page.locator("#manage_user_username").fill(user_id)

    # Full name
    page.locator("#manage_user_fullName").fill(full_name)

    # Email
    page.locator("#manage_user_email").fill(email)

    # Department section
    page.wait_for_selector("#manage_user_profile_memberOfDepartments")
    dept_checkbox = page.locator("[name='manage_user[profile][memberOfDepartments][]']").first
    dept_checkbox.check(force=True)
    print("✅ Department selected")

    # Password
    page.locator("#manage_user_plainPassword_first").fill("Ncc@1234")
    page.locator("#manage_user_plainPassword_second").fill("Ncc@1234")

    # Select all department groups
    group_values = page.locator("#department-groups option").evaluate_all(
        "options => options.map(o => o.value)"
    )
    page.select_option("#department-groups", group_values)
    print("✅ All groups selected")

    # Scroll to Create button and click
    create_btn = page.locator("xpath=//button[contains(.,'Create User')]")
    create_btn.scroll_into_view_if_needed()
    create_btn.click()

    print("✅ User created successfully")

    input("Check UI. Press Enter to close browser...")
