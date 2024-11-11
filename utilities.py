import logging
import os, dotenv
from pathlib import Path

class env:
    @staticmethod
    def load(file: str, setting: str) -> dict:
        """
        Load the value of a setting from a dotenv file.

        Args:
            file (str): The path to the dotenv file.
            setting (str): The key of the setting to load.

        Returns:
            dict: Dictionary with keys 'success' and 'result', where 'success' is False if an exception occurs. 'result' contains the value of requested key, or a string of the exception that occurred.
        """
        try:
            dotenv.load_dotenv(file)
            value = os.getenv(setting)
            return {'success': True, 'result': value}
        except Exception as e:
            return {'success': False, 'result': str(e)}
    
    @staticmethod
    def write(file: str, setting: str, value: str) -> dict:
        """
        Write a value to a setting in a dotenv file and update the environment variable.

        Args:
            file (str): The path to the dotenv file.
            setting (str): The key of the setting to write.
            value (str): The value to write to the setting.

        Returns:
            dict: Dictionary with keys 'success' and 'result', where 'success' is False if an exception occurs. 'result' contains the value of set key, or a string of the exception that occurred.
        """
        try:
            dotenv.set_key(file, setting, value)
            os.environ[setting] = value
            return {'success': True, 'result': value}
        except Exception as e:
            return {'success': False, 'result': str(e)}

class files:
    @staticmethod
    def check_exist(file: str) -> dict:
        """
        Check if a file exists.

        Args:
            file (str): The path to the file to check.

        Returns:
            dict: Dictionary with keys 'success' and 'result', where 'success' is False if an exception occurs. 'result' contains True if file exists, False if the file does not exist, or a string of the exception that occurred.
        """
        try:
            with open(file):
                return {'success': True, 'result': True}
        except FileNotFoundError:
            return {'success': True, 'result': False}
        except Exception as e:
            return {'success': False, 'result': str(e)}
    
    @staticmethod
    def create(file: str) -> dict:
        """
        Create a file and its directories if they do not exist.

        Args:
            file (str): The path to the file to create.

        Returns:
            dict: Dictionary with keys 'success' and 'result', where 'success' is False if an exception occurs. 'result' contains True if file was created, or a string of the exception that occurred.
        """
        try:
            os.makedirs(os.path.dirname(file), exist_ok=True)
            with open(file, 'w') as f:
                pass
            return {'success': True, 'result': True}
        except Exception as e:
            return {'success': False, 'result': str(e)}
    
    @staticmethod
    def remove(file: str) -> dict:
        """
        Remove a file.

        Args:
            file (str): The path to the file to remove.

        Returns:
            dict: Dictionary with keys 'success' and 'result', where 'success' is False if an exception occurs. 'result' contains True if file was removed, False if the file was not found, or a string of the exception that occurred.
        """
        try:
            os.remove(file)
            return {'success': True, 'result': True}
        except FileNotFoundError:
            return {'success': True, 'result': False}
        except Exception as e:
            return {'success': False, 'result': str(e)}

class logs:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If the logging env file does not exist, create it. Default to level INFO.
        log_settings = str(Path('Settings/logging.env'))
        if not files.check_exist(log_settings):
            files.create(log_settings)
            env.write(log_settings, 'LOGGING_LEVEL', 'INFO')
        
        # Load logging settings
        load_level = env.load(log_settings, 'LOGGING_LEVEL')
        level = load_level['result']
        self.app_logger = logging.getLogger(__name__)
        
        # Convert string to actual logging level
        self.level = level.upper() if level else 'INFO'
        self.app_logger.setLevel(getattr(logging, self.level))
        print(f"Logging level set to: {level}")

    # Set the logging level if it needs to be updated
    def set_level(self, level: str):
        self.new_level = level.upper()
        self.app_logger.setLevel(getattr(logging, self.new_level))
        print(f"Logging level updated to {self.new_level}")

    # Print to log file INFO message
    def info(self, message: str) -> None:
        self.app_logger.info(f"{__name__} - INFO: {message}")
    
    # Print to log file DEBUG message
    def debug(self, message: str) -> None:
        self.app_logger.debug(f"{__name__} - DEBUG: {message}")

    # Print to log file CRTICAL message
    def critical(self, message: str) -> None:
        self.app_logger.critical(f"{__name__} - CRITICAL: {message}")

    # Print to log file ERROR message
    def error(self, message: str) -> None:
        self.app_logger.error(f"{__name__} - ERROR: {message}")