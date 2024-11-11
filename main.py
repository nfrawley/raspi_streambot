import customtkinter, utilities, jitsi
from pathlib import Path
from playwright.sync_api import sync_playwright

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("PyStreamer Bot")
        self.geometry("800x480")

        # Check if global.env exists, create if not and set defaults
        self.global_env = str(Path('Settings/global.env'))
        if not utilities.files.check_exist(self.global_env):
            utilities.env.write(self.global_env, 'SETUP_REQUIRED', 'Yes')
            utilities.env.write(self.global_env, 'APPEARANCE', 'System')
            utilities.env.write(self.global_env, 'MEETING_SOFTWARE', 'jitsi')
        # Set location for env files for meeting software (Currently only Jitsi, may expand to more)
        self.jitsi_env = str(Path('Settings/jitsi.env'))        
        
        # Load global appearance, set System if errors loading
        self.default_appearance = utilities.env.load(self.global_env, 'APPEARANCE') or 'System'

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

        
        self.init_options()


    def sidebar_button_event(self):
        print("Sidebar button pressed, functionality TBD")
        
    def set_appearance(self, new_appearance: str):
        customtkinter.set_appearance_mode(new_appearance)
        utilities.env.write(self.global_env, 'APPEARANCE', new_appearance)
        print(f'Changing appearance to {new_appearance}')
    
    def init_options(self):
        customtkinter.set_appearance_mode(self.default_appearance)
        if utilities.env.load(self.global_env, 'MEETING_SOFTWARE') == 'JITSI' and not utilities.files.check_exist(self.jitsi_env):
            utilities.env.write(self.jitsi_env, 'JITSI_SETUP_REQUIRED', 'Yes')
            utilities.env.write(self.jitsi_env, 'JITSI_URL', 'NONE')
            utilities.env.write(self.jitsi_env, 'MEETING_ID', 'NONE')
            utilities.env.write(self.jitsi_env, 'MEETING_URL', 'NONE')
            utilities.env.write(self.jitsi_env, 'DISPLAY_NAME', 'A Streamer Bot')
            utilities.env.write(self.jitsi_env, 'USER_NAME', 'NONE')
            utilities.env.write(self.jitsi_env, 'USER_PASSWORD', 'NONE')


    def join_meeting(self):
        print('Join Meeting clicked')
        try:
            print(f'Trying: {utilities.env.load(self.global_env, 'MEETING_SOFTWARE')} and {utilities.env.load(self.jitsi_env, 'JITSI_SETUP_REQUIRED')}')
            if utilities.env.load(self.global_env, 'MEETING_SOFTWARE') == 'JITSI' and utilities.env.load(self.jitsi_env, 'JITSI_SETUP_REQUIRED') != 'Yes':
                print('Starting Jitsi')
                with sync_playwright() as playwright:
                    jitsi.run(playwright)
        except Exception as e:
            print(f'There was an error joining meeting: {e}')

App().mainloop()