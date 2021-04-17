from PyQt5.QtWidgets import *
import os
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException


templates_path = os.path.join("hosts", "templates")
j2_env = Environment(
    loader=FileSystemLoader(templates_path), trim_blocks=True, autoescape=True,
)


class connection(QDialog):
    def create_show_handler(self, device):
        try:
            conn = ConnectHandler(**device['data'])
            self.run_show_commands(conn, device)
        except NetMikoTimeoutException:
            print(f"{device['hostname']}  in not reachable")
            self.statusBar().showMessage(
                f"{device['hostname']} in not reachable")
            # QMessageBox.information(
            #     self, "Note", f"{device['hostname']} in not reachable")
        except AuthenticationException:
            print("authentication failure")
            # QMessageBox.information(
            #     self, "Note", f"For {device['hostname']} authentication Failed"
            # )
            self.statusBar().setMessage(
                f"For {device['hostname']} authentication Failed")

        except SSHException:
            print("SSH error. Make sure ssh is enabled on device")
            self.statusBar().setMessage(
                f"SSH error. Make sure ssh is enabled on device[{'hostname'}]")
            # QMessageBox.information(
            #     self, "Note", f"SSH error. Make sure ssh is enabled on device[{'hostname'}]"
            # )
        except Exception as error:
            print(str(error))
            self.statusBar.showMessage(str(error))
            # QMessageBox.information(self, "Note", str(error))

    def run_show_commands(self, conn, host):
        conn.enable()
        output = f"\n\n--------------------{host['hostname']}--------------------\n\n"
        output += conn.send_command(self.command)
        # print(self.show_output)
        self.show_output += output
