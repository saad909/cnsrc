from PyQt5.QtWidgets import *


class update_combo_boxes(QDialog):
    # show commands
    def update_bt_all_devices(self):
        # getting all the devices
        all_devices_list = self.get_all_devices_hostname()
        all_devices_list.sort()
        all_devices_list.insert(0, "Select a Device")
        self.cb_bt_all_devices.clear()
        self.cb_bt_all_devices.addItems(all_devices_list)
        return

    def update_show_commands_groups_combobox(self):
        self.cb_bt_all_groups.clear()
        if self.get_all_groups()[0] == "dummy":
            return
        self.cb_bt_all_groups.addItems(["Select a group"] + self.get_all_groups_names())

    def update_mon_all_devices(self):
        # getting all the devices
        all_devices_list = self.get_all_devices_hostname()
        all_devices_list.sort()
        all_devices_list.insert(0, "Select a Device")
        self.mon_int_cb_all_devices.clear()
        self.mon_int_cb_all_devices.addItems(all_devices_list)
        return

    def update_mgmt_config_all_devices(self):
        # getting all the devices
        all_devices_list = self.get_all_devices_hostname()
        all_devices_list.sort()
        all_devices_list.insert(0, "Select a Device")
        self.mgmt_config_all_devices.clear()
        self.mgmt_config_all_devices.addItems(all_devices_list)
        return

    def update_mgmt_os_all_devices(self):
        # getting all the devices
        all_devices_list = self.get_all_devices_hostname()
        all_devices_list.sort()
        all_devices_list.insert(0, "Select a Device")
        self.mgmt_os_all_devices.clear()
        self.mgmt_os_all_devices.addItems(all_devices_list)
        return

    def update_configs_all_devices(self):
        # getting all the devices
        all_devices_list = self.get_all_devices_hostname()
        all_devices_list.sort()
        self.configs_all_devices.clear()
        all_devices_list.insert(0, "Select a Device")
        self.configs_all_devices.addItems(all_devices_list)
        return

    # def update_dhcp_client_all_devices(self):
    #     # getting all the devices
    #     all_devices_list = self.get_all_devices_hostname()
    #     all_devices_list.sort()
    #     self.dhcp_client_all_devices.clear()
    #     all_devices_list.insert(0, "Select a Device")
    #     self.dhcp_client_all_devices.addItems(all_devices_list)
    #     return

    def update_remote_devices(self):
        # getting all the devices
        all_devices_list = self.get_all_routers()
        all_devices_hostname = list()
        local_device_name = self.configs_all_devices.currentText()
        print("Local device name is")
        print(local_device_name)
        for device in all_devices_list:
            if device['hostname'] == local_device_name:
                continue
            else:
                all_devices_hostname.append(device['hostname'])

        all_devices_hostname.sort()
        self.ppp_remote_all_devices.clear()
        self.ppp_remote_all_devices.addItems(all_devices_hostname)
        return
