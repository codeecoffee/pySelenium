"""
Selenium Test Script for Login Verification
WGU Student ID: 001234567
Using Page Object Model Pattern
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time


class LoginPage:
    """Page Object Model for Login Page"""
    
    def __init__(self, driver):
        self.driver = driver
        
        # Locators
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.student_id_header = (By.ID, "student-id")
        
    def enter_username(self, username):
        """Enter username in the login form"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.username_input)
        )
        element.clear()
        element.send_keys(username)
        
    def enter_password(self, password):
        """Enter password in the login form"""
        element = self.driver.find_element(*self.password_input)
        element.clear()
        element.send_keys(password)
        
    def click_login(self):
        """Click the login button"""
        element = self.driver.find_element(*self.login_button)
        element.click()
        
    def get_student_id(self):
        """Retrieve student ID from page header"""
        try:
            element = self.driver.find_element(*self.student_id_header)
            return element.text
        except:
            return "Student ID header not found"
            
    def login_user(self, username, password):
        """Complete login process"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()


class HomePage:
    """Page Object Model for Home Page"""
    
    def __init__(self, driver):
        self.driver = driver
        
        # Locators
        self.logout_button = (By.CSS_SELECTOR, "a.btn.btn-primary")
        self.home_heading = (By.TAG_NAME, "h1")
        
    def is_home_page_displayed(self):
        """Check if home page is displayed"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.home_heading)
            )
            heading = self.driver.find_element(*self.home_heading)
            return "Home Page" in heading.text
        except:
            return False


def test_login_verification():
    """Main test function for login verification"""
    
    # Configuration
    BASE_URL = "http://127.0.0.1:8000"  # Update with your Django server URL
    LOGIN_URL = f"{BASE_URL}/login/"
    STUDENT_ID = "001234567"  # Replace with your actual WGU Student ID
    
    # Test credentials - use the same credentials from registration test
    # Or create a user first using Django admin/shell
    test_username = "testuser123"  # Update with actual username
    test_password = "SecurePass123!"  # Update with actual password
    
    print("=" * 60)
    print("SELENIUM LOGIN VERIFICATION TEST SCRIPT")
    print("=" * 60)
    print(f"WGU Student ID: {STUDENT_ID}")
    print(f"Test Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Browser: Chrome")
    print("=" * 60)
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to login page
        print(f"\n[STEP 1] Navigating to login page: {LOGIN_URL}")
        driver.get(LOGIN_URL)
        time.sleep(2)
        
        # Initialize Page Objects
        login_page = LoginPage(driver)
        
        # Capture Student ID from login page
        student_id_text = login_page.get_student_id()
        print(f"[STEP 2] Student ID displayed on page: {student_id_text}")
        
        # Perform login
        print(f"[STEP 3] Attempting login with credentials...")
        print(f"  - Username: {test_username}")
        print(f"  - Password: {'*' * len(test_password)}")
        
        login_page.login_user(test_username, test_password)
        
        # Wait for page load
        print(f"[STEP 4] Waiting for page transition...")
        time.sleep(3)
        
        # Verify login success
        current_url = driver.current_url
        print(f"[STEP 5] Current URL after login: {current_url}")
        
        # Check if redirected to home page
        home_page = HomePage(driver)
        
        if home_page.is_home_page_displayed():
            print("[SUCCESS] Login successful! Home page is displayed.")
            print(f"[INFO] Successfully authenticated user: {test_username}")
            login_status = "PASSED"
        else:
            # Check if still on login page (failed login)
            if "login" in current_url:
                print("[FAILED] Login failed! Still on login page.")
                print("[INFO] Check if credentials are correct or user exists.")
                login_status = "FAILED"
            else:
                print(f"[WARNING] Unexpected redirect to: {current_url}")
                login_status = "WARNING"
        
        # Capture screenshot
        screenshot_name = f"login_verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_name)
        print(f"[INFO] Screenshot saved: {screenshot_name}")
        
        # Additional verification - check page title
        page_title = driver.title
        print(f"[INFO] Page Title: {page_title}")
        
        # Keep browser open for inspection
        time.sleep(3)
        
    except Exception as e:
        print(f"[ERROR] Test failed with exception: {str(e)}")
        login_status = "ERROR"
        driver.save_screenshot(f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        import traceback
        print(traceback.format_exc())
        
    finally:
        # Test summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Test Status: {login_status}")
        print(f"WGU Student ID: {STUDENT_ID}")
        print(f"Current Date: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"Current Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Username Tested: {test_username}")
        print("=" * 60)
        print("[INFO] Script execution completed!")
        print("=" * 60)
        
        # Close browser
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    test_login_verification()
