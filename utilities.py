import os, dotenv
from typing import Optional

class env:
    @staticmethod
    def load(file: str, setting: str) -> Optional[str]:
        """
        Load the value of a setting from a dotenv file.

        Args:
            file (str): The path to the dotenv file.
            setting (str): The key of the setting to load.

        Returns:
            str: The value of the setting, or None if an error occurs.
        """
        try:
            dotenv.load_dotenv(file)
            value = os.getenv(setting)
            return value
        except Exception as e:
            print(f"Error loading {setting} from {file}: {e}")
            return None
    
    @staticmethod
    def write(file: str, setting: str, value: str) -> Optional[str]:
        """
        Write a value to a setting in a dotenv file and update the environment variable.

        Args:
            file (str): The path to the dotenv file.
            setting (str): The key of the setting to write.
            value (str): The value to write to the setting.

        Returns:
            str: The value written, or None if an error occurs.
        """
        try:
            dotenv.set_key(file, setting, value)
            os.environ[setting] = value
            return value
        except Exception as e:
            print(f"Error writing {value} to {setting} in {file}: {e}")
            return None

class files:
    @staticmethod
    def check_exist(file: str) -> bool:
        """
        Check if a file exists.

        Args:
            file (str): The path to the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        try:
            with open(file):
                return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"Error checking if file exists {file}: {e}")
            return False
    
    @staticmethod
    def create(file: str) -> bool:
        """
        Create a file and its directories if they do not exist.

        Args:
            file (str): The path to the file to create.

        Returns:
            bool: True if the file was created, False otherwise.
        """
        try:
            os.makedirs(os.path.dirname(file), exist_ok=True)
            with open(file, 'w') as f:
                pass
            return True
        except OSError as e:
            print(f"OS error creating file {file}: {e}")
            return False
        except Exception as e:
            print(f"Error creating file {file}: {e}")
            return False
    
    @staticmethod
    def remove(file: str) -> bool:
        """
        Remove a file.

        Args:
            file (str): The path to the file to remove.

        Returns:
            bool: True if the file was removed, False otherwise.
        """
        try:
            os.remove(file)
            return True
        except FileNotFoundError:
            print(f"File not found: {file}")
            return False
        except OSError as e:
            print(f"OS error removing file {file}: {e}")
            return False
        except Exception as e:
            print(f"Error removing file {file}: {e}")
            return False
