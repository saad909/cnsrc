from PyQt5.QtWidgets import *
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException


class connection(QDialog):
    def create_show_handler(self, device, command):
        try:
            if int(device["data"]["port"]) > 65535:
                self.statusBar().showMessage(
                    f"{device['hostname']} has invalid port number"
                )
                QMessageBox.information(
                    self, "Warning", f"{device['hostname']} has invalid port number"
                )
                print(f"{device['hostname']} has invalid port number")
                QMessageBox.information(
                    self, "Warning", f"{device['hostname']} has invalid port number"
                )
                return

            conn = ConnectHandler(**device["data"])
            output = conn.send_command(command)
            return output
        except NetMikoTimeoutException:
            print(f"{device['hostname']}  in not reachable")
            self.statusBar().showMessage(f"{device['hostname']} in not reachable")
            QMessageBox.information(
                self, "Warning", f"{device['hostname']} in not reachable"
            )
            return

        except AuthenticationException:
            print("authentication failure")
            self.statusBar().setMessage(
                f"For {device['hostname']} authentication Failed"
            )
            QMessageBox.information(
                self, "Warning", f"For {device['hostname']} authentication Failed"
            )
            return

        except SSHException:
            print("SSH error. Make sure ssh is enabled on device")
            self.statusBar().setMessage(
                f"SSH error. Make sure ssh is enabled on device[{'hostname'}]"
            )
            return
        except Exception as error:
            print(str(error))
            self.statusBar.showMessage(str(error))
            QMessageBox.information(self, "Warning", str(error))
            return
