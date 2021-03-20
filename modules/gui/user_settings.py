import yaml, os
from PyQt5.QtWidgets import *


class user_settings(QDial):
    def tab_movement(self, main_tab_index, section_tab, section_tab_index):
        self.tab_main.setCurrentIndex(main_tab_index)
        section_tab.setCurrentIndex(section_tab_index)

    def create_default_settings_dictionary(self):
        return {
            # "theme": "breeze dark",
            "default_section": 1
        }

    def apply_user_defined_changes(self, key, value):
        settings = self.read_yaml_file("settings.yaml")
        settings[key] = value
        f = open("settings.yaml", "w+")
        yaml.dump(settings, f, allow_unicode=True)

    def create_default_settings_yaml_file(self):
        default_settings = self.create_default_settings_dictionary()
        f = open("settings.yaml", "w+")
        yaml.dump(default_settings, f, allow_unicode=True)

    def check_settings_file(self):
        exists = os.path.isfile("settings.yaml")
        if not exists:
            self.create_default_settings_yaml_file()

    def load_settings(self):
        # check whether the user defined settings exists
        # 1. if exits - then load them
        # 2. else create default settings and load them
        self.check_settings_file()
        settings = self.read_yaml_file("settings.yaml")
        print(settings)

        # default load page
        self.toolBox.setCurrentIndex(settings["default_section"])
        # default theme
        # file_path  = os.path.join("themes", settings['theme'] + '.css')
        # with open(file_path,'r') as handler:
        #     style = handler.read()
        # self.setStyleSheet(style)
