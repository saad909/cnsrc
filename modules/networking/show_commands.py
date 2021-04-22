from PyQt5.QtWidgets import *
import os, re
import threading
from queue import Queue


from pprint import pprint


class show_commands(QDialog):
    def fill_show_commands(self):
        # check whether group is selected or a device
        selection = "None"
        if self.cb_bt_all_devices.isEnabled():
            selection = "device"
            file_path = os.path.join("hosts", "show commands")
            device_name = str(self.cb_bt_all_devices.currentText())
            print(f"Device is selected is {device_name}")
            all_devices = self.convert_host_file_into_list()
            for device in all_devices:
                if device["hostname"] == device_name:
                    file_path = os.path.join(
                        file_path,
                        device["type"] + "_" + device["data"]["device_type"] + ".cfg",
                    )
                    break
        # check device type and os type and fill listbox with its own commands
        else:
            selection = "group"
            file_path = os.path.join("hosts", "show commands")
            group_name = str(self.cb_bt_all_groups.currentText())
            our_group = None
            all_groups = self.convert_group_file_into_list()
            for group in all_groups:
                if group["group_name"] == group_name:
                    our_group = group
                    break
            authentic_group = self.check_group_incompatibility(our_group)
            if not our_group["group_members"]:
                QMessageBox.information(self, "Warning", "Group has no group members")
                self.show_commands_list.clear()
                return
            elif not authentic_group:
                QMessageBox.information(
                    self, "Warning", "Group has incomptaible members"
                )
                self.show_commands_list.clear()
                return
            print(f"Group is selected is {group_name}")
            all_groups = self.get_all_groups()
            group_member = None
            for group in all_groups:
                if group["group_name"] == group_name:
                    group_member = group
            all_devices = self.convert_host_file_into_list()
            try:
                # if all devices are router or switch, the for groups show the commands
                # of that device_type and deivce_os
                # i.e if all devices in group are swith and ios. then show switch ios commands
                type = self.check_all_group_members_type(group_member)
                if type:
                    member = group_member["group_members"][0]
                    for device in all_devices:
                        if device["hostname"] == member:
                            file_path = os.path.join(
                                file_path,
                                f"{type[1]}_{device['data']['device_type']}.cfg",
                            )
                            break

                elif group_member["group_members"]:
                    member = group_member["group_members"][0]
                    for device in all_devices:
                        if device["hostname"] == member:
                            file_path = os.path.join(
                                file_path,
                                f"Group_{device['data']['device_type']}.cfg",
                            )
                            break

                else:
                    QMessageBox.information(self, "Warning", "Group has no members")
                    self.show_commands_list.clear()
                    return
            except Exception as error:
                QMessageBox.information(self, "Warning", str(error))
                self.show_commands_list.clear()
                return
        print(f"config file = {file_path}")
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r") as handler:
                    commands = handler.read()
                    # fill commands against single device
                    self.show_commands_list.clear()
                    self.show_commands_list.addItems(commands.splitlines())
                    return
            except Exception as error:
                QMessageBox.information(self, "Warning", str(error))
                self.show_commands_list.clear()
                return
        else:
            open(file_path, "a").close()
            QMessageBox.information(self, "Warning", "Config is empty")
            self.show_commands_list.clear()
            return

    def update_show_commands_groups_combobox(self):
        self.cb_bt_all_groups.clear()
        self.cb_bt_all_groups.addItems(["Select a group"] + self.get_all_groups_names())

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
            self.fill_show_commands()

        # command seelection

    def show_commands_submit_button(self):

        if self.device_selection and self.show_commands_list.selectedItems():
            self.config_show_btn_submit.setEnabled(True)
        else:
            self.config_show_btn_submit.setEnabled(False)

            # | | ___   __ _(_) ___
            # | |/ _ \ / _` | |/ __|
            # | | (_) | (_| | | (__
            # |_|\___/ \__, |_|\___|
            #         |___/

    def get_command(self, command_text):
        file_name = os.path.join("hosts", "show commands", command_text + ".cfg")
        with open(file_name, "r") as handler:
            command = handler.read()
        return command

    def run_show_command(self):
        device_name = None
        self.statusBar().showMessage("")
        device_selection = self.cb_bt_all_devices.isEnabled()

        # if single device is selected
        if device_selection:
            device_name = self.cb_bt_all_devices.currentText()
            self.show_cmd_against_device(device_name)

        # if group is selected
        else:
            group_name = self.cb_bt_all_groups.currentText()
            # print(command)
            self.show_cmd_against_group(group_name)

    def get_custom_group_members(self, group_name):
        all_groups = self.get_all_groups()
        group_members = None
        for group in all_groups:
            try:
                if group["group_name"] == group_name:
                    group_members = group["group_members"]
            except Exception as error:
                print(error)
        return group_members

    # this actually send the command to the handler
    def create_thread(self, devices, cmds):
        self.show_output = ""
        self.config_show_te_cmds_output.setText("")
        for device in devices:
            device["data"]["password"] = self.decrypt_password(
                device["data"]["password"]
            )
            device["data"]["secret"] = self.decrypt_password(device["data"]["secret"])

        with cf.ThreadPoolExecutor(max_workers=5) as ex:
            ex.map(self.create_show_handler, devices, cmds)

    def show_cmd_against_group(self, group_name):
        group_members = list()
        custom_group_members = list()
        group_members = self.get_custom_group_members(group_name)
        all_devices = self.convert_host_file_into_list()
        for member in group_members:
            for device in all_devices:
                if member == device["hostname"]:
                    custom_group_members.append(device)
        all_commands = list()
        for command in self.show_commands_list.selectedItems():
            all_commands.append(command.text())
        print("commands are")
        print(str(all_commands))
        self.create_thread(custom_group_members, all_commands)
        print(self.show_output)
        return

    def show_cmd_against_device(self, device_name):
        device_name = self.cb_bt_all_devices.currentText()
        # get device
        my_device = None
        all_devices = self.convert_host_file_into_list()
        for device in all_devices:
            if device["hostname"] == device_name:
                my_device = device
                break

        show_ouput_dictionary = {"hostname": "", "commands": [], "error": ""}
        all_commands = list()
        for command in self.show_commands_list.selectedItems():
            all_commands.append(command.text())

        output_q = Queue()
        # decrypt_passwords
        my_device["data"]["password"] = self.decrypt_password(
            my_device["data"]["password"]
        )
        my_device["data"]["secret"] = self.decrypt_password(my_device["data"]["secret"])
        for command in all_commands:
            my_thread = threading.Thread(
                target=self.create_show_handler,
                args=(my_device, command, show_ouput_dictionary, output_q),
            )
            my_thread.start()

        # Wait for all threads to complete
        main_thread = threading.currentThread()
        for some_thread in threading.enumerate():
            if some_thread != main_thread:
                some_thread.join()

        # for thread in threading.enumerate():
        #     if thread != main_thread:
        #         thread.kill()

        output = ""
        errors = ""
        regex = r"""
            (^(\(|'|\('))|((\)|'|\)')$)
        """
        while not output_q.empty():
            my_dict = output_q.get()
            output += "".join(my_dict["commands"])
            errors += "".join(my_dict["error"])
        output = re.sub(regex, "", output)
        errors = re.sub(regex, "", errors)

        print(output)
        print(errors)
        self.config_show_te_cmds_output.clear()
        self.config_show_te_cmds_output.setText(output)
        return
