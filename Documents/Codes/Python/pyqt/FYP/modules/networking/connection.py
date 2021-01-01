from PyQt5.QtWidgets import *

import os
import yaml
from yaml import safe_load
from pprint import pprint

from jinja2 import Environment, FileSystemLoader
# from bracket_expansion import *
from netmiko import Netmiko, file_transfer,ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException


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
        except NetMikoAuthenticationException:
            print("authentication failure")
            QMessageBox.information(self,"Note",f"For {hostname} authentication Failed")
            return False
        except Exception as error:
            print("make sure ssh is enabled on device")
            QMessageBox.information(self,"Note",f"Make sure ssh is enabled on {hostname}")
            print(error)

            return False

    # def write_commad_output(command_output):
    #     with open('logs.txt', 'a') as filehandle:
    #             filehandle.writelines("%s\n" % line for line in command_output)

    # def write_message(message):
    #     with open("logs.txt",'a') as handler:
    #         handler.write(message)


    # generate the configuration template

    # 1. get the values from yaml file
    # 2. feed those valus to jinj2 template
    def gen(self,filename):

        print('-------------------')
        print('')
        var_file_path = os.path.join('hosts', 'vars', filename + '.yaml')
        with open(var_file_path) as _:
            var_file = safe_load(_)
            print(var_file)
            template = ENV.get_template(filename + ".j2")
            print(template.render(config=var_file))

    # use this template for those commands which dont require any arguments
    def gen_false(self,filename):
        filename = os.path.join('hosts', 'templates', filename + '.j2')
        # filename  = ENV.get_template(filename + '.j2')
        print(filename)
        with open(filename,'r') as handler:
            command = handler.read()
        print(command)
        return command

        
        

            




