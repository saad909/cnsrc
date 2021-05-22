from PyQt5.QtWidgets import *
import os
import re
import csv
from pprint import pprint


class devices(QDialog):
    def create_device_directory(self, hostname):
        # check for directory, if does not exists then make it
        try:
            if not os.path.isdir(os.path.join("hosts", "configs")):
                os.mkdir(os.path.join("hosts", "configs"))
            config_path = os.path.join("hosts", "configs", hostname)
            os.mkdir(config_path)
        except Exception as error:
            print(str(error))

    def add_host(self):
        ##### getting the values from the boxes ######

        hostname = self.d_add_hostname.text()
        ip_address = self.d_add_ip_address.text()
        username = self.d_add_username.text()
        password = self.d_add_password.text()
        secret = self.d_add_secret.text()
        port_number = self.d_add_port_number.text()
        if not port_number:
            port_number = 22
        device_type = str(self.d_add_device_type.currentText())
        os_type = str(self.d_add_cb_os_type.currentText())

        ##### checking for empty boxes ######

        if not hostname:
            self.highlight_border(self.d_add_hostname)
            self.statusBar().showMessage("Hostname can not be empty")
            self.d_add_hostname.setFocus()
            return
        else:
            self.highlight_border_false(self.d_add_hostname)
        if self.d_add_ip_address and self.is_ip_complete(self.d_add_ip_address):
            self.highlight_border_false(self.d_add_ip_address)
        else:
            self.highlight_border(self.d_add_ip_address)
            self.statusBar().showMessage("Invalid Ip Address")
            self.d_add_ip_address.setFocus()

            return

        if not username:
            self.highlight_border(self.d_add_username)
            self.statusBar().showMessage("username can not be empty")
            self.d_add_username.setFocus()
            return
        else:
            self.highlight_border_false(self.d_add_username)
        if not password:
            self.highlight_border(self.d_add_password)
            self.statusBar().showMessage("password can not be empty")
            self.d_add_password.setFocus()
            return
        else:
            self.highlight_border_false(self.d_add_password)
        if not secret:
            self.highlight_border(self.d_add_secret)
            self.statusBar().showMessage("Eanble password can not be empty")
            self.d_add_secret.setFocus()
            return
        else:
            self.highlight_border_false(self.d_add_secret)
        if not port_number:
            self.highlight_border(self.d_add_port_number)
            self.statusBar().showMessage("Port Number can not be empty")
            self.d_add_port_number.setFocus()
            return
        else:
            self.highlight_border_false(self.d_add_port_number)

        # create the dictionary
        password = self.encrypt_password(password)
        secret = self.encrypt_password(secret)
        device = self.create_dictionary(
            hostname,
            ip_address,
            username,
            password,
            secret,
            device_type,
            port_number,
            os_type,
        )

        # add host_into inventory
        added = self.add_host_into_inventory(device)

        if added:
            QMessageBox.information(
                self, "Success", "Device added successfully")
            # create directory of the file
            self.create_device_directory(hostname)
            # clearing the fileds
            self.clear_add_devices_fileds()

            # Update the all device table
            self.clear_device_search_results()
            # update autocomplete list of ip_addresses and hostnames
            self.auto_complete_edit_results()
            self.auto_complete_search_results()
            # update devices in show commands combo box
            self.update_bt_all_devices()
            # update devices in group addition
            self.add_devices_for_group_selection()
            # update groups table
            self.fill_groups_table(self.get_all_groups())
            # update devices in inteface monitoring section
            # self.update_mon_all_devices()
            # update devices in all configurations section
            self.update_configs_all_devices()

    #          ____  _   _ _     _  __     _    ____  ____ ___ _____ ___ ___  _   _
    #         | __ )| | | | |   | |/ /    / \  |  _ \|  _ \_ _|_   _|_ _/ _ \| \ | |
    #         |  _ \| | | | |   | ' /    / _ \ | | | | | | | |  | |  | | | | |  \| |
    #         | |_) | |_| | |___| . \   / ___ \| |_| | |_| | |  | |  | | |_| | |\  |
    #         |____/ \___/|_____|_|\_\ /_/   \_\____/|____/___| |_| |___\___/|_| \_|
    # set path of csv file
    def check_csv_file(self, csv_file):
        regexp = (
            # device type
            r"\s*(Router|Switch)\s*"
            + ","
            # device os
            r"\s*cisco_(ios|xr|xe|nxos|asa)\s*"
            + ","
            # hostname
            r"\s*[\w+\-@$!]+\s*"
            + ","
            # ip address
            + r"\s*(25[0-4]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-4]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-4]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-4]|2[0-4][0-9]|[01]?[0-9][0-9]?)\s*"
            # + r"\s*([0-1]?[0-9]?[0-9]?|2[0-2][0-3])\.([0-1]?\d\d\.|[2]?[0-4]?\d?\.|25?[0-5]?\.){2}([0-1]\d\d|2[0-4]\d|25[0-5])\s*"
            + ","
            # username and password
            + r"(\s*[\w\-@$!]+\s*,){2}"
            # secret
            + r"("
            + r"[\w\-@$!]+"
            + r"\D|[\w\-@$!]+,"
            + r"\D|[\w\-@$!]+,\s*"
            + r"\D|\s*[\w\-@$!]+"
            + r"\D|\s*[\w\-@$!]+,"
            + r"\D|\s*[\w\-@$!]+,\s*"
            + r"\D|\s*[\w\-@$!]+\s*,\s*"
            + r"\D|[\w\-@$!]+\s*"
            + r"\D|[\w\-@$!]+\s*,"
            + r"\D|[\w\-@$!]+\s*,\s*"
            + r")"
            # port number

            r"\s*([1-9]|[1-5]?[0-9]{2,4}|6[1-4][0-9]{3}|65[1-4][0-9]{2}|655[1-2][0-9]|6553[1-5])[\s,]*"
            # + r"("
            # + r"\d{1,5}"
            # + r"|\d{1,5},"
            # + r"|\d{1,5},\s*"
            # + r"|\s*\d{1,5}"
            # + r"|\s*\d{1,5},"
            # + r"|\s*\d{1,5},\s*"
            # + r"|\s*\d{1,5}\s*"
            # + r"|\s*\d{1,5}\s*,"
            # + r"|\s*\d{1,5}\s*,\s*"
            # + r")?"
        )
        regex = re.compile(regexp)
        error_on_lines = list()
        i = 1
        for line in csv_file:
            result = regex.fullmatch(line)
            # print(regex.fullmatch(line))
            if result:
                print(f"Line {i} is valid")
            else:
                error_on_lines.append(str(i))
                print(f"Line {i} is Invalid")
            i += 1
        if error_on_lines:
            print("error on line " + ",".join(error_on_lines))
            QMessageBox.information(
                self, "Warning", "Error on line " + ",".join(error_on_lines)
            )
            return False
        else:
            QMessageBox.information(self, "Note", "csv file is valid")
            return True

    def read_csv_file(self, csv_file_path):
        try:
            with open(csv_file_path, "r") as handler:
                reader = csv.reader(handler, delimiter=",")
                device_cred_list = [", ".join(device) for device in reader]
                return device_cred_list
                # device_cred_list = [", ".join(device) for device in csv_file_content]
                # for row in reader:
                #     print(row)
        except Exception as error:
            QMessageBox.information(self, "Warning", str(error))

    def browse_file(self):
        url = QFileDialog.getOpenFileName(
            self, "Open a csv file", ".", "CSV FILE(*.csv);;All File(*)"
        )
        self.dev_add_txt_csv_file_path.setText(url[0])

    def bulk_device_addition(self):
        csv_file_path = self.dev_add_txt_csv_file_path.text()
        if csv_file_path:
            # file exists
            if os.path.isfile(csv_file_path):
                # check for valid csv file
                csv_file_content = self.read_csv_file(csv_file_path)
                valid_csv_file = self.check_csv_file(csv_file_content)
                devices = list()
                if valid_csv_file:
                    for device in csv_file_content:
                        devices.append(device.split(","))
                # set default port number
                port_number = "22"
                for device in devices:
                    # .strip will remove leading and ending zeros from the string
                    device_type = device[0].strip()
                    os_type = device[1].strip()
                    hostname = device[2].strip()
                    ip_address = device[3].strip()
                    username = device[4].strip()
                    password = device[5].strip()
                    secret = device[6].strip()
                    print(f"Port Number before={port_number}")
                    if len(device) >= 8:
                        if device[7].strip().isdigit():
                            port_number = device[7].strip()
                        else:
                            port_number = "22"
                    print(f"Port Number after={port_number}")
                    password = self.encrypt_password(password)
                    secret = self.encrypt_password(secret)
                    device = self.create_dictionary(
                        hostname,
                        ip_address,
                        username,
                        password,
                        secret,
                        device_type,
                        port_number,
                        os_type,
                    )
                    pprint(device)
                    # add host_into inventory
                    added = self.add_host_into_inventory(device)

                    if added:
                        QMessageBox.information(
                            self, "Success", f"{hostname} added successfully"
                        )

                        self.create_device_directory(hostname)
                        self.dev_add_txt_csv_file_path.setText("")
                        # Update the all device table
                        self.clear_device_search_results()
                        # update autocomplete list of ip_addresses and hostnames
                        self.auto_complete_edit_results()
                        self.auto_complete_search_results()
                        # update devices in show commands combo box
                        self.update_bt_all_devices()
                        # update devices in group addition
                        self.add_devices_for_group_selection()
                        # update groups table
                        self.fill_groups_table(self.get_all_groups())
                        # update devices in inteface monitoring section
                        # self.update_mon_all_devices()
                        # update devices in all configurations section
                        self.update_configs_all_devices()
                return

            else:
                QMessageBox.information(self, "Warning", "file does not exist")
                self.dev_add_txt_csv_file_path.setFocus()
                self.dev_add_txt_csv_file_path.setText("")
                return
        else:
            QMessageBox.information(
                self, "Warning", "Please enter the csv file path")
            self.dev_add_txt_csv_file_path.setFocus()
            return
