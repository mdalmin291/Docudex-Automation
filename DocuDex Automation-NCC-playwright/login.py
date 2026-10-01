from common import new_page, login, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD

with new_page() as page:
    login(page, SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD)

    print("✅ Successfully logged in")
    
    input("Press Enter to close browser...")
