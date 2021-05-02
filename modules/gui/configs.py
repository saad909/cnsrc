from PyQt5.QtWidgets import *
import glob, os, re, sys
from modules.gui_windows.backup_config import *


class backup_window(QWidget, Config):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.show()
        self.handle_config_submit()

    def handle_config_submit(self):
        self.configs_backup_btn_cancel.clicked.connect(lambda: self.close())
        self.configs_backup_btn_save.clicked.connect(self.backup_config)

    def backup_config(self):
        # device_name = ui.mgmt_config_all_devices.currentText()
        # config_type = ui.mgmt_config_config_type.currentText()
        QMessageBox.information(self, "Note", f"Saving config")
        # QMessageBox.information(self, "Note", f"Saving {config_type} of {device_name}")
        self.close()


class configs(QDialog):
    def show_configs_backup_window(self):
        backup_config_window = backup_window()
        backup_config_window.show()

    def check_config_restore_button(self):
        if self.configs_list.selectedItems():
            self.mgmt_config_btn_restore.setEnabled(True)
        else:
            self.mgmt_config_btn_restore.setEnabled(False)

    def fill_configs(self):
        text = self.mgmt_config_all_devices.currentText()
        self.mgmt_config_btn_restore.setEnabled(False)
        if not text == "Select a Device":
            self.mgmt_config_btn_backup.setEnabled(True)
            device_name = text
            device_dir = os.path.join("hosts", "configs", device_name)
            print(device_dir)
            config_type = self.mgmt_config_config_type.currentText()
            if config_type == "startup config":
                all_configs = glob.glob(os.path.join(device_dir, "*start*.cfg"))
            else:
                all_configs = glob.glob(os.path.join(device_dir, "*run*.cfg"))
            self.configs_list.clear()
            if all_configs:
                # remove the path before and add only the filename
                i = 0
                for config in all_configs:
                    config = re.sub(r"\w+\/", "", config)
                    all_configs[i] = config
                    print(all_configs[i])
                    i += 1
                self.configs_list.addItems(all_configs)
            else:
                QMessageBox.information(self, "Warning", "No backup configs are found")
                self.mgmt_config_btn_restore.setEnabled(False)
        else:
            self.mgmt_config_btn_backup.setEnabled(False)
            self.mgmt_config_btn_restore.setEnabled(False)
            self.configs_list.clear()
