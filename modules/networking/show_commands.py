from PyQt5.QtWidgets import *
import os
import concurrent.futures as cf
from yaml import safe_load
# from pprint import pprint


class show_commands(QDialog):
    def update_show_commands_groups_combobox(self):
        self.cb_bt_all_groups.clear()
        self.cb_bt_all_groups.addItems(
            ["Select a group", "switch", "router"] + self.get_all_groups_names()
        )

    def disable_box(self, checking_box, box_to_disable):

        self.device_section = False

        current_index = checking_box.currentIndex()
        if current_index == 0:

            self.device_selection = False
            box_to_disable.setEnabled(True)
            self.show_commands_submit_button()

        elif current_index != 0:

            self.device_selection = True
            box_to_disable.setEnabled(False)
            self.show_commands_submit_button()

        # command seelection

    def show_commands_submit_button(self):

        if self.device_selection and self.cb_bt_all_commands.currentIndex() != 0:
            self.config_show_btn_submit.setEnabled(True)
        else:
            self.config_show_btn_submit.setEnabled(False)

            # | | ___   __ _(_) ___
            # | |/ _ \ / _` | |/ __|
            # | | (_) | (_| | | (__
            # |_|\___/ \__, |_|\___|
            #         |___/

    def get_command(self, command_text):
        file_name = os.path.join("hosts", "show commands", command_text+".cfg")
        with open(file_name, 'r') as handler:
            command = handler.read()
        return command

    # this will start running show commands procedure
    def run_show_command(self):
        device_name = None
        self.statusBar().showMessage("")
        device_selection = self.cb_bt_all_devices.isEnabled()

        # if single device is selected
        if device_selection:
            device_name = self.cb_bt_all_devices.currentText()
            command_text = self.cb_bt_all_commands.currentText()
            self.command = self.get_command(command_text)
            self.show_cmd_against_device(
                device_name)

        # if group is selected
        else:
            group_name = self.cb_bt_all_groups.currentText()
            command_text = self.cb_bt_all_commands.currentText()
            self.command = self.get_command(command_text)
            # print(command)
            self.show_cmd_against_group(group_name)

    def get_custom_group_members(self, group_name):
        all_groups = self.get_all_groups()
        group_members = None
        for group in all_groups:
            try:
                if group['group_name'] == group_name:
                    group_members = group['group_members']
            except Exception as error:
                print(error)
        return group_members

    # this actually send the command to the handler
    def create_thread(self, group_members):
        self.show_output = ""
        self.config_show_te_cmds_output.setText("")
        for device in group_members:
            device['data']['password'] = self.decrypt_password(
                device['data']['password'])
            device['data']['secret'] = self.decrypt_password(
                device['data']['secret'])

        with cf.ThreadPoolExecutor(max_workers=5) as ex:
            ex.map(self.create_show_handler, group_members)
        print(self.show_output)
        self.config_show_te_cmds_output.setText(self.show_output)

    def show_cmd_against_group(self, group_name):
        # run against device type groups
        group_members = list()
        if group_name == "router":
            all_device = self.convert_host_file_into_list()
            for device in all_device:
                if 'router' in device['groups']:
                    group_members.append(device)
            self.create_thread(group_members)
            return

        elif group_name == "switch":
            all_device = self.convert_host_file_into_list()
            for device in all_device:
                if 'switch' in device['groups']:
                    group_members.append(device)
            self.create_thread(group_members)
            return
        else:
            # This will only get the group members name
            custom_group_members = list()
            group_members = self.get_custom_group_members(group_name)
            all_devices = self.convert_host_file_into_list()
            for member in group_members:
                for device in all_devices:
                    if member == device['hostname']:
                        custom_group_members.append(device)
            self.create_thread(custom_group_members)
            return

    def show_cmd_against_device(self):
        pass
