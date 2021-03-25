from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import *
from netmiko import ConnectHandler
from yaml import safe_load
import yaml
from pprint import pprint
import os


class groups(QDialog):
    def clear_group_all_user_search(self):
        self.fill_groups_table(self.get_all_groups())
        self.txt_g_all_group_name.setText("")
        self.txt_g_all_group_name.setFocus()

    def search_group(self):
        # get values
        searched_text = self.txt_g_all_group_name.text()
        groups = self.get_all_groups()
        searched_groups = list()
        count = 0
        for group in groups:
            if searched_text in group["group_name"]:
                searched_groups.append(group)
                count += 1
        if count == 0:
            QMessageBox.information(self, "Note", "No results found")
            self.clear_group_all_user_search()
        else:
            QMessageBox.information(self, "Note", f"{count} result(s) found")
            self.fill_groups_table(searched_groups)

    def add_devices_for_group_selection(self):
        devices = self.get_all_devices_hostname()
        # devices.sort()
        self.g_add_group_members.clear()
        self.g_add_group_members.addItems(devices)
        self.g_add_group_members.setSortingEnabled(True)

    def get_all_groups(self):
        self.check_for_group_file()
        group_file = self.get_group_file_path()
        groups = self.read_yaml_file(group_file)
        return groups

    def get_group_file_path(self):
        return os.path.join("hosts", "groups.yaml")

    def create_dictionary_for_group(self, group_name, group_members):
        return {"group_name": group_name, "group_members": group_members}

    def check_for_group_file(self):
        # check the directory
        dir_exists = os.path.isdir("hosts")
        group_file = self.get_group_file_path()
        if dir_exists:
            print("Folder exists")
        else:
            os.mkdir("hosts")
            # creating a dummy file
            group_name = "dummy"
            group_members = list()
            demo_group = self.create_dictionary_for_group(group_name, group_members)
            groups = list()
            groups.append(demo_group)

            f = open(group_file, "w")
            yaml.dump(groups, f, allow_unicode=True)
            return False

        # check for file existance
        file_exists = os.path.isfile(group_file)
        if not file_exists:
            print("group file does not exists")

            group_name = "dummy"
            group_members = list()
            demo_group = self.create_dictionary_for_group(group_name, group_members)
            groups = list()
            groups.append(demo_group)

            f = open(group_file, "w")
            yaml.dump(groups, f, allow_unicode=True)
            return False

        # file exists
        else:
            print("group file exists")
            return True

    def convert_group_file_into_list(self):
        group_file = self.get_group_file_path()
        groups = None
        with open(group_file, "r") as handler:
            groups = safe_load(handler)
        return groups

    def add_group_into_file(self, group_name, group_members):
        self.check_for_group_file()
        groups = self.convert_group_file_into_list()
        group = self.create_dictionary_for_group(group_name, group_members)
        if len(groups) == 1 and groups[0]["group_name"] == "dummy":
            groups.pop(0)
            groups.append(group)
        else:
            groups.append(group)
        print(group)
        pprint(groups)
        return groups

    def write_group_file(self, groups):
        group_file = self.get_group_file_path()
        f = open(group_file, "w+")
        yaml.dump(groups, f, allow_unicode=True)

    def clear_add_group_fields(self):
        self.g_add_groupname.setText("")
        self.g_add_group_members.selectionModel().clear()
        self.g_add_groupname.setFocus()

    def fill_groups_table(self, groups):
        groups_count = len(groups)
        self.tbl_groups.setRowCount(groups_count)
        i = 0
        for group in groups:
            # get the values
            group_name = group["group_name"]
            group_members = group["group_members"]

            # convert all group members list into a comma separated string
            group_members = ", ".join(group_members)

            # fill table
            self.tbl_groups.setItem(i, 0, QTableWidgetItem(group_name))
            self.tbl_groups.setItem(i, 1, QTableWidgetItem(group_members))

            i += 1

    def add_group(self):
        group_name = self.g_add_groupname.text()
        group_members = list()
        for device in self.g_add_group_members.selectedItems():
            group_members.append(device.text())

        self.check_for_group_file()
        groups = self.read_yaml_file(self.get_group_file_path())
        # check for group duplication
        duplicaton_occured = False
        for group in groups:
            if group["group_name"] == group_name:
                duplicaton_occured = True
                break
        if duplicaton_occured:
            print("Duplication occured")
            QMessageBox.information(
                self, "Warning", f"group {group_name} already exists"
            )
            self.clear_add_group_fields()
            return

        if group_name:
            groups = self.add_group_into_file(group_name, group_members)

            # ask for confirmation
            selection = QMessageBox.question(
                self,
                "Alert",
                "Add group",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if selection == QMessageBox.Yes:
                self.write_group_file(groups)
                QMessageBox.information(self, "Note", "Group added successfully")
                self.statusBar().showMessage("Succesfuly")
                self.fill_groups_table(self.get_all_groups())

            else:
                QMessageBox.information(self, "Note", "Group did not added")
                self.statusBar().showMessage("Failed")
            # clear selections

            self.clear_add_group_fields()

        # Need to add
        # 1. check for groupName duplication, already membership while editing
        # 2. add or remove a device to a certain group from devices section
        # 3. show all groups
        # 4. remove a group
        # 5. edit a group
        # reflect data changes
