"""
Selenium Test Script for User Registration
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


class SignupPage:
    """Page Object Model for Signup Page"""
    
    def __init__(self, driver):
        self.driver = driver
        
        # Locators
        self.username_input = (By.ID, "username")
        self.email_input = (By.ID, "email")
        self.password1_input = (By.ID, "password1")
        self.password2_input = (By.ID, "password2")
        self.signup_button = (By.CSS_SELECTOR, "button[type='submit']")
        
    def enter_username(self, username):
        """Enter username in the signup form"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.username_input)
        )
        element.clear()
        element.send_keys(username)
        
    def enter_email(self, email):
        """Enter email in the signup form"""
        element = self.driver.find_element(*self.email_input)
        element.clear()
        element.send_keys(email)
        
    def enter_password1(self, password):
        """Enter password in the first password field"""
        element = self.driver.find_element(*self.password1_input)
        element.clear()
        element.send_keys(password)
        
    def enter_password2(self, password):
        """Enter password in the confirm password field"""
        element = self.driver.find_element(*self.password2_input)
        element.clear()
        element.send_keys(password)
        
    def click_signup(self):
        """Click the signup button"""
        element = self.driver.find_element(*self.signup_button)
        element.click()
        
    def register_user(self, username, email, password):
        """Complete registration process"""
        self.enter_username(username)
        self.enter_email(email)
        self.enter_password1(password)
        self.enter_password2(password)
        self.click_signup()


def test_registration():
    """Main test function for user registration"""
    
    # Configuration
    BASE_URL = "http://127.0.0.1:8000"  
    STUDENT_ID = "011821146"  
    
    # Test data
    # test_username = f"testuser_{int(time.time())}"
    test_username= "test_meu_cu"
    test_email = f"testuser_{int(time.time())}@example.com"
    test_password = "SecurePass123!"
    
    print("=" * 60)
    print("SELENIUM REGISTRATION TEST SCRIPT")
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
        # Navigate to signup page
        print(f"\n[STEP 1] Navigating to signup page: {BASE_URL}")
        driver.get(BASE_URL)
        time.sleep(2)
        
        # Initialize Page Object
        signup_page = SignupPage(driver)
        
        # Perform registration
        print(f"[STEP 2] Entering registration details...")
        print(f"  - Username: {test_username}")
        print(f"  - Email: {test_email}")
        print(f"  - Password: {'*' * len(test_password)}")
        
        signup_page.register_user(test_username, test_email, test_password)
        
        # Wait for redirect to login page
        print(f"[STEP 3] Waiting for redirect to login page...")
        time.sleep(3)
        
        # Verify redirect
        current_url = driver.current_url
        print(f"[STEP 4] Current URL: {current_url}")
        
        if "login" in current_url:
            print("[SUCCESS] Registration successful! Redirected to login page.")
            registration_status = "PASSED"
        else:
            print("[WARNING] Registration may have failed. Not redirected to login page.")
            registration_status = "FAILED"
        
        # Capture screenshot
        screenshot_name = f"registration_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        driver.save_screenshot(screenshot_name)
        print(f"[INFO] Screenshot saved: {screenshot_name}")
        
        # Keep browser open for inspection
        time.sleep(3)
        
    except Exception as e:
        print(f"[ERROR] Test failed with exception: {str(e)}")
        registration_status = "ERROR"
        driver.save_screenshot(f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        
    finally:
        # Test summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Test Status: {registration_status}")
        print(f"WGU Student ID: {STUDENT_ID}")
        print(f"Current Date: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Test Username Created: {test_username}")
        print("=" * 60)
        print("[INFO] Script execution completed!")
        print("=" * 60)
        
        # Close browser
        time.sleep(5)
        input("\n[PAUSE] Pres Enter to close th browsr and complete the test")
        driver.quit()


if __name__ == "__main__":
    test_registration()
