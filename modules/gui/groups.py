from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from yaml import safe_load
import yaml
from pprint import pprint
import os, re


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
        devices = self.convert_host_file_into_list()
        self.g_add_group_members.clear()
        for device in devices:
            device["hostname"] = "{:40s} {:10s}".format(
                device["hostname"], device["data"]["device_type"]
            )
            self.g_add_group_members.addItem(device["hostname"])

        # devices = [devices+"\t\t - " for deivce in devices["hostname"]]
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
        # first check for inventory file
        if not os.path.isfile(self.get_host_file_path()):
            if os.path.isfile(self.get_group_file_path()):
                os.remove(group_file)
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

    def check_all_group_members_type(self, group):
        if group:
            if group["group_members"]:
                device_type_list = list()
                all_devices = self.convert_host_file_into_list()
                for member in group["group_members"]:
                    for device in all_devices:
                        if device["hostname"] == member:
                            device_type_list.append(device["type"])
                            break
                if len(device_type_list) == 1:
                    return [True, device_type_list[0]]
                elif len(device_type_list) > 1:
                    first_type = device_type_list[0]
                    for index in range(1, len(device_type_list)):
                        if device_type_list[index] != first_type:
                            return False
                    return [True, first_type]
            else:
                return False

    def check_group_incompatibility(self, group):
        all_devices = self.convert_host_file_into_list()
        os_type_list = list()
        if group:
            if group["group_members"]:
                for member in group["group_members"]:
                    for device in all_devices:
                        if device["hostname"] == member:
                            os_type_list.append(device["data"]["device_type"])
                            break
            else:
                return False

        # print(group['group_members'])
        # print(os_type_list)
        incomptaible_group = False
        if len(group["group_members"]) > 1:
            first_member = os_type_list[0]
            for index in range(1, len(os_type_list)):
                if os_type_list[index] != first_member:
                    incomptaible_group = True
        else:
            return [True, os_type_list[0]]

        if incomptaible_group:
            return False
        else:
            return [True, first_member]

    def fill_groups_table(self, groups):
        groups_count = len(groups)
        self.tbl_groups.setRowCount(groups_count)
        i = 0
        for group in groups:
            # get the values
            group_name = group["group_name"]
            group_members = group["group_members"]
            os_type = "None"
            if group_members:
                member = group_members[0]
                host_file_exists = self.check_for_host_file()
                if host_file_exists:
                    all_devices = self.convert_host_file_into_list()
                    for device in all_devices:
                        if device["hostname"] == member:
                            os_type = device["data"]["device_type"]
                            break
                else:
                    QMessageBox.information(
                        self, "Warning", "Hosts inventory is not present"
                    )
                    self.tbl_groups.setRowCount(0)
                    return

            # convert all group members list into a comma separated string
            group_members = ", ".join(group_members)

            # fill table
            self.tbl_groups.setItem(i, 0, QTableWidgetItem(group_name))
            authentic_group = self.check_group_incompatibility(group)
            if authentic_group:
                self.tbl_groups.setItem(i, 1, QTableWidgetItem(authentic_group[1]))
            elif not group["group_members"]:
                self.tbl_groups.setItem(i, 1, QTableWidgetItem("None"))
            else:
                self.tbl_groups.setItem(i, 1, QTableWidgetItem("Incompatible"))
            self.tbl_groups.setItem(i, 2, QTableWidgetItem(group_members))

            i += 1

    def add_group(self):
        group_name = self.g_add_groupname.text()
        group_members = list()
        regexp = r"\s+\w+\s*"
        for device in self.g_add_group_members.selectedItems():
            group_members.append(re.sub(regexp, "", device.text()))

        if group_members:
            if group_members[0].strip() == "dummy" and len(group_members) == 1:
                QMessageBox.information(
                    self,
                    "Warning",
                    "Can not add dummy device into a group\nPlease first add a device",
                )
                self.clear_add_group_fields()
                return

        self.check_for_group_file()
        groups = self.read_yaml_file(self.get_group_file_path())
        # check group name not equal to router or switch
        if group_name == "router" or group_name == "switch":
            QMessageBox.information(
                self, "Warning", r"group name can't be 'router' or 'switch'"
            )
            self.clear_add_group_fields()
            return
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

        if group_name and group_members:
            # check for incomptaible grouping
            devices = self.convert_host_file_into_list()
            all_members = list()
            for member in group_members:
                for device in devices:
                    if device["hostname"] == member:
                        all_members.append(device)
            match = True
            if all_members:
                first_device = all_members[0]
                list_length = len(all_members)
                for index in range(1, list_length):
                    if (
                        first_device["data"]["device_type"]
                        != all_members[index]["data"]["device_type"]
                    ):
                        match = False

                if not match:
                    QMessageBox.information(self, "Warning", "Incompatible grouping")
                    return

            print(group_members)
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
                self.clear_device_search_results()
                self.clear_device_search_results()
                self.auto_complete_group_edit_search_results()
                self.auto_complete_group_search_results()
                self.update_show_commands_groups_combobox()
            else:
                QMessageBox.information(self, "Note", "Group did not added")
                self.statusBar().showMessage("Failed")
            # clear selections

            self.clear_add_group_fields()

    def clear_edit_group_fields(self):
        self.searched_groupname = self.txt_g_edit_groupname.text()
        self.txt_g_edit_groupname.setText("")
        self.g_edit_groupname.setText("")
        self.g_edit_group_members.clear()
        self.txt_g_edit_groupname.setFocus()

    def delete_group(self):
        # get values from gui
        searched_groupname = self.g_edit_groupname.text()
        groups = self.get_all_groups()
        group_index = -1
        i = 0
        for group in groups:
            if group["group_name"] == searched_groupname:
                group_index = i
            i += 1

        if group_index == -1:
            QMessageBox.information(self, "Note", "No result found")
            return
        else:
            selection = QMessageBox.question(
                self,
                "Warning",
                "Do you really want to delete the group?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Cancel,
            )
            if selection == QMessageBox.Yes:
                groups.pop(group_index)
                # write to group file
                self.write_group_file(groups)
                self.fill_groups_table(self.get_all_groups())
                self.clear_edit_group_fields()
                self.clear_device_search_results()
                self.update_show_commands_groups_combobox()
            elif selection == QMessageBox.Cancel:
                self.clear_edit_group_fields()

    def edit_group_search(self):
        # get values from gui
        searched_groupname = self.txt_g_edit_groupname.text()
        if searched_groupname:
            groups = self.get_all_groups()
            group_index = -1
            i = 0
            for group in groups:
                if group["group_name"] == searched_groupname:
                    group_index = i
                    break
                i += 1
            if group_index == -1:
                QMessageBox.information(self, "Note", "No result found")
                return
            else:
                # fill the fileds
                self.clear_edit_group_fields()
                self.g_edit_groupname.setText(groups[group_index]["group_name"])
                pprint(groups[group_index]["group_members"])
                devices = self.convert_host_file_into_list()
                for device in devices:
                    device["hostname"] = "{:40s} {:10s}".format(
                        device["hostname"], device["data"]["device_type"]
                    )
                    self.g_edit_group_members.addItem(device["hostname"])
                # self.g_edit_group_members.addItems(self.get_all_devices_hostname())

                # now higlight the group members of group in qlist widget
                group_members = groups[group_index]["group_members"]

                index = list()
                devices = self.convert_host_file_into_list()
                # devices['hostname'].sort()
                i = 0
                for device in devices:
                    for member in group_members:
                        if device["hostname"] == member:
                            index.append(i)
                    i += 1
                pprint(index)
                for i in index:
                    devices[i]["hostname"] = "{:40s} {:10s}".format(
                        devices[i]["hostname"], devices[i]["data"]["device_type"]
                    )
                    matching_items = self.g_edit_group_members.findItems(
                        devices[i]["hostname"], Qt.MatchExactly
                    )
                    for item in matching_items:
                        item.setSelected(True)

    def edit_group(self):
        # get values from gui - if not empty groupname
        searched_group_name = self.searched_groupname
        group_name = self.g_edit_groupname.text()
        if group_name == "dummy":
            QMessageBox.information(
                self, "Warning", "Can not edit dummy group.Please add a group first"
            )
            self.g_edit_groupname.setFocus()
            self.clear_edit_group_fields()
            return
        group_members = list()
        regexp = r"\s+\w+\s*"
        for device in self.g_edit_group_members.selectedItems():
            group_members.append(re.sub(regexp, "", device.text()))
        # for device in self.g_edit_group_members.selectedItems():
        #     group_members.append(device.text())
        for member in group_members:
            if member.strip() == "dummy":
                QMessageBox.information(
                    self,
                    "Warning",
                    "Can not add dummy device into a group.\nPlease select other devices if present",
                )
                self.g_edit_groupname.setFocus()
                self.clear_edit_group_fields()
                return
        edited_group = self.create_dictionary_for_group(group_name, group_members)
        all_groups = self.get_all_groups()

        # check group name not equal to router or switch
        if group_name == "Router" or group_name == "Switch":
            QMessageBox.information(
                self, "Warning", r"group name can't be 'Router' or 'Switch'"
            )
            self.g_edit_groupname.setFocus()
            return
        if group_name and group_members:
            # check for incomptaible grouping
            devices = self.convert_host_file_into_list()
            all_members = list()
            for member in group_members:
                for device in devices:
                    if device["hostname"] == member:
                        all_members.append(device)
            match = True
            first_device = all_members[0]
            list_length = len(all_members)
            for index in range(1, list_length):
                if (
                    first_device["data"]["device_type"]
                    != all_members[index]["data"]["device_type"]
                ):
                    match = False

            if not match:
                QMessageBox.information(self, "Warning", "Incompatible grouping")
                return

            # get the index of target group
            group_index = -1
            i = 0
            for group in all_groups:
                if group["group_name"] == searched_group_name:
                    group_index = i
                    break
                i += 1

            # check for group duplication
            duplicaton_occured = False
            groups = self.convert_group_file_into_list()
            i = 0
            for group in groups:
                if i == group_index:
                    continue
                if group["group_name"] == group_name:
                    duplicaton_occured = True
                    break
                i += 1
            if duplicaton_occured:
                print("Duplication occured")
                QMessageBox.information(
                    self, "Warning", f"group {group_name} already exists"
                )
                self.clear_edit_group_fields()
                return

            print(
                "------------------ Your target group is(index = {0}) ------------------".format(
                    group_index
                )
            )
            pprint(all_groups[group_index])
            # check for changes done
            print(
                "------------------ Your new group is(index = {0}) ------------------".format(
                    group_index
                )
            )
            pprint(edited_group)
            for group in all_groups:
                if group == edited_group:
                    QMessageBox.information(self, "Note", "You made no changes")
                    return
            # ask for changes
            selection = QMessageBox.question(
                self,
                "Alert",
                "Do you really want to edit group?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if selection == QMessageBox.Yes:
                all_groups[group_index] = edited_group
                self.write_group_file(all_groups)
                QMessageBox.information(self, "Note", "Edited successfully")
                self.fill_groups_table(self.get_all_groups())
                self.statusBar().showMessage("Succesfuly")
                self.clear_edit_group_fields()
                self.clear_device_search_results()
                self.txt_g_edit_groupname.setFocus()
                self.auto_complete_group_edit_search_results()
                self.auto_complete_group_search_results()
                self.update_show_commands_groups_combobox()

        else:
            QMessageBox.information(self, "Warning", "Group name can't be empty")
            self.clear_edit_group_fields()
            self.txt_g_edit_groupname.setFocus()
            return

    def get_all_groups_names(self):
        groups = self.get_all_groups()
        all_groups_list = list()
        for group in groups:
            all_groups_list.append(group["group_name"])
        return all_groups_list

    def auto_complete_group_edit_search_results(self):
        self.auto_fill(self.get_all_groups_names(), self.txt_g_edit_groupname)

    def auto_complete_group_search_results(self):
        self.auto_fill(self.get_all_groups_names(), self.txt_g_all_group_name)
