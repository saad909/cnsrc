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
