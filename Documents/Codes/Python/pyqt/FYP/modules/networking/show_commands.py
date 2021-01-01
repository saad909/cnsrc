from PyQt5.QtWidgets import *
import os
from pprint import pprint

class show_commands(QDialog):
    def run_show_command(self):
        # get the values from the combo_boxes
        device_name = device_group  = None

        device_selection = self.cb_bt_all_devices.isEnabled()

        # if group is selected
        if device_selection: 
            device_name = self.cb_bt_all_devices.currentText()
            command_text= self.cb_bt_all_commands.currentText()
            self.execute_show_command_against_single_device(device_name,command_text)

        # if single device is selected
        else:

            group_name = self.cb_bt_all_groups.currentText()
            command_text = self.cb_bt_all_commands.currentText()
            self.execute_show_command_against_group(group_name,command_text)




    def get_device(self,hostname):
        devices = self.convert_host_file_into_list()
        for device in devices:
            if device['hostname'] == hostname:
                return device

    # execute show command agianst a single device
    def execute_show_command(self,net_conn,filename):
        filename = os.path.join('show',filename)
        command = self.gen_false(filename)
        output = net_conn.send_command(command)
        print(output)
        self.te_bt_command_output.setPlainText(str(output))


    def execute_show_command_against_single_device(self, device_name,command_text):
        print(f"Device name is {device_name}")
        print(f"command to execute is {command_text}")

        device = self.get_device(device_name)
        net_conn = self.create_handler(device)

        self.te_bt_command_output.clear()
        if net_conn:
            # show clock
            if command_text == "clock":
                self.execute_show_command(net_conn,'show_clock')
                return

            #show startup config
            elif command_text == "startup config":
                self.execute_show_command(net_conn,'show_start')
                return

            #show running config
            elif command_text == "running config":
                self.execute_show_command(net_conn,'show_run')
                return
            # sh interfaces information
            elif command_text == "all interfaces configurations":
                self.execute_show_command(net_conn,'show_interface_brief')
                return
            
        






    # execute show command agianst a group
    def execute_show_command_against_group(self, group_name, command_text):
        print(f"Group name is {group_name}")
        print(f"command to execute is {command_text}")
        group_devices = list()
        all_devices = self.convert_host_file_into_list()

        for device in all_devices:
            if group_name in device['groups']:
                group_devices.append(device)
        pprint(group_devices)
        print(f"total devices = {len(group_devices)}")


        self.te_bt_command_output.clear()
        for device in group_devices:
            net_conn = self.create_handler(device)
            if net_conn:
                print(f"\n================== {device['hostname']} ==================\n")
                self.te_bt_command_output.setPlainText(f"\n================== {device['hostname']} ==================\n")
                # show clock
                if command_text == "clock":
                    self.execute_show_command(net_conn,'show_clock')

                #show startup config
                elif command_text == "startup config":
                    print("Startup config")
                    self.execute_show_command(net_conn,'show_start')

                #show running config
                elif command_text == "running config":
                    print("Running config")
                    self.execute_show_command(net_conn,'show_run')
                # sh interfaces information
                elif command_text == "all interfaces configurations":
                    self.execute_show_command(net_conn,'show_interface_brief')

                elif command_text == "version":
                    self.execute_show_command(net_conn,'show_version')


    def disable_box(self,checking_box,box_to_disable): 


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
            self.pb_bt_submit.setEnabled(True)
        else:
            self.pb_bt_submit.setEnabled(False)

