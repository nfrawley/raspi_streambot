import utilities
from pathlib import Path
from playwright.sync_api import Playwright


def run(playwright: Playwright) -> None:
    # Pull env variables
    file = str(Path('Settings/jitsi.env'))
    display_name = utilities.env.load(file, 'DISPLAY_NAME') or 'None'
    user_name = utilities.env.load(file, 'USER_NAME') or 'None'
    user_password = utilities.env.load(file, 'USER_PASSWORD') or 'None'
    meeting_base = utilities.env.load(file, 'JITSI_URL') or 'None'
    meeting_id = utilities.env.load(file, 'MEETING_ID') or 'None'
    meeting_url = f"{meeting_base}/{meeting_id}"

    # Initialize the browser. The --use-fake-ui-for-media-stream prevents the popup for permissions to access camera and video.
    # You can disable headless mode for debugging (Or if you want the meeting window to be visible)
    browser = playwright.chromium.launch(headless=True, args=["--use-fake-ui-for-media-stream"])
    context = browser.new_context()
    page = context.new_page()

    # Navigate to meeting URL
    page.goto(meeting_url)
    print(f"Opened meeting URL: {meeting_url}")

    # Find and fill in Displayname, click join
    page.get_by_role("textbox", name="Enter your name").fill(display_name)
    page.get_by_role("button", name="Join Meeting").click()

    # Handle user auth prompt, if required. Timeout is in miliseconds. If not visible, no auth required.
    try:
        message = page.wait_for_selector("text=Authentication required", timeout=10000)
        if message and message.is_visible():
            print("Login is required")
            page.get_by_placeholder("User identifier").fill(user_name)
            page.get_by_placeholder("Password").fill(user_password)
            page.get_by_role("button", name="Login").click()
        else:
            print("No auth required.")
    except Exception as e:
        print(f'Error occurred during auth step: {e}')
    
    # Keep it open until we're done with it :)
    print("Press enter key to quit...")
    input()
    context.close()
    browser.close()