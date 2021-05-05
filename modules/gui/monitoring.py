from PyQt5.QtWidgets import *
import os, re
from pprint import pprint


class monitoring:
    def check_interface_toggle_state(self):
        self.mon_int_cb_all_interface.count()
        if count and (
            self.mon_int_rb_up.isChecked() or self.mon_int_rb_down.isChecked()
        ):
            self.mon_int_btn_toggle.setEnabled(True)

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
                pprint(interfaces)
                # ip_address = result.group("ip_address")

            except Exception as error:
                QMessageBox.critical(self, "Warning", str(error))
        else:
            self.mon_int_cb_all_interface.clear()
            self.mon_int_btn_toggle.setEnabled(False)

            # also clear the radio buttons
