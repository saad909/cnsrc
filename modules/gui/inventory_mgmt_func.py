from PyQt5.QtWidgets import QDialog, QMessageBox
from netmiko import ConnectHandler
from yaml import safe_load
import yaml
from pprint import pprint
import os


class inventory_mgmt_func(QDialog):

    # check hostfile
    # 1. check whether the hosts dir exists
    # 1a. if does not  exists create it
    # 2. if exist: check for invtory file
    # 2a. if inventory file exists -> return True
    # 2b. else create an empty file
    def check_for_host_file(self):
        # check the directory
        dir_exists = os.path.isdir("hosts")
        if dir_exists:
            print("Folder exists")
        else:
            os.mkdir("hosts")
            # creating a dummy file
            hostname = ip_address = username = password = secret = "dummy"
            port_number = "22"
            device_type = ""
            os_type = ""
            device = self.create_dictionary(
                hostname,
                ip_address,
                username,
                password,
                secret,
                device_type,
                port_number,
                os_type,
            )
            devices_list = list()
            devices_list.append(device)
            host_file = self.get_host_file_path()
            f = open(host_file, "w+")
            yaml.dump(devices_list, f, allow_unicode=True)
            return False

        # check for file existance
        host_file = self.get_host_file_path()
        file_exists = os.path.isfile(host_file)
        if not file_exists:

            # creating a dummy file
            hostname = ip_address = username = password = secret = "dummy"
            port_number = "22"
            device_type = ""
            os_type = ""
            device = self.create_dictionary(
                hostname,
                ip_address,
                username,
                password,
                secret,
                device_type,
                port_number,
                os_type,
            )
            devices_list = list()
            devices_list.append(device)
            f = open(host_file, "w+")
            yaml.dump(devices_list, f, allow_unicode=True)
            return False

        # file exists
        else:
            return True

    # read the yaml file and returns a list
    def read_yaml_file(self, yaml_file):
        devices = None
        with open(yaml_file, "r") as handler:
            devices = safe_load(handler)
        return devices

    # read the yaml file and returns a list
    def convert_host_file_into_list(self):
        host_file = self.get_host_file_path()
        devices = None
        with open(host_file, "r") as handler:
            devices = safe_load(handler)
        return devices

    # input = device parameters
    # output = dictionary created from those parameter
    # output['data'] -> contains the information for actual connection
    def create_dictionary(
        self,
        hostname,
        ip_address,
        username,
        password,
        secret,
        device_type,
        port_number,
        os_type,
    ):

        return {
            "hostname": hostname,
            "data": {
                "device_type": os_type,
                "host": ip_address,
                "username": username,
                "password": password,
                "secret": secret,
                "port": port_number,
            },
            "type": device_type,
            "groups": [],
        }

    # get os independent inventory file path
    def get_host_file_path(self):
        return os.path.join("hosts", "inventory.yaml")

    # 1. check for duplication of hostname in the database
    # 2.return True in case of duplication -> True,False
    # 3. True -> duplication occurs
    def check_hostname_duplication(self, all_hosts, host):
        for device in all_hosts:
            if device["hostname"] == host["hostname"]:
                print("Host name duplication occured")
                QMessageBox.information(
                    self,
                    "Waring",
                    f"{host['hostname']}: {device['data']['host']} also has the same hostname",
                )
                # QMessageBox.information(
                #     self, "Warning", "Host name duplication occured"
                # )

                self.d_add_hostname.setFocus()
                self.highlight_border(self.d_add_hostname)
                return True
        self.highlight_border_false(self.d_add_hostname)
        return False

    # 1. check for duplication of ip address in the database
    # 2.return True in case of duplication -> True,False
    # 3. True -> duplication occurs
    def check_ip_duplication(
        self, all_hosts, host
    ):  # return True in case of duplication
        for device in all_hosts:
            if device["data"]["host"] == host["data"]["host"]:
                print(f"{device['hostname']} has the same ip address")
                # QMessageBox.information(
                #     self, "Warning", f"{device['hostname']} has the same ip address "
                # )
                QMessageBox.information(
                    self,
                    "Waring",
                    f"{host['hostname']}: {device['hostname']} already has been assigned the ip address {device['data']['host']}",
                )
                self.d_add_ip_address.setFocus()
                self.highlight_border(self.d_add_ip_address)
                return True

        self.highlight_border_false(self.d_add_ip_address)
        return False

    # write devices to the inventory file
    # takes a list as input
    def write_inventory(self, all_devices_list):
        host_file = self.get_host_file_path()
        f = open(host_file, "w+")
        yaml.dump(all_devices_list, f, allow_unicode=True)

    # how the device is added
    def add_host_into_inventory(self, device):
        # checking for empty inventory
        host_file_not_empty = self.check_for_host_file()
        all_devices_list = None
        #  Database is not empty
        if host_file_not_empty:

            # getting all devices
            all_devices_list = self.convert_host_file_into_list()

            # check  whether it contains the dummy device

            # remove the dummy file
            if len(all_devices_list) == 1:
                if all_devices_list[0]["hostname"] == "dummy":
                    all_devices_list.pop(0)

            # check whether the ip address exists before
            hostname_duplication = self.check_hostname_duplication(
                all_devices_list, device
            )
            if hostname_duplication:
                return False
            # check whether the ip address exists before
            ip_duplication = self.check_ip_duplication(all_devices_list, device)
            if ip_duplication:
                return False

            print("=================== Already Present Devices ==================")
            pprint(all_devices_list)

            # get the hosts from the user and create its dictionary
            all_devices_list.append(device)

            print(
                "-----------------------ALL Devices in host file --------------------------------"
            )

            pprint(all_devices_list)

            # adding the device to the group based on its type
            groupname = device["type"]
            device["groups"].append(groupname)

            self.write_inventory(all_devices_list)
            return True
