import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from imports import *

ui, _ = loadUiType("main.ui")


class Window(
    QMainWindow,
    # Ui_main_window,
    ui,
    startup_settings,
    devices,
    devices_func,
    inventory_mgmt_func,
    user_settings,
    connection,
    update_combo_boxes,
    show_commands,
    basic_tasks,
):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Configuration Software for Cisco")
        self.setupUi(self)
        self.startup()

        self.handleUIChanges()
        self.handleButtons()

    ###################### handle UI changes  ######################

    def handleUIChanges(self):
        # get the valid ip
        self.get_valid_ip(self.d_add_ip_address)
        self.get_valid_ip(self.txt_d_all_ip_address)
        self.get_valid_ip(self.txt_d_edit_ip_address)
        self.get_valid_ip(self.d_edit_ip_address)

        # handle show commands combo boxes
        self.device_selection = None
        self.cb_bt_all_groups.currentIndexChanged.connect(
            lambda: self.disable_box(self.cb_bt_all_groups, self.cb_bt_all_devices)
        )
        self.cb_bt_all_devices.currentIndexChanged.connect(
            lambda: self.disable_box(self.cb_bt_all_devices, self.cb_bt_all_groups)
        )
        self.cb_bt_all_commands.currentIndexChanged.connect(
            self.show_commands_submit_button
        )

    ###################### handle buttons action ######################

    def handleButtons(self):

        ################### Tab movement #####################
        ##### add device ######

        self.pb_dev_all.clicked.connect(
            lambda: self.tab_movement(0, self.tab_devices, 0)
        )
        self.pb_dev_add.clicked.connect(
            lambda: self.tab_movement(0, self.tab_devices, 1)
        )
        self.pb_dev_edit.clicked.connect(
            lambda: self.tab_movement(0, self.tab_devices, 2)
        )

        ##### general tasks ######
        self.pb_bt_show_commands.clicked.connect(
            lambda: self.tab_movement(1, self.tab_basic_tasks, 0)
        )

        ################### button click action #####################
        ##### add device ######

        self.btn_d_add_save.clicked.connect(self.add_host)

        ##### all devices ######

        self.btn_d_all_search.clicked.connect(self.search_device)
        self.btn_d_all_clear.clicked.connect(self.clear_device_search_results)

        ##### edit or delete devices ######

        self.btn_d_edit_search.clicked.connect(self.edit_search_device)

        self.btn_d_edit_edit.clicked.connect(self.edit_device)
        self.btn_d_edit_delete.clicked.connect(self.delete_device)
        self.btn_d_edit_clear.clicked.connect(self.clear_edit_search_results)

        ##### show commands ######
        self.pb_bt_submit.clicked.connect(self.run_show_command)

        ##### basic tasks ######

        self.bt_set_vlan_submit.clicked.connect(self.create_vlan)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
