from PyQt5.QtWidgets import *
import os
import re
import time
from pprint import pprint
from modules.networking.connection import ConnectionWithThreading
from PyQt5.QtCore import QThread, Qt, QRegExp
import functools


class monitoring:
    all_interfaces = list()
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
        my_device["data"]["secret"] = self.decrypt_password(
            my_device["data"]["secret"])
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
            print("state changed")
            self.get_all_interfaces(self.mon_int_cb_all_devices.currentText(), self.mon_int_cb_all_interface)
            all_interfaces = self.all_interfaces
            if all_interfaces:


                state = ""
                interface = None
                for intf in all_interfaces:
                    if intf["intf_name"] == interface_name:
                        interface = intf
                        break

                print(interface_name)
                print(
                    f"inteface state is {interface['status']} and {interface['protocol']}"
                )
                if interface["status"] == "up" and interface["protocol"] == "up":
                    self.mon_int_rb_up.setChecked(True)
                else:
                    self.mon_int_rb_down.setChecked(True)

                print(self.mon_int_cb_all_interface.currentText())
            if self.mon_int_rb_up.isChecked() or self.mon_int_rb_down.isChecked():
                self.mon_int_btn_toggle.setEnabled(True)

            print("Goes here")
            index = self.mon_int_cb_all_interface.findText(interface_name)
            print(index)
            self.mon_int_cb_all_interface.setCurrentIndex(int( index ))
            return
        except Exception as error:
            QMessageBox.critical(self, "Warning", str(error))
            return


    def filter_interfaces_name(self, my_box, output):
        if output:
            interfaces = list()
            for line in output.splitlines():
                regex = re.compile(
                    r"(?P<interface_name>^(G|E|F|V|L)[\w\/]+)\s+(?P<ip_address>([\d.]+)|unassigned)\s+YES.*?(?P<status>(up|down))\s+(?P<protocol>(up|down)).*"
                )
                result = regex.fullmatch(line)
                if result:
                    # print(result.group("interface_name"))
                    interfaces.append(
                        
                        {
                            "intf_name": result.group("interface_name"),
                            'ip_address':result.group("ip_address"),
                            'status':result.group("status"),
                            'protocol':result.group("protocol"),

                        }

                    )
            # print(interfaces)
            self.all_interfaces = list()
            if interfaces:
                print("test 1")
                my_box.clear()
                for intf in interfaces:
                    my_box.addItem(intf['intf_name'])
                self.all_interfaces = interfaces
            else:
                return False

    def get_all_interfaces(self, device_name, my_box):
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
            print(my_device)
            file_path = os.path.join(
                "hosts",
                "monitor",
                my_device["data"]["device_type"] + "_" + "get_interfaces.cfg",
            )
            try:
                with open(file_path, "r") as handler:
                    command = handler.read()
                all_commands = command.splitlines()

                # getting output
                self.thread = QThread()
                # Step 3: Create a worker object
                self.worker = ConnectionWithThreading(my_device, all_commands)
                # Step 4: Move worker to the thread
                self.worker.moveToThread(self.thread)
                # Step 5: Connect signals and slots
                self.thread.started.connect(self.worker.run)
                self.worker.finished_signal.connect(self.thread.quit)
                self.worker.finished_signal.connect(self.worker.deleteLater)
                self.worker.error_signal.connect(self.show_errors)
                # rps -> routing protocols
                self.worker.output_signal.connect(
                    functools.partial(self.filter_interfaces_name, my_box))
                # Step 6: Start the thread
                self.thread.start()
                time.sleep(3)

                # output = self.create_show_handler(my_device, command)

                # ip_address = result.group("ip_address")

            except Exception as error:
                QMessageBox.critical(self, "Warning", str(error))
        else:
            print("test 2")
            self.mon_int_cb_all_interface.clear()
            self.mon_int_btn_toggle.setEnabled(False)

            # also clear the radio buttons
