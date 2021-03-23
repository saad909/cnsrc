from PyQt5.QtWidgets import *


class update_combo_boxes(QDialog):
    # show commands
    def update_bt_all_devices(self):
        # getting all the devices
        all_devices_list = self.get_all_devices_hostname()
        all_devices_list.sort()
        all_devices_list.insert(0, "Select a Device")
        self.cb_bt_all_devices.addItem("")
        self.cb_bt_all_devices.clear()
        self.cb_bt_all_devices.addItems(all_devices_list)
