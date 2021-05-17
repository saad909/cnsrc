###################### startup settings ######################
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os


class startup_settings(QDial):
    def startup(self):

        ###################### groups section ######################
        # add devices for custom groups
        self.check_for_group_file()
        self.check_for_host_file()
        self.add_devices_for_group_selection()
        # show all groups in table on startup
        if os.path.isfile(self.get_group_file_path()):
            self.fill_groups_table(self.get_all_groups())
        # autocomplete for all groups and edits groups section
        self.auto_complete_group_search_results()
        self.auto_complete_group_edit_search_results()

        # update all devices table
        self.check_for_host_file()
        self.clear_device_search_results()

        # load user saved settings
        self.load_settings()

        # update devices in show commands section
        self.update_bt_all_devices()

        # sort show commands combobox
        # sort show groups combobox
        self.cb_bt_all_groups.model().sort(0)
        # all group to groups combobox in basic task section - show commands
        self.update_show_commands_groups_combobox()

        ###################### hide the tabs ######################
        # main tab
        self.tab_main.tabBar().setVisible(False)
        self.tab_basic_tasks.tabBar().setVisible(False)
        self.tab_devices.tabBar().setVisible(False)
        self.tab_groups.tabBar().setVisible(False)
        self.tab_users.tabBar().setVisible(False)
        self.tab_configs.tabBar().setVisible(False)
        ###################### devices ######################

        ##### ALL Devices Table ######

        # set auto completion for search boxes
        self.auto_complete_search_results()

        # edit or delete device
        self.auto_complete_edit_results()

        ######## users section #############
        self.db_connection()
        self.fill_all_users_table(self.get_all_users())
        self.auto_complete_user_edit_results()

        ###################### remove border ######################
        # self.remove_border(self.tab_main)
        # self.remove_border(self.tab_devices)
        # show commands submit button

        self.update_mon_all_devices()

        # configuration section
        self.update_mgmt_config_all_devices()

        #update devices in all configurations section
        self.update_configs_all_devices()
        # configurations
        self.tab_configs.setCurrentIndex(0)
