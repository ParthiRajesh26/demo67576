import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = 'https://opensource-demo.orangehrmlive.com/web/index.php/auth/login'
USERNAME = 'Admin'
PASSWORD = 'admin123'
USERNAME_XPATH = "//input[@name='username']"
PASSWORD_XPATH = "//input[@name='password']"
LOGIN_BUTTON_XPATH = "//button[@type='submit']"
DASHBOARD_URL_FRAGMENT = '/dashboard'

@pytest.mark.login
def test_automate_login_functionality_for_orangehrm():
    """
    Test Case: Automate login functionality for OrangeHRM (KAN-15)
    Scenario:
        - Verify that a valid user can successfully log in to the application.
        - User should be redirected to the dashboard page.
    Steps:
        1. Navigate to the login page
        2. Enter valid username
        3. Enter valid password
        4. Click on Login button
        5. Validate dashboard redirection and page load
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    try:
        driver.get(LOGIN_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, USERNAME_XPATH)))
        driver.find_element(By.XPATH, USERNAME_XPATH).send_keys(USERNAME)
        driver.find_element(By.XPATH, PASSWORD_XPATH).send_keys(PASSWORD)
        driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH).click()
        WebDriverWait(driver, 15).until(lambda d: DASHBOARD_URL_FRAGMENT in d.current_url)
        assert DASHBOARD_URL_FRAGMENT in driver.current_url, (
            f"Login failed: Expected to be redirected to dashboard, but current URL is {driver.current_url}")
        # Additional validation: ensure dashboard page loads key element
        dashboard_header_xpath = "//h6[text()='Dashboard']"
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, dashboard_header_xpath)))
    except Exception as e:
        pytest.fail(f"Test failed due to exception: {e}")
    finally:
        driver.quit()
