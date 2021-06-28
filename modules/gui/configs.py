from PyQt5.QtWidgets import *
import glob, os, re, sys
from modules.gui_windows.backup_config import *
from netmiko import ConnectHandler
from datetime import datetime
from yaml import safe_load
import yaml


class backup_window(
    QWidget,
    Config,
):
    def __init__(self, device, config_type):
        self.device = device
        self.config_type = config_type
        QWidget.__init__(self)
        self.setupUi(self)
        self.show()
        self.handle_config_submit()

    def handle_config_submit(self):
        self.configs_backup_btn_cancel.clicked.connect(lambda: self.close())
        self.configs_backup_btn_save.clicked.connect(self.backup_config)

    def get_config_command(self):
        config_type = "cisco_ios"
        if "start" in self.config_type:
            config_type = "startup"
        else:
            config_type = "running"

        config_path = os.path.join("hosts", "configs", "commands")
        config_path = os.path.join(
            config_path, self.device["data"]["device_type"] + "_" + config_type + ".cfg"
        )
        with open(config_path, "r") as handler:
            command = handler.read()
        if command:
            return command
        else:
            return False

    def check_description_file(self):
        if not os.path.isdir(os.path.join("hosts", "configs")):
            os.mkdir(os.path.join("hosts", "configs"))
            os.path.join("hosts", "configs", self.device["hostname"])
            return False
        if not os.path.isdir(os.path.join("hosts", "configs", self.device["hostname"])):
            os.mkdir(os.path.join("hosts", "configs", self.device["hostname"]))
            return False

        file_path = os.path.join(
            "hosts", "configs", self.device["hostname"], "description.yaml"
        )
        if not os.path.isfile(file_path):
            return False
        else:
            return True

    def read_yaml_file(self, yaml_file):
        descriptions = None
        with open(yaml_file, "r") as handler:
            descriptions = safe_load(handler)
        return descriptions

    def create_config_dict(self, file_name, description):
        return {"desc": description, "file_name": file_name, "type": self.config_type}

    def write_description(self, file_path, description):
        regex = re.compile(
            r"hosts(?P<slsh>\/|\\)configs(?P=slsh)(?P<hostname>\w+)(?P=slsh)(?P<file_name>.+\.cfg)"
        )
        matching = regex.search(file_path)
        hostname = matching.group("hostname")
        file_name = matching.group("file_name")

        desc_file_path = os.path.join("hosts", "configs", hostname, "description.yaml")

        desc = self.create_config_dict(file_name, description)

        all_descriptions = list()
        if self.check_description_file():
            all_descriptions = self.read_yaml_file(desc_file_path)
            all_descriptions.append(desc)
            f = open(desc_file_path, "w+")
            yaml.dump(all_descriptions, f, allow_unicode=True)

        else:
            all_descriptions.append(desc)
            f = open(desc_file_path, "w+")
            yaml.dump(all_descriptions, f, allow_unicode=True)

    def backup_config(self):
        try:
            conn = ConnectHandler(**self.device["data"])
            conn.enable()
            command = self.get_config_command()
            if command:
                output = conn.send_command(command)
                now = datetime.now()
                config_name = now.strftime("%d-%m-%Y_%H-%M-%S")
                output_filename = os.path.join(
                    "hosts",
                    "configs",
                    self.device["hostname"],
                    self.config_type + "_" + config_name + ".cfg",
                )
                with open(output_filename, "w") as handler:
                    handler.write(output)
                QMessageBox.information(self, "Succesful", "Backup successful")
                description = self.lineEdit.text()
                self.write_description(output_filename, description)
                self.close()
                return

            else:
                print("command is invalid")
                self.close()
                return
        except Exception as error:
            QMessageBox.critical(self, "Warning", str(error))
            self.close()
            return


class configs(QDialog):
    def show_configs_backup_window(self):
        device_name = self.mgmt_config_all_devices.currentText()
        if device_name == "dummy":
            QMessageBox.critical(self,"Note","Please add a group")
            return
        all_devices = self.convert_host_file_into_list()
        our_device = None
        for device in all_devices:
            if device["hostname"] == device_name:
                our_device = device
                break
        our_device["data"]["password"] = self.decrypt_password(
            our_device["data"]["password"]
        )
        our_device["data"]["secret"] = self.decrypt_password(
            our_device["data"]["secret"]
        )
        backup_config_window = backup_window(
            our_device,
            self.mgmt_config_config_type.currentText(),
        )
        self.fill_configs()
        return

    # def check_config_restore_button(self):
    #     if self.configs_list.selectedItems():
            # self.mgmt_config_btn_restore.setEnabled(True)
        # else:
            # self.mgmt_config_btn_restore.setEnabled(False)

    def get_config_file_path(self, device_name):
        return os.path.join("hosts", "configs", device_name, "description.yaml")

    def check_config_files_existance(
        self, all_configs_in_file, config_type, device_name
    ):

        device_dir = os.path.join("hosts", "configs", device_name)
        all_existing_files = glob.glob(os.path.join(device_dir, "*.cfg"))
        # all_existing_files = glob.glob(os.path.join(device_dir, f"*{config_type}*.cfg"))
        print(f"All existing files {all_existing_files}")
        print(f"all configs in file {all_configs_in_file}")
        files_not_present = list()
        i = 0
        for config in all_configs_in_file:
            present = False
            for file in all_existing_files:
                if config["file_name"] in file:
                    present = True
                    break
            if not present:
                files_not_present.append(i)
            i += 1

        print(f"Files not present at indexes {files_not_present}")
        return files_not_present

    def check_desc_file(self, hostname):
        if not os.path.isdir(os.path.join("hosts", "configs")):
            os.mkdir(os.path.join("hosts", "configs"))
            os.path.join("hosts", "configs", hostname)
            print("configs directory does not exists")
            return False
        if not os.path.isdir(os.path.join("hosts", "configs", hostname)):
            print(f"Host's({hostname}) configs directory does not exist")
            os.mkdir(os.path.join("hosts", "configs", hostname))
            return False

        file_path = os.path.join("hosts", "configs", hostname, "description.yaml")
        if not os.path.isfile(file_path):
            return False
        else:
            return True

    def fill_configs(self):
        device_name = self.mgmt_config_all_devices.currentText()
        # self.mgmt_config_btn_restore.setEnabled(False)
        if not device_name == "Select a Device":
            self.mgmt_config_btn_backup.setEnabled(True)
            device_dir = os.path.join("hosts", "configs", device_name)
            config_type = self.mgmt_config_config_type.currentText()
            # check for Per device config file
            if self.check_desc_file(device_name):
                all_configs = self.read_yaml_file(
                    self.get_config_file_path(device_name)
                )
                print(f"All configs are {all_configs}")
                our_configs = list()
                if config_type == "startup config":
                    for config in all_configs:
                        if config["type"] == "startup config":
                            our_configs.append(config)
                else:
                    for config in all_configs:
                        if config["type"] == "running config":
                            our_configs.append(config)
                print(f"Our config is {our_configs}")
                # check for empty entries
                files_not_present_indices = self.check_config_files_existance(
                    all_configs, config_type, device_name
                )
                if files_not_present_indices:
                    for index in files_not_present_indices:
                        all_configs.pop(index)
                    try:
                        desc_file_path = os.path.join(
                            "hosts", "configs", device_name, "description.yaml"
                        )
                        f = open(desc_file_path, "w+")
                        yaml.dump(all_configs, f, allow_unicode=True)
                        return
                    except Exception as error:
                        QMessageBox.critical(self, "Warning", str(error))

                self.configs_list.clear()
                if our_configs:
                    for config in our_configs:
                        output = "{:50s} {:10s}".format(
                            config["file_name"], config["desc"]
                        )
                        self.configs_list.addItem(output)
                else:
                    print("No backup configs are found")
                    # QMessageBox.information(
                    #     self, "Warning", "No backup configs are found"
                    # )
                    # self.mgmt_config_btn_restore.setEnabled(False)
            else:
                # self.mgmt_config_btn_restore.setEnabled(False)
                self.configs_list.clear()

        else:
            self.mgmt_config_btn_backup.setEnabled(False)
            # self.mgmt_config_btn_restore.setEnabled(False)
            self.configs_list.clear()
