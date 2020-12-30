from PyQt5.QtWidgets import *
from pprint import pprint
from netmiko import ConnectHandler
class connection(QDialog):

    # craete the connection handler and return
    def create_connection_handler(self,device):
        device_data = device['data']
        return ConnectHandler(**devices_data)

    def update_combo_boxes(self,box):
        devices = self.get_all_devices_hostname()
        box.addItems(devices)

