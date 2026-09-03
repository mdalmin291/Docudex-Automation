from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

# Open login page
driver.get("http://27.147.184.165:8082/login")

# Wait and enter username
wait.until(EC.presence_of_element_located((By.NAME, "_username"))).send_keys("alamin")

# Enter password
wait.until(EC.presence_of_element_located((By.NAME, "_password"))).send_keys("Mtb@12345678910")

# Click login button (important)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# Wait until homepage/dashboard loads
wait.until(EC.url_changes("http://27.147.184.165:8082/login"))
print("✅ Successfully logged in")

input("Press Enter to close browser...")

# # Keep browser open
# input("Press Enter to close browser...")
