import configparser
import os

class ConfigManager:
    def __init__(self, config_file='setup.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()
        
    def load_config(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            
    def get_value(self, key, section='DEFAULT'):
        return self.config.get(section, key, fallback='')
        
    def set_value(self, key, value, section='DEFAULT'):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self.save_config()
        
    def save_config(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile) 