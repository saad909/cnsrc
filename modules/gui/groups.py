from PyQt5.QtWidgets import QDialog, QMessageBox
from netmiko import ConnectHandler
from yaml import safe_load
import yaml
from pprint import pprint
import os


class groups(QDialog):
    def add_group(self):
        group_name = self.g_add_groupname.text()
        group_members = self.g_add_group_members.selectedItems.text()
        pprint(group_members)
