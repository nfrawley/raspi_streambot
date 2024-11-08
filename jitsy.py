from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def join_jitsi_meeting():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--headless")

    # Initialize the browser
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    browser.set_window_size(1280, 800)
    browser.get("https://meet.noahfrawley.ca/test-games-night")
    print("Opened meeting URL")

    # Wait for the display name input field to be available and enter the display name
    try:
        display_name_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "premeeting-name-input"))
        )
        display_name_input.send_keys("Test User")
        print("Entered display name")
    except Exception as e:
        print(f"Error entering display name: {e}")

    # Wait for and click the "Join Meeting" button
    try:
        join_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Join meeting"]'))
        )
        join_button.click()
        print("Clicked Join Meeting button")
    except Exception as e:
        print(f"Error clicking Join Meeting button: {e}")

    # Wait for the login page and enter the username and password
    try:
        username_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "login-dialog-username"))
        )
        username_input.send_keys("noah")
        print("Entered username")

        password_input = browser.find_element(By.NAME, "password")
        password_input.send_keys("REDACTED")
        print("Entered password")

        login_button = browser.find_element(By.CSS_SELECTOR, '[aria-label="Login"]')
        login_button.click()
        print("Clicked Login button")
    except Exception as e:
        print(f"Error logging in: {e}")

    # Wait for the meeting to load and check if video is playing
    try:
        video_element = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        if video_element.is_displayed():
            print("Video is playing")
    except Exception as e:
        print(f"Error checking video: {e}")

    # Keep the browser open until manually closed
    print("Keeping the browser open. Press Ctrl+C to close.")
    try:
        while True:
            time.sleep(30)
            # Take a screenshot every 30 sec in case it needs to be verified
            browser.save_screenshot("screenshot.png")
            print("Screenshot saved")
    except KeyboardInterrupt:
        print("Quit command received. Closing browser.")
        browser.quit()

if __name__ == "__main__":
    join_jitsi_meeting()
