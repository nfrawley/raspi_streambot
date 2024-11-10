import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    # Pull env variables
    dotenv_path = Path('Settings/jitsy.env')
    load_dotenv(dotenv_path=dotenv_path)
    display_name = os.getenv('DISPLAY_NAME')
    user_name = os.getenv('USER_NAME')
    user_password = os.getenv('USER_PASSWORD')
    meeting_base = os.getenv('JITSI_URL')
    meeting_id = os.getenv('MEETING_ID')

    if meeting_base and meeting_id:
        meeting_url = f"{meeting_base}/{meeting_id}"
        print(meeting_url)
    else:
        print("Error loading env variables for meeting.")


    # Initialize the browser. The --use-fake-ui-for-media-stream prevents the popup for permissions to access camera and video.
    # You can disable headless mode for debugging (Or if you want the meeting window to be visible)
    browser = playwright.chromium.launch(headless=False, args=["--use-fake-ui-for-media-stream"])
    context = browser.new_context()
    page = context.new_page()

    # Navigate to meeting URL
    page.goto(meeting_url)
    print(f"Opened meeting URL: {meeting_url}")

    # Find and fill in Displayname, click join
    page.get_by_role("textbox", name="Enter your name").fill(display_name)
    page.get_by_role("button", name="Join Meeting").click()

    # Handle user auth prompt, if required. Timeout is in miliseconds. If not visible, no auth required
    message = page.wait_for_selector("text=Authentication required", timeout=10000)
    if message.is_visible():
        print("Login is required")
        page.get_by_placeholder("User identifier").fill(user_name)
        page.get_by_placeholder("Password").fill(user_password)
        page.get_by_role("button", name="Login").click()
    else:
        print("No auth required.")
    
    # Keep it open until we're done with it :)
    print("Press enter key to quit...")
    input()
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)