import customtkinter, utilities, jitsi
from pathlib import Path
from playwright.sync_api import sync_playwright

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("PyStreamer Bot")
        self.geometry("800x480")
        
        # Initialize logging
        self.logs = utilities.logs(app_name="Main-UI")
        # Check if global.env exists, create if not and set defaults
        self.global_env = str(Path('Settings/global.env'))
        x = utilities.files.check_exist(self.global_env)
        # If file already exist
        if x['success'] and x['result']:
            self.logs.debug(f'File exists: {self.global_env}')
        # If file is not found, create it
        elif x['success'] and not x['result']:
            y = utilities.files.create(self.global_env)
            # Check if creation was successful
            match y['success']:
                # If file was created, add default settings
                case True: 
                    self.logs.debug(f"File created: {self.global_env}")

                    settings = {
                        'SETUP_REQUIRED': 'Yes',
                        'APPEARANCE': 'System',
                        'MEETING_SOFTWARE': 'jitsi'
                    }

                    for key, value in settings.items():
                        z = utilities.env.write(self.global_env, key, value)
                        if z['success']:
                            self.logs.debug(f"Set {key} = {value} in {self.global_env}")
                        else:
                            self.logs.error(f"Couldn't write {key} = {value} in {self.global_env}")
                            self.logs.error(f"{z['result']}")
                case False: 
                    self.logs.error(f"Error creating file: {y['result']}")
        # If there was an exception, log it
        else:
            self.logs.error(x['result'])

        # Set location for env files for meeting software (Currently only Jitsi, may expand to more)
        self.jitsi_env = str(Path('Settings/jitsi.env'))        
        
        # Load global appearance, set System if errors loading
        x = utilities.env.load(self.global_env, 'APPEARANCE')
        if x['success']:
            self.logs.debug(f"Loaded {self.global_env}")
            self.default_appearance = x['result']
        else:
            self.logs.critical(x['result'])

        # Frame for the options on left side of screen.
        self.sidebar_frame = customtkinter.CTkFrame(self, width=120, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Join Meeting", command=self.join_meeting)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=20)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Settings", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=20)

        self.sidebar_dropdown_1 = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System", "Dark", "Light"], command=self.set_appearance)
        self.sidebar_dropdown_1.set(str(self.default_appearance))
        self.sidebar_dropdown_1.grid(row=3, column=0, padx=20, pady=20)

        # Call init_options to make sure the appropriate files are in place, and fetch options for UI
        self.init_options()


    def sidebar_button_event(self):
        self.logs.debug("Sidebar button pressed, functionality TBD")
        
    def set_appearance(self, new_appearance: str):
        self.logs.debug("Appearance dropdown menu used")
        self.logs.debug(f"Setting appearance to: {new_appearance}")
        customtkinter.set_appearance_mode(new_appearance)
        x = utilities.env.write(self.global_env, 'APPEARANCE', new_appearance)
        if x['success']:
            self.logs.debug(f"Successfully updated to appearance: {new_appearance}")
        else:
            self.logs.error(f"Couldn't update appearance in {self.global_env}")
            self.logs.error(x['result'])
    
    def init_options(self):
        self.logs.debug(f"Setting appearance: {self.default_appearance}")
        customtkinter.set_appearance_mode(self.default_appearance)
        x = utilities.env.load(self.global_env, 'MEETING_SOFTWARE')
        y = utilities.files.check_exist(self.jitsi_env)
        
        # If MEETING_SOFTWARE is jitsi, and the env file does not exist, create it
        self.logs.debug(f"Software: {x['result']}.")
        self.logs.debug(f"Env file exists: {y['result']}")
        if x['result'] == 'jitsi' and y['result'] != True:
            jitsi_settings = {
            'JITSI_SETUP_REQUIRED': 'Yes',
            'JITSI_URL': 'NONE',
            'MEETING_ID': 'NONE',
            'DISPLAY_NAME': 'A Streamer Bot',
            'USER_NAME': 'NONE',
            'USER_PASSWORD': 'NONE'
            }
            # Loop through settings and try to set them in ENV file
            for key, value in jitsi_settings.items():
                z = utilities.env.write(self.jitsi_env, key, value)
                if z['success']:
                    self.logs.debug(f"Set {key} = {value} in {self.jitsi_env}")
                else:
                    self.logs.error(f"Couldn't write {key} = {value} in {self.jitsi_env}")
                    self.logs.error(f"{z['result']}")
  
    def join_meeting(self):
        self.logs.debug('Join Meeting clicked')
        # Check which meeting software should be launched, and if setup is required, before launching
        x = utilities.env.load(self.global_env, 'MEETING_SOFTWARE')
        match x['result']:
            case 'jitsi':
                self.logs.debug(f"Selected Jitsi Meeting.")
                y = utilities.env.load(self.jitsi_env, 'JITSI_SETUP_REQUIRED')
                # If Jitsi setup is not required, attempt to start.
                if y['result'] != 'Yes':
                    try:
                        self.logs.debug("Trying to launch Jitsi meeting...")
                        with sync_playwright() as playwright:
                            jitsi.run(playwright)
                    except Exception as e:
                        self.logs.error(f"Couldn't launch Jitsi: {e}")
                else:
                    self.logs.error("Jitsi requires setup in settings.")
            case default:
                self.logs.error(f"There was an error trying to determine meeting software. Are you trying to launch: {x['value']}?")
                self.logs.critical("You need to set up meeting software settings!")

App().mainloop()