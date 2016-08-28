from . import APP_DIR
import configparser
import os


class PasswordManager:
    config = None

    def __init__(self, api_name):
        self.config = configparser.RawConfigParser()
        file_path = os.path.join(APP_DIR, "api", api_name, 'settings.ini')
        self.config.read_file(open(file_path, 'r'))

    def get_username(self):
        return self.config.get('Login', 'username')

    def get_password(self):
        return self.config.get('Login', 'password')
