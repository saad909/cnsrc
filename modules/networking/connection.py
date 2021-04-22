from PyQt5.QtWidgets import *
import os
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
from jinja2 import Environment, FileSystemLoader


templates_path = os.path.join("hosts", "templates")
j2_env = Environment(
    loader=FileSystemLoader(templates_path),
    trim_blocks=True,
    autoescape=True,
)


class connection(QDialog):
    def create_show_handler(self, device, command, show_output_dictionary, output_q):
        try:
            show_output_dictionary["hostname"] = device["hostname"]
            if int(device["data"]["port"]) > 65535:
                self.statusBar().showMessage(
                    f"{device['hostname']} has invalid port number"
                )
                show_output_dictionary[
                    "error"
                ] = f"{device['hostname']} has invalid port number"
                return

            output_dict = {}
            conn = ConnectHandler(**device["data"])
            output = conn.send_command(command)
            show_output_dictionary["commands"].append(output)
            output_q.put(show_output_dictionary)
        except NetMikoTimeoutException:
            print(f"{device['hostname']}  in not reachable")
            self.statusBar().showMessage(f"{device['hostname']} in not reachable")
            show_output_dictionary["error"] = f"{device['hostname']} in not reachable"
            output_q.put(show_output_dictionary)

        except AuthenticationException:
            print("authentication failure")
            self.statusBar().setMessage(
                f"For {device['hostname']} authentication Failed"
            )
            show_output_dictionary[
                "error"
            ] = f"For {device['hostname']} authentication Failed"
            output_q.put(show_output_dictionary)

        except SSHException:
            print("SSH error. Make sure ssh is enabled on device")
            self.statusBar().setMessage(
                f"SSH error. Make sure ssh is enabled on device[{'hostname'}]"
            )
            show_output_dictionary[
                "error"
            ] = f"SSH error. Make sure ssh is enabled on device[{'hostname'}]"
            output_q.put(show_output_dictionary)
        except Exception as error:
            print(str(error))
            self.statusBar.showMessage(str(error))
            show_output_dictionary["error"] = str(error)
            output_q.put(show_output_dictionary)
