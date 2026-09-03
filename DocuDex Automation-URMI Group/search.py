from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

# Step 1: Login
driver.get("http://203.76.124.126:5058/login")

wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("superadmin")
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("password")

wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

documents_menu = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Documents')]"))
)
documents_menu.click()

# Step 4: Click Upload Document
search_link = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/documents/')]"))    
)
search_link.click()


# Generate same dynamic value used during upload
today = datetime.now().strftime("%d.%m.%Y")
search_text = f"test_document_pdf_{today}"

search_button = wait.until(
    EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and contains(@class,'green')]"))
)

# Wait for input and type value
search_input = wait.until(
    EC.presence_of_element_located((By.NAME, "localId"))
)

search_input.clear()
search_input.send_keys(search_text)

# Scroll into view
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", search_button)

# Force click using JavaScript
driver.execute_script("arguments[0].click();", search_button)

print("✅ Search button clicked successfully")


input("Check UI. Press Enter to close browser...")
