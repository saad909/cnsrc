import re
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pprint import pprint
import pandas as pd
import os


class devices_func(QDial):

    # _____                       _                  ____ ______     __
    # | ____|_  ___ __   ___  _ __| |_    __ _ ___   / ___/ ___\ \   / /
    # |  _| \ \/ / '_ \ / _ \| '__| __|  / _` / __| | |   \___ \\ \ / /
    # | |___ >  <| |_) | (_) | |  | |_  | (_| \__ \ | |___ ___) |\ V /
    # |_____/_/\_\ .__/ \___/|_|   \__|  \__,_|___/  \____|____/  \_/
    #           |_|

    def export_file_path(self, box_to_set_path):
        filename = QFileDialog.getSaveFileName(
            self, "Save File", ".", "Excel File (*.xlsx);;All files(*)"
        )[0]
        # Append extension if not there yet
        if filename:
            if not filename.endswith(".xlsx"):
                filename += ".xlsx"
            box_to_set_path.setText(filename)
            return
        else:
            QMessageBox.information(
                self, "Failed", "Please select path"
            )
            return

    def export_table(self, table, file_path_widget):
        filename = file_path_widget.text()
        # filename not given
        if not filename or not filename.endswith(".xlsx"):
            QMessageBox.information(self, "Warning", "Please first enter the file path")
            file_path_widget.setFocus()
            return

        else:

            try:
                columnHeaders = []
                # create column header list
                for j in range(table.model().columnCount()):
                    columnHeaders.append(table.horizontalHeaderItem(j).text())

                df = pd.DataFrame(columns=columnHeaders)

                # create dataframe object recordset
                for row in range(table.rowCount()):
                    for col in range(table.columnCount()):
                        df.at[row, columnHeaders[col]] = table.item(row, col).text()

                df.to_excel(filename, index=False)
                print("Excel file exported")
                QMessageBox.information(self, "Success", "Excel file exported")
                file_path_widget.setText("")
            except Exception as error:
                QMessageBox.information(self, "Failed", str(error))

    # clear the text boxes
    def clear_text_box(self, widget):
        widget.setText("")

    def highlight_border_false(self, widget):
        widget.setStyleSheet("")

    ##### higlight the border-> make red if left empty ######

    def highlight_border(self, widget):
        widget.setStyleSheet("border-color: darkred;")

    ###################### get ip in correct form  ######################

    def get_valid_ip(self, textBox):
        # validate ip address input
        octet = "(?:[0-1]?[0-9]?[0-9]|2?[0-4]?[0-9]|25?[0-4])"
        ipRegExp = QRegExp(
            "^" + octet + r"\." + octet + r"\." + octet + r"\." + octet + "$"
        )
        # ipRegExp = QRegExp(
        #     r"\s*([0-1]?[0-9]?[0-9]?|2[0-2][0-3])\.([0-1]?\d\d\.|[2]?[0-4]?\d?\.|25?[0-5]?\.){2}([0-1]\d\d|2[0-4]\d|25[0-5])\s*"
        # )
        ipValidator = QRegExpValidator(ipRegExp)
        textBox.setValidator(ipValidator)

    def get_valid_subnet(self, textBox):
        # validate ip address input
        octet = "(?:[0-1]?[0-9]?[0-9]|2?[0-4]?[0-9]|25?[0-5])"
        ipRegExp = QRegExp(
            "^" + octet + r"\." + octet + r"\." + octet + r"\." + octet + "$"
        )
        # ipRegExp = QRegExp(
        #     r"\s*([0-1]?[0-9]?[0-9]?|2[0-2][0-3])\.([0-1]?\d\d\.|[2]?[0-4]?\d?\.|25?[0-5]?\.){2}([0-1]\d\d|2[0-4]\d|25[0-5])\s*"
        # )
        ipValidator = QRegExpValidator(ipRegExp)
        textBox.setValidator(ipValidator)

    def is_subnet_mask_complete(self, ipTextBox):

        ip_address = ipTextBox.text()
        # reg_exp = r"\s*([0-1]?[0-9]?[0-9]?|2[0-2][0-3])\.([0-1]?\d\d\.|[2]?[0-4]?\d?\.|25?[0-5]?\.){2}([0-1]\d\d|2[0-4]\d|25[0-5])\s*"

        octet = "(?:[0-1]?[0-9]?[0-9]|2?[0-4]?[0-9]|25?[0-5])"
        reg_exp = "^" + octet + r"\." + octet + r"\." + octet + r"\." + octet + "$"
        result = list()
        result = re.findall(reg_exp, ip_address)
        if len(result) == 1:
            return True
        else:
            return False

    def is_ip_complete(self, ipTextBox):

        ip_address = ipTextBox.text()
        # reg_exp = r"\s*([0-1]?[0-9]?[0-9]?|2[0-2][0-3])\.([0-1]?\d\d\.|[2]?[0-4]?\d?\.|25?[0-5]?\.){2}([0-1]\d\d|2[0-4]\d|25[0-5])\s*"

        octet = "(?:[0-1]?[0-9]?[0-9]|2?[0-4]?[0-9]|25?[0-4])"
        reg_exp = "^" + octet + r"\." + octet + r"\." + octet + r"\." + octet + "$"
        result = list()
        result = re.findall(reg_exp, ip_address)
        if len(result) == 1:
            return True
        else:
            return False

    def get_valid_identifier(self, textBox):
        # validate ip address input
        regexp = QRegExp(r"[\w_\-!#@]+")
        # ipRegExp = QRegExp(
        #     r"\s*([0-1]?[0-9]?[0-9]?|2[0-2][0-3])\.([0-1]?\d\d\.|[2]?[0-4]?\d?\.|25?[0-5]?\.){2}([0-1]\d\d|2[0-4]\d|25[0-5])\s*"
        # )
        validator = QRegExpValidator(regexp)
        textBox.setValidator(validator)


    def clear_add_devices_fileds(self):
        self.clear_text_box(self.d_add_hostname)
        self.clear_text_box(self.d_add_ip_address)
        self.clear_text_box(self.d_add_username)
        self.clear_text_box(self.d_add_password)
        self.clear_text_box(self.d_add_secret)
        self.d_add_device_type.setCurrentIndex(0)

    ################################ ALL Devices Section #################################

    def fill_devices_table(self, devices):
        devices_count = len(devices)
        self.tbl_devices.setRowCount(devices_count)
        i = 0
        for device in devices:

            # get the values
            hostname = device["hostname"]
            ip = device["data"]["host"]
            username = device["data"]["username"]
            password = device["data"]["password"]
            secret = device["data"]["secret"]
            device_type = device["type"]
            port_number = device["data"]["port"]
            # groups based on device type
            # groups = device["groups"]
            # user defined groups
            other_groups = list()
            all_custom_groups = self.get_all_groups()
            for group in all_custom_groups:
                if hostname in group["group_members"]:
                    other_groups.append(group["group_name"])

            all_groups = other_groups
            os_type = device["data"]["device_type"]

            self.tbl_devices.setItem(i, 0, QTableWidgetItem(hostname))
            self.tbl_devices.setItem(i, 1, QTableWidgetItem(ip))
            self.tbl_devices.setItem(i, 2, QTableWidgetItem(username))

            # decrypt passwords
            if devices[0]["hostname"] != "dummy":
                password = self.decrypt_password(password)
                secret = self.decrypt_password(secret)
                print(f"Password: {password}")
                print(f"Secret: {secret}")

            self.tbl_devices.setItem(i, 3, QTableWidgetItem(password))
            self.tbl_devices.setItem(i, 4, QTableWidgetItem(secret))

            self.tbl_devices.setItem(i, 5, QTableWidgetItem(", ".join(all_groups)))
            self.tbl_devices.setItem(i, 6, QTableWidgetItem(device_type))
            self.tbl_devices.setItem(i, 7, QTableWidgetItem(port_number))
            self.tbl_devices.setItem(i, 8, QTableWidgetItem(os_type))

            i += 1

    def update_devices_table(self):
        not_empty = self.check_for_host_file()
        if not_empty:
            print("host file is not empty")
        else:
            print("host file is empty")
        if not_empty:
            test_devices = self.convert_host_file_into_list()

            host_file = self.get_host_file_path()
            devices = self.read_yaml_file(host_file)
            # fill the table
        else:
            self.fill_devices_table(devices)

    ###################### search device ######################
    def auto_complete_search_results(self):
        all_ip_addresses_list = self.get_all_devices_ip()
        all_hostnames_list = self.get_all_devices_hostname()
        self.auto_fill(all_ip_addresses_list, self.txt_d_all_ip_address)
        self.auto_fill(all_hostnames_list, self.txt_d_all_hostname)

    def get_all_devices_hostname(self):
        devices = self.convert_host_file_into_list()
        all_hostnames = list()
        for device in devices:
            all_hostnames.append(device["hostname"])
        return all_hostnames

    def get_all_devices_ip(self):
        devices = self.convert_host_file_into_list()
        all_ips = list()
        for device in devices:
            all_ips.append(device["data"]["host"])
        return all_ips

    def auto_fill(self, completion_list, destination_box):
        completer = QCompleter(completion_list)
        destination_box.setCompleter(completer)

    def search_device(self):
        # check the empty values
        hostname = self.txt_d_all_hostname.text()
        ip_address = self.txt_d_all_ip_address.text()
        print(hostname, ip_address)

        # ip address and hostname both are empty
        if not (hostname or ip_address):
            QMessageBox.information(self, "Note", "Please enter ip address or hostname")
            self.txt_d_all_ip_address.setFocus()
            self.highlight_border(self.txt_d_all_hostname)
            return
        search_key = None

        # ip address and hostname both are given
        if hostname and ip_address:
            # default search is by ip_address

            search_key = ip_address

            devices = self.convert_host_file_into_list()

            searched_devices = list()

            for device in devices:
                if search_key in device["data"]["host"]:
                    searched_devices.append(device)

            if searched_devices:
                self.clear_device_search_results()
                QMessageBox.information(
                    self,
                    "Infromation",
                    "{} result(s) were found".format(len(searched_devices)),
                )
                pprint(searched_devices)
                self.fill_devices_table(searched_devices)
                return
            else:
                QMessageBox.information(
                    self, "Note", "No match found for ip now searching using hostname"
                )

                search_key = hostname
                devices = self.convert_host_file_into_list()
                searched_devices = list()
                for device in devices:
                    if search_key.lower() in device["hostname"].lower():
                        searched_devices.append(device)
                if searched_devices:
                    self.clear_device_search_results()
                    QMessageBox.information(
                        self,
                        "Infromation",
                        "{} result(s) were found".format(len(searched_devices)),
                    )
                    pprint(searched_devices)
                    self.fill_devices_table(searched_devices)
                    return
                else:
                    QMessageBox.information(
                        self, "Note", "No result(s) found using hostname "
                    )
                    self.clear_device_all_user_search()
                    self.txt_d_all_ip_address.setFocus()
                    return

        # only hostname is given
        if hostname and not (ip_address):
            search_key = hostname
            devices = self.convert_host_file_into_list()
            searched_devices = list()
            for device in devices:
                if search_key.lower() in device["hostname"].lower():
                    searched_devices.append(device)
            if searched_devices:
                self.clear_device_search_results()
                QMessageBox.information(
                    self,
                    "Infromation",
                    "{} result(s) were found".format(len(searched_devices)),
                )
                pprint(searched_devices)
                self.fill_devices_table(searched_devices)
                return
            else:
                QMessageBox.information(self, "Note", "No result found")
                self.clear_device_search_results()
                self.txt_d_all_hostname.setFocus()
                return

        # only  ip address is given
        if ip_address and not (hostname):
            search_key = ip_address
            devices = self.convert_host_file_into_list()
            searched_devices = list()
            for device in devices:
                if search_key in device["data"]["host"]:
                    searched_devices.append(device)
            if searched_devices:
                self.clear_device_search_results()
                QMessageBox.information(
                    self,
                    "Infromation",
                    "{} result(s) were found".format(len(searched_devices)),
                )
                pprint(searched_devices)
                self.fill_devices_table(searched_devices)
                return
            else:
                QMessageBox.information(self, "Note", "No result found")
                self.clear_device_search_results()
                self.txt_d_all_ip_address.setFocus()
                return

    def clear_device_search_results(self):
        self.clear_text_box(self.txt_d_all_ip_address)
        self.clear_text_box(self.txt_d_all_hostname)

        self.fill_devices_table(self.convert_host_file_into_list())

    ################################ Delete or edit the device #################################

    ##### clear top bar search results ######
    def auto_complete_edit_results(self):
        all_hostnames = self.get_all_devices_hostname()
        self.auto_fill(all_hostnames, self.txt_d_edit_hostname)

    ###################### edit the deivce ######################

    def clear_edit_search_results(self):
        self.d_edit_hostname.setText("")
        self.d_edit_ip_address.setText("")
        self.d_edit_username.setText("")
        self.d_edit_password.setText("")
        self.d_edit_secret.setText("")
        self.d_edit_port_number.setText("")
        self.d_edit_device_type.setCurrentIndex(0)
        self.d_edit_cb_os_type.setCurrentIndex(0)

    def fill_edit_search_results(self, device):
        if device["hostname"] == "dummy":
            QMessageBox.information(self, "Note", "Dummy device can't be edited")
            self.clear_device_edit_user_search()
            self.txt_d_edit_hostname.setFocus()
            return
        self.d_edit_hostname.setText(device["hostname"])
        self.d_edit_ip_address.setText(device["data"]["host"])
        self.d_edit_username.setText(device["data"]["username"])
        self.d_edit_password.setText(self.decrypt_password(device["data"]["password"]))
        self.d_edit_secret.setText(self.decrypt_password(device["data"]["secret"]))
        self.d_edit_port_number.setText(device["data"]["port"])
        os_type_index = self.d_edit_cb_os_type.findText(device["data"]["device_type"])
        self.d_edit_cb_os_type.setCurrentIndex(os_type_index)
        dev_type_index = self.d_edit_device_type.findText(device["type"])
        self.d_edit_device_type.setCurrentIndex(dev_type_index)

    def edit_search_device(self):
        self.clear_edit_search_results()
        # check the empty values
        hostname = self.txt_d_edit_hostname.text()

        # ip address and hostname both are empty
        if not hostname:
            QMessageBox.information(self, "Note", "Please enter hostname first")
            self.txt_d_edit_hostname.setFocus()
            self.highlight_border(self.txt_d_edit_hostname)
            return
        # only hostname is given
        search_key = hostname
        devices = self.convert_host_file_into_list()
        searched_device = None
        for device in devices:
            if search_key == device["hostname"]:
                searched_device = device
                break
        if searched_device:
            pprint(searched_device)
            self.fill_edit_search_results(searched_device)
            self.device_before = searched_device
            return
        else:
            QMessageBox.information(self, "Note", "Host not found")
            self.clear_device_edit_user_search()
            self.txt_d_edit_hostname.setFocus()

    def change_group_type(self, device, group_type):
        # get the device before group
        if self.device_before["groups"][0] == group_type:
            return
        else:
            device["groups"][0] = group_type

    def check_group_members_os_type(self, device_name):
        all_devices = self.convert_host_file_into_list()
        for device in all_devices:
            if device["hostname"] == device_name:
                return device["data"]["device_type"]

    def synchronize_editing(self, old_name, new_name):
        print(f"------------------Host name before = {old_name}------------")
        print(f"------------------Host name after = {new_name}------------")
        all_groups = self.convert_group_file_into_list()
        target_groups = list()
        index = 0
        for group in all_groups:
            for group_member in group['group_members']:
                i = 0
                if group_member == old_name:
                    print(f"------------------Host name before = \n{group}")
                    if old_name != new_name:
                        group['group_members'][i] = new_name
                    print(f"------------------Host name after = \n{group}")
                    target_groups.append(index)
                    break
                i += 1
            index += 1

        self.write_group_file(all_groups)
        # Target Groups
        QMessageBox.information(self, "Warning", f"Target Groups are {target_groups}")

        # checking for os type match
        groups = list()
        for index in target_groups:
            groups.append(all_groups[index])
        print("Target groups are")
        print(groups)

        all_devices = self.convert_host_file_into_list()
        for group in groups:
            os_type_list = list()
            for member in group["group_members"]:
                for device in all_devices:
                    if device["hostname"] == member:
                        os_type_list.append(device["data"]["device_type"])
                        break
            if os_type_list:
                print("--------- OS TYPE LIST--------------")
                print(os_type_list)
                first_member = os_type_list[0]
                for index in range(1, len(os_type_list)):
                    if os_type_list[index] != first_member:
                        QMessageBox.information(
                            self,
                            f"Warning",
                            f"{group['group_name']} group has incomptaible members",
                        )
                        break

            # first_member = group['group_members'][0]
            # for index in range(1,len(group['group_members'])):
            #     for device in all_devices:
            #         if device['hostname'] == group['group_member'][index]:
            #             os_type_list.append(device['data']['device_type'])
            #             break

    def edit_device(self):
        hostname = self.d_edit_hostname.text()
        ip_address = self.d_edit_ip_address.text()
        username = self.d_edit_username.text()
        password = self.d_edit_password.text()
        secret = self.d_edit_secret.text()
        port_number = self.d_edit_port_number.text()
        device_type = str(self.d_edit_device_type.currentText())
        os_type = str(self.d_edit_cb_os_type.currentText())

        # encrypt password
        password = self.encrypt_password(password)
        secret = self.encrypt_password(secret)
        print("----------------- Encryption password --------------------")
        print(self.decrypt_password(password))
        print(self.decrypt_password(secret))
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

        ##### check for empty boxes ######

        if not hostname:
            self.highlight_border(self.d_edit_hostname)
            self.statusBar().showMessage("Hostname can not be empty")
            self.d_edit_hostname.setFocus()
            return
        else:
            self.highlight_border_false(self.d_edit_hostname)
        if self.d_edit_ip_address and self.is_ip_complete(self.d_edit_ip_address):
            self.highlight_border_false(self.d_edit_ip_address)
        else:
            self.highlight_border(self.d_edit_ip_address)
            self.statusBar().showMessage("Invalid Ip Address")
            self.d_edit_ip_address.setFocus()

            return

        if not username:
            self.highlight_border(self.d_edit_username)
            self.statusBar().showMessage("username can not be empty")
            self.d_edit_username.setFocus()
            return
        else:
            self.highlight_border_false(self.d_edit_username)
        if not password:
            self.highlight_border(self.d_edit_password)
            self.statusBar().showMessage("password can not be empty")
            self.d_edit_password.setFocus()
            return
        else:
            self.highlight_border_false(self.d_edit_password)
        if not secret:
            self.highlight_border(self.d_edit_secret)
            self.statusBar().showMessage("Eanble password can not be empty")
            self.d_edit_secret.setFocus()
            return
        else:
            self.highlight_border_false(self.d_edit_secret)
        if not port_number:
            self.highlight_border(self.d_edit_port_number)
            self.statusBar().showMessage("Port Number can not be empty")
            self.d_edit_port_number.setFocus()
            return
        else:
            self.highlight_border_false(self.d_edit_port_number)

        if device == self.device_before:
            QMessageBox.information(self, "Warning", "You made no changes")
            return

        else:

            ##### check for ip or hostname duplication ######

            hostname_before = self.device_before["hostname"]
            ip_before = self.device_before["data"]["host"]

            hostname_changed = None
            if hostname != hostname_before:
                hostname_changed = True
                # hostname check
                all_hostnames = self.get_all_devices_hostname()
                status = None
                if hostname in all_hostnames:
                    status = True
                if status:
                    # self.d_edit_hostname.setFocus()
                    self.highlight_border(self.d_edit_hostname)
                    QMessageBox.information(
                        self,
                        "Waring",
                        f"{hostname}: {self.device_before['data']['host']} also has the same hostname",
                    )
                    return
            # ip check
            if ip_address != ip_before:
                all_devices_list = self.convert_host_file_into_list()
                status = None
                for device in all_devices_list:
                    if device["data"]["host"] == ip_address:
                        status = True
                if status:
                    # self.d_edit_ip_address.setFocus()
                    self.highlight_border(self.d_edit_ip_address)
                    QMessageBox.information(
                        self,
                        "Waring",
                        f"{hostname}: {hostname_before} also has the same ip address and port number",
                    )
                    return

            selection = QMessageBox.question(
                self,
                "Alert",
                "Do you want to make changes",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.No,
            )
            if selection == QMessageBox.Yes:
                devices = self.convert_host_file_into_list()
                # get the index
                device_index = None
                i = 0
                print("---------------- Devices Before ----------------")
                pprint(devices)
                for device in devices:
                    if self.device_before["hostname"] == device["hostname"]:
                        device_index = i
                    i += 1
                devices[device_index]["hostname"] = hostname
                devices[device_index]["data"]["host"] = ip_address
                devices[device_index]["data"]["username"] = username
                # save encrypted passwords
                devices[device_index]["data"]["password"] = password
                devices[device_index]["data"]["secret"] = secret
                devices[device_index]["data"]["port"] = port_number
                devices[device_index]["data"]["device_type"] = os_type
                devices[device_index]["type"] = device_type

                # device group based on type
                if devices[device_index]["type"] == "router":
                    self.change_group_type(devices[device_index], "router")

                elif devices[device_index]["type"] == "switch":
                    self.change_group_type(devices[device_index], "switch")

                print("---------------- Devices After Editing ----------------")
                pprint(devices)

                self.write_inventory(devices)

                QMessageBox.information(self, "Success", "Data modified successfully")
                try:
                    if hostname_before != hostname:
                        os.rename(os.path.join
                          (
                              "hosts","configs",hostname_before
                          )
                          ,os.path.join("hosts","configs",hostname)
                  )
                except Exception as error:
                    print(str(error))
                # reflect changes in groups.yaml file
                self.synchronize_editing(hostname_before, hostname)
                # update groups table
                self.fill_groups_table(self.get_all_groups())
                # update all devices table
                self.clear_device_search_results()
                # update autocomplete list of ip_addresses and hostnames
                self.auto_complete_edit_results()
                self.auto_complete_search_results()
                # clear search results
                self.clear_edit_search_results()
                self.clear_device_edit_user_search()
                # update devices in show commands combo boxes
                self.update_bt_all_devices()
                # update devices in group addition
                self.add_devices_for_group_selection()
                # update devices in inteface monitoring section
                # self.update_mon_all_devices()
                #update devices in all configurations section
                self.update_configs_all_devices()
                self.update_remote_devices()
            elif selection == QMessageBox.No:
                self.clear_edit_search_results()
                self.clear_device_edit_user_search()

    ##################### delete the device ######################
    def clear_device_edit_user_search(self):
        self.txt_d_edit_hostname.setText("")

    def synchronize_deletion(self, device_name):
        all_groups = self.convert_group_file_into_list()
        for group in all_groups:
            index = -1
            i = 0
            for member in group["group_members"]:
                if member == device_name:
                    index = i
                    break
                i += 1
            if index != -1:
                group["group_members"].pop(index)
        self.write_group_file(all_groups)
        return

    def delete_device(self):
        hostname_before = self.device_before["hostname"]
        hostname = self.d_edit_hostname.text()
        if hostname:
            if hostname == hostname_before:
                selection = QMessageBox.question(
                    self,
                    "Warning",
                    "Do you want to delete the device ?",
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                    QMessageBox.No,
                )
                if selection == QMessageBox.Yes:
                    devices = self.convert_host_file_into_list()
                    # getting the deletion device index
                    index = None
                    i = 0
                    for device in devices:
                        if device["hostname"] == hostname:
                            index = i
                            break
                        i += 1

                    devices.pop(index)

                    # write to the inventory file
                    self.write_inventory(devices)

                    QMessageBox.information(
                        self, "Success", "host deleted successfully"
                    )
                    # reflect changes in groups.yaml file
                    self.synchronize_deletion(hostname)
                    # update all devices table
                    self.clear_device_search_results()
                    # update autocomplete list of ip_addresses and hostnames
                    self.auto_complete_edit_results()
                    self.auto_complete_search_results()
                    # clear search results
                    self.clear_edit_search_results()
                    self.clear_device_edit_user_search()
                    # update devices in show commands combo boxes
                    self.update_bt_all_devices()
                    # update devices in group addition
                    self.add_devices_for_group_selection()
                    # update groups table
                    self.fill_groups_table(self.get_all_groups())
                    # self.update_mon_all_devices()
                    #update devices in all configurations section
                    self.update_configs_all_devices()
                    self.update_remote_devices()
                else:
                    self.clear_edit_search_results()
                    self.clear_device_edit_user_search()
            else:
                QMessageBox.information(self, "Failed", "You alterd the results")
                self.clear_edit_search_results()
                self.clear_device_edit_user_search()
        else:
            QMessageBox.information(self, "Failed", "hostname can't be empty")
            self.clear_edit_search_results()
            self.clear_device_edit_user_search()
