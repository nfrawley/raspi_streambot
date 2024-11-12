import utilities
from pathlib import Path
from playwright.sync_api import Playwright


def run(playwright: Playwright) -> None:
    # Init logging
    logs = utilities.logs(app_name='Jitsi')
    
    # Pull env values, validate if successful
    file = str(Path('Settings/jitsi.env'))
    settings = {
        'DISPLAY_NAME': '',
        'USER_NAME': '',
        'USER_PASSWORD': '',
        'JITSI_URL': '',
        'MEETING_ID': ''
    }
    # Fetch value for each key from settings, then add to dictionary
    for item in settings:
        logs.debug(f"Searching for: {item}")
        y = utilities.env.load(file, item)
        if y['success']:
            logs.debug(f"Found {item} from .ENV")
            logs.debug(f"Setting {item}")
            settings[item] = y['result']
        else:
            logs.error(f"Couldn't find value of {item}!")
    
    # Fetch values for keys from dictionary for use
    display_name = settings['DISPLAY_NAME']
    user_name = settings['USER_NAME']
    user_password = settings['USER_PASSWORD']
    meeting_base = settings['JITSI_URL']
    meeting_id = settings['MEETING_ID']
    meeting_url = f"{meeting_base}/{meeting_id}"

    # Initialize the browser. The --use-fake-ui-for-media-stream prevents the popup for permissions to access camera and video.
    # You can disable headless mode for debugging (Or if you want the meeting window to be visible)
    browser = playwright.chromium.launch(headless=True, args=["--use-fake-ui-for-media-stream"])
    context = browser.new_context()
    page = context.new_page()

    # Navigate to meeting URL
    page.goto(meeting_url)
    logs.info(f"Opened meeting URL: {meeting_url}")

    # Find and fill in Displayname, click join
    try:
        logs.debug("Searching for display name field.")
        page.get_by_role("textbox", name="Enter your name").fill(display_name)
        logs.debug(f"Typed: {display_name}.")
    except Exception as e:
        logs.debug(f"Couldn't complete step display name: {e}")
    
    try:
        logs.debug("Searching for Join Meeting button")
        page.get_by_role("button", name="Join Meeting").click()
        logs.debug("Clicked join meeting button.")
        logs.info("Joining meeting!")
    except Exception as e:
        logs.error(f"Couldn't complete step join meeting: {e}")
    
    # Handle user auth prompt, if required. Timeout is in miliseconds. If not visible, no auth required.
    try:
        message = page.wait_for_selector("text=Authentication required", timeout=10000)
        if message and message.is_visible():
            logs.debug("Login is required.")
            try:
                logs.debug("Searching for user name field.")
                page.get_by_placeholder("User identifier").fill(user_name)
                logs.debug(f"Typed: {user_name}")
                logs.debug("Searching for user password field.")
                page.get_by_placeholder("Password").fill(user_password)
                logs.debug("Typed provided password.")
                logs.debug("Searching for login button.")
                page.get_by_role("button", name="Login").click()
                logs.debug("Clicked login button.")
            except Exception as e:
                logs.error(f"Couldn't complete step user authorization: {e}")
        else:
            logs.debug("No auth required.")
    except Exception as e:
        print(f'Error occurred during auth step: {e}')
    
    # Keep it open until we're done with it :)
    input()
    context.close()
    browser.close()