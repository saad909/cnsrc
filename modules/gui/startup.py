###################### startup settings ######################
from re import sub
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import glob


class startup_settings(QDial):
    def startup(self):

        ###################### groups section ######################
        # show all groups in table on startup
        self.fill_groups_table(self.get_all_groups())

        # update all devices table
        self.clear_device_search_results()

        # load user saved settings
        self.load_settings()

        # update devices in show commands section
        self.update_bt_all_devices()

        # sort show commands combobox
        self.cb_bt_all_commands.model().sort(0)

        ###################### hide the tabs ######################
        # main tab
        self.tab_main.tabBar().setVisible(False)
        self.tab_basic_tasks.tabBar().setVisible(False)
        self.tab_devices.tabBar().setVisible(False)
        self.tab_groups.tabBar().setVisible(False)
        ###################### devices ######################

        ##### ALL Devices Table ######

        # set auto completion for search boxes
        self.auto_complete_search_results()

        # edit or delete device
        self.auto_complete_edit_results()

        # add devices for custom groups
        self.add_devices_for_group_selection()

        ###################### remove border ######################
        # self.remove_border(self.tab_main)
        # self.remove_border(self.tab_devices)
        # show commands submit button
