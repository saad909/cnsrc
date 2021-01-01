from PyQt5.QtWidgets import *

class show_commands(QDialog):
    def run_show_command(self):
        # get the values from the combo_boxes
        device_name = device_group  = None

        device_selection = self.cb_bt_all_devices.isEnabled()

        # if group is selected
        if device_selection: 
            device_name = self.cb_bt_all_devices.currentText()
            command_index = self.cb_bt_all_commands.currentIndex()
            print('')
        # if single device is selected
        else:
            group_name = self.cb_bt_all_groups.currentText()
            command_index = self.cb_bt_all_commands.currentIndex()

        # if device_name and group_name:
        #     QMessageBox.information(self,"Note","Single device will be prefered")
        # # Only device is selected
        # elif device_name and not (group_name):
        #     pass
        

        # devices = read_yaml_file()
        # print(f"================= Total = {len(devices)} =================")
        # pprint(devices)

        # for device in devices:
        #     message = f"-------------------- {device['hostname']}--------------------\n"
        #     print(message)

        #     write_message(message)
        #     net_conn = create_handler(device['data'])
        #     if net_conn:
        #         output = net_conn.send_command("show ip int br",use_textfsm=True)
        #         write_to_file(output)

        #         print(f"ALL interfaces")
        #         print(f"Total Interfaces = {len(output)}")

        #         for interface in output:
        #             print(interface['intf'])


        #         print(f"ALL up interfaces are")

        #         up_count = 0
        #         for interface in output:
        #             if interface['status'] == 'up' and interface['proto'] == 'up':
        #                 print(interface['intf'])
        #                 up_count += 1

        #         print(f"Total up = {up_count}")


        #         print(f"ALL down interfaces are")

        #         down_count = 0
        #         for interface in output:
        #             if interface['status'] == 'down' or interface['proto'] == 'down':
        #                 print(interface['intf'])
        #                 down_count += 1

        #         print(f"Total down  = {down_count}")


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

