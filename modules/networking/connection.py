from PyQt5.QtWidgets import *
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
from jinja2 import Environment, FileSystemLoader
from PyQt5.QtCore import QObject, pyqtSignal
from pyfiglet import Figlet


class Connection(
    QObject,
):

    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)
    output_signal = pyqtSignal(str)

    def __init__(self, device, all_commands):
        self.device = device
        self.all_commands = all_commands
        super().__init__()

    def run(self):
        if int(self.device["data"]["port"]) > 65535:
            self.error_signal.emit(f"{self.device['hostname']} has invalid port number")
            self.finished_signal.emit()
            return
        try:
            f = Figlet(font="slant")
            for command in self.all_commands:
                self.output_signal.emit("\n" * 2 + f.renderText(command) + "\n" * 2)
                conn = ConnectHandler(**self.device["data"])
                conn.enable()
                output = conn.send_command(command)
                conn.disconnect()
                self.output_signal.emit(output)
            self.finished_signal.emit()
        except Exception as error:
            print(error)
            self.error_signal.emit(str(error))
            self.finished_signal.emit()

    # def create_show_handler(self, device, command):
    #     try:
    #         if int(device["data"]["port"]) > 65535:
    #             self.statusBar().showMessage(
    #                 f"{device['hostname']} has invalid port number"
    #             )
    #             QMessageBox.information(
    #                 self, "Warning", f"{device['hostname']} has invalid port number"
    #             )
    #             print(f"{device['hostname']} has invalid port number")
    #             QMessageBox.information(
    #                 self, "Warning", f"{device['hostname']} has invalid port number"
    #             )
    #             return

    #         conn = ConnectHandler(**device["data"])
    #         output = conn.send_command(command)
    #         conn.disconnect()
    #         return output
    #     except NetMikoTimeoutException:
    #         print(f"{device['hostname']}  in not reachable")
    #         self.statusBar().showMessage(f"{device['hostname']} in not reachable")
    #         QMessageBox.information(
    #             self, "Warning", f"{device['hostname']} in not reachable"
    #         )
    #         return

    #     except AuthenticationException:
    #         print("authentication failure")
    #         self.statusBar().setMessage(
    #             f"For {device['hostname']} authentication Failed"
    #         )
    #         QMessageBox.information(
    #             self, "Warning", f"For {device['hostname']} authentication Failed"
    #         )
    #         return

    #     except SSHException:
    #         print("SSH error. Make sure ssh is enabled on device")
    #         self.statusBar().setMessage(
    #             f"SSH error. Make sure ssh is enabled on device[{'hostname'}]"
    #         )
    #         return
    #     except Exception as error:
    #         print(str(error))
    #         self.statusBar.showMessage(str(error))
    #         QMessageBox.information(self, "Warning", str(error))
    #         return

    def send_mon_int_configs(self, device, interface_name, command_file):
        try:
            # print(device)
            # print(interface_name)
            # print(command_file)
            config_dictionary = {"intf_name": interface_name}
            j2_env = Environment(
                loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
            )
            template = j2_env.get_template(command_file)
            configuration = template.render(data=config_dictionary)
            print(configuration)
            conn = ConnectHandler(**device["data"])
            conn.enable()
            output = conn.send_config_set(configuration.split("\n"))
            print(output)
        except Exception as error:
            QMessageBox.critical(self, "Warning", str(error))
