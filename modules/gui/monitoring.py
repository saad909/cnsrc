from PyQt5.QtWidgets import *
import os, re
from pprint import pprint


class monitoring:
    def toggle_interface_state(self):
        # try:
        interface_name = self.mon_int_cb_all_interface.currentText()
        device_name = self.mon_int_cb_all_devices.currentText()
        all_devices = self.convert_host_file_into_list()
        my_device = None
        for device in all_devices:
            if device["hostname"] == device_name:
                my_device = device
                break
        my_device["data"]["password"] = self.decrypt_password(
            my_device["data"]["password"]
        )
        my_device["data"]["secret"] = self.decrypt_password(my_device["data"]["secret"])
        command_file = ""
        if self.mon_int_rb_up.isChecked():
            command_file = os.path.join(
                "hosts",
                "monitor",
                my_device["data"]["device_type"] + "_int_shutdown.j2",
            )
        else:
            command_file = os.path.join(
                "hosts",
                "monitor",
                my_device["data"]["device_type"] + "_int_noshut.j2",
            )

        if command_file:
            self.send_mon_int_configs(my_device, interface_name, command_file)

        # except Exception as error:
        #     QMessageBox.critical(self, "Warning", str(error))

    def check_interface_toggle_state(self, interface_name):
        try:
            count = self.mon_int_cb_all_interface.count()
            if count:
                all_interfaces = self.get_all_interfaces(
                    self.mon_int_cb_all_devices.currentText()
                )
                index = self.mon_int_cb_all_interface.findText(interface_name)
                print(index)
                self.mon_int_cb_all_interface.setCurrentIndex(index)
                state = ""
                interface = None
                for intf in all_interfaces:
                    if intf["name"] == interface_name:
                        interface = intf
                        break

                print(interface)
                print(
                    f"inteface state is {interface['status']} and {interface['protocol']}"
                )
                if interface["status"] == "up" and interface["protocol"] == "up":
                    self.mon_int_rb_up.setChecked(True)
                else:
                    self.mon_int_rb_down.setChecked(True)
            if count and (
                self.mon_int_rb_up.isChecked() or self.mon_int_rb_down.isChecked()
            ):
                self.mon_int_btn_toggle.setEnabled(True)
                return
        except Exception as error:
            QMessageBox.critical(self, "Warning", str(error))
            return

    def get_all_interfaces(self, device_name):
        if device_name != "Select a Device":
            all_devices = self.convert_host_file_into_list()
            my_device = None
            for device in all_devices:
                if device["hostname"] == device_name:
                    my_device = device
                    break
            my_device["data"]["password"] = self.decrypt_password(
                my_device["data"]["password"]
            )
            my_device["data"]["secret"] = self.decrypt_password(
                my_device["data"]["secret"]
            )
            file_path = os.path.join(
                "hosts",
                "monitor",
                my_device["data"]["device_type"] + "_" + "get_interfaces.cfg",
            )
            try:
                with open(file_path, "r") as handler:
                    command = handler.read()
                output = self.create_show_handler(my_device, command)
                interfaces = list()
                for line in output.splitlines():
                    regex = re.compile(
                        r"(?P<interface_name>^(G|E|F|V|L)[\w\/]+)\s+(?P<ip_address>([\d\.]+)|unassigned)(\s+\w+){2}\s+(?P<status>up|down|administratively down)\s+(?P<protocol>up|down|administratively down)\s*"
                    )
                    result = regex.fullmatch(line)
                    if result:
                        intf = {
                            "name": result.group("interface_name"),
                            "ip_address": result.group("ip_address"),
                            "status": result.group("status"),
                            "protocol": result.group("protocol"),
                        }
                        interfaces.append(intf)
                self.mon_int_cb_all_interface.clear()
                for intf in interfaces:
                    self.mon_int_cb_all_interface.addItem(intf["name"])

                return interfaces

                # ip_address = result.group("ip_address")

            except Exception as error:
                QMessageBox.critical(self, "Warning", str(error))
        else:
            self.mon_int_cb_all_interface.clear()
            self.mon_int_btn_toggle.setEnabled(False)

            # also clear the radio buttons
