from PyQt5.QtWidgets import QDialog, QMessageBox
from netmiko import ConnectHandler
from yaml import safe_load
import yaml
from pprint import pprint
import os


class groups(QDialog):
    def add_devices_for_group_selection(self):
        devices = self.get_all_devices_hostname()
        # devices.sort()
        self.g_add_group_members.addItems(devices)
        self.g_add_group_members.setSortingEnabled(True)

    def add_group(self):
        group_name = self.g_add_groupname.text()
        group_members = list()
        for device in self.g_add_group_members.selectedItems():
            group_members.append(device.text())
        pprint(group_members)
        if group_name and group_members:
            devices = self.convert_host_file_into_list()

            # add the selected users to the group
            for member in group_members:
                for device in devices:
                    if device["hostname"] == member:
                        device["groups"].append(group_name)
                        break
            # ask for confirmation
            selection = QMessageBox.question(
                self,
                "Alert",
                "Add group",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if selection == QMessageBox.Yes:
                self.write_inventory(devices)
                QMessageBox.information(self, "Note", "Group added successfully")
                self.statusBar().showMessage("Succesfuly")
            else:
                QMessageBox.information(self, "Note", "Group did not added")
                self.statusBar().showMessage("Failed")
            # clear selections

            self.g_add_groupname.setText("")
            self.g_add_group_members.selectionModel().clear()
            self.g_add_groupname.setFocus()

            # Need to add
            # 1. check for groupName duplication, already membership while editing
            # 2. add or remove a device to a certain group from devices section
            # 3. show all groups
            # 4. remove a group
            # 5. edit a group
            # reflect data changes
