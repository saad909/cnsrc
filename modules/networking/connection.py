from PyQt5.QtWidgets import *

import os
import yaml
from yaml import safe_load
from pprint import pprint

from jinja2 import Environment, FileSystemLoader
# from bracket_expansion import *
from netmiko import Netmiko, file_transfer,ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException


templates_path = os.path.join('hosts','templates')
ENV = Environment(loader=FileSystemLoader(templates_path))


class connection(QDialog):

    # craete the connection handler and return
    def create_handler(self,device):
        hostname = device['hostname']
        device = device['data']
        try:
            net_conn =  ConnectHandler(**device)
            return net_conn
        except NetMikoTimeoutException:
            print("devices in not reachable")
            QMessageBox.information(self,"Note",f"{hostname} in not reachable")
            return False
        except AuthenticationException:
            print("authentication failure")
            QMessageBox.information(self,"Note",f"For {hostname} authentication Failed")
            return False

        except SSHException:
            print("SSH error. Make sure ssh is enabled on device")
            QMessageBox.information(self,"Note",f"SSH error. Make sure ssh is enabled on {hostname}")
            print(str(error))
        except Exception as error:
            print(str(error))
            QMessageBox.information(self,"Note",str(error))
            return False



    # generate the configuration template

    # 1. get the values from yaml file
    # 2. feed those valus to jinj2 template
    def gen(self,configs_dictionary, filename):
        template_path = os.path.join(filename + '.j2')
        template = ENV.get_template(template_path)
        return template.render(config=configs_dictionary)



    # use this template for those commands which dont require any arguments
    def gen_false(self,filename):
        filename = os.path.join('hosts', 'templates', filename + '.j2')
        # filename  = ENV.get_template(filename + '.j2')
        print(filename)
        with open(filename,'r') as handler:
            command = handler.read()
        print(command)
        return command
