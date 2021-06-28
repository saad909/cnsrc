import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from imports import *


class Login(QWidget, Ui_login, password_hashing):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.db_connection()
        self.handle_login()

    def handle_login(self):
        self.btn_login.clicked.connect(self.check_login_credentials)

    def db_connection(self):
        self.con = sqlite3.connect("users.db")
        self.cur = self.con.cursor()

    def get_all_users(self):
        query = "SELECT * FROM users"
        return self.cur.execute(query).fetchall()

    def check_login_credentials(self):
        username = self.txt_login_username.text()
        password = self.txt_login_password.text()

        all_users = self.get_all_users()
        user_authenticated = False
        username_matched = False
        password_matched = False
        for user in all_users:
            if username == user[0]:
                username_matched = True
                if self.verify_hashed_password(user[1], password):
                    user_authenticated = True
                    break

        if user_authenticated:
            QMessageBox.information(self, "Succesfuly", "Login Succesful")
            self.close()
            main_window = Main_Window()
            main_window.show()
        elif username_matched and not password_matched:
            QMessageBox.information(self, "Note", "Wrong password")
            self.txt_login_password.setFocus()
            self.txt_login_password.setText("")
        else:
            QMessageBox.information(
                self, "Warning", "username does not exists")
            self.txt_login_username.setText("")
            self.txt_login_password.setText("")
            self.txt_login_username.setFocus()




class Main_Window(
    QMainWindow,
    Ui_main_window,
    startup_settings,
    devices,
    devices_func,
    inventory_mgmt_func,
    user_settings,
    Connection,
    update_combo_boxes,
    show_commands,
    basic_tasks,
    groups,
    users,
    password_hashing,
    password_encryption,
    configs,
    monitoring,
    configurations,
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
        # get valid identifier
        self.get_valid_identifier(self.dhcp_pool_name)
        self.get_valid_identifier(self.ppp_remote_username)
        self.get_valid_identifier(self.ppp_remote_password)
        self.get_valid_identifier(self.ppp_local_username)
        self.get_valid_identifier(self.ppp_local_password)
        self.get_valid_identifier(self.d_add_hostname)
        self.get_valid_identifier(self.d_add_username)
        self.get_valid_identifier(self.d_add_password)
        self.get_valid_identifier(self.d_add_secret)
        self.get_valid_identifier(self.d_edit_hostname)
        self.get_valid_identifier(self.d_edit_username)
        self.get_valid_identifier(self.d_edit_password)
        self.get_valid_identifier(self.d_edit_secret)
        self.get_valid_identifier(self.txt_d_all_hostname)
        self.get_valid_identifier(self.txt_g_edit_groupname)
        self.get_valid_identifier(self.g_edit_groupname)
        self.get_valid_identifier(self.g_add_groupname)
        self.get_valid_identifier(self.txt_g_all_group_name)
        self.get_valid_identifier(self.g_add_groupname)

        # get the valid ip
        self.get_valid_ip(self.d_add_ip_address)
        self.get_valid_ip(self.txt_d_all_ip_address)
        self.get_valid_ip(self.d_edit_ip_address)
        self.get_valid_ip(self.dhcp_network_address)
        self.get_valid_ip(self.dhcp_exclude_start)
        self.get_valid_ip(self.dhcp_exclude_end)
        self.get_valid_ip(self.dhcp_default_gateway)
        self.get_valid_ip(self.dhcp_dns_server)
        self.get_valid_ip(self.dhcp_ip_phone_gateway)
        # get valid subnet mask
        self.get_valid_subnet(self.dhcp_subnet_mask)
        # as_no and port number range = 1-65535
        self.get_valid_as_no(self.d_edit_port_number)
        self.get_valid_as_no(self.d_add_port_number)
        self.get_valid_as_no(self.txt_eigrp_as_number)
        self.get_valid_as_no(self.txt_process_id)
        self.get_valid_area_no(self.txt_ospf_area)

        ########## SHow section ##################
        # main toolbox index changed
        # show section
        self.load_settings()
        self.toolBox.currentChanged.connect(self.tool_box_and_tabs_movement)
        self.cb_bt_all_devices.textActivated.connect(
            lambda: self.check_for_activation(
                self.cb_bt_all_devices, self.cb_bt_all_groups
            )
        )
        self.cb_bt_all_groups.textActivated.connect(
            lambda: self.check_for_activation(
                self.cb_bt_all_groups, self.cb_bt_all_devices
            )
        )

        self.cb_bt_all_devices.textActivated.connect(
            lambda: self.disable_box(
                self.cb_bt_all_devices, self.cb_bt_all_groups)
        )
        self.cb_bt_all_groups.textActivated.connect(
            lambda: self.disable_box(
                self.cb_bt_all_groups, self.cb_bt_all_devices)
        )
        self.show_commands_list.itemSelectionChanged.connect(
            self.show_commands_submit_button
        )
        self.config_show_btn_export.clicked.connect(self.export_show_output)
        self.config_show_btn_custom_commands.clicked.connect(
            self.add_custom_commands)

        # devices configs section
        self.mgmt_config_config_type.textActivated.connect(self.fill_configs)
        self.mgmt_config_all_devices.textActivated.connect(self.fill_configs)
        # self.configs_list.itemClicked.connect(self.check_config_restore_button)
        self.mgmt_config_btn_backup.clicked.connect(
            self.show_configs_backup_window)
        # configurations
        self.configs_all_devices.textActivated.connect(
            self.fill_configurations)
        self.configs_all_configurations.textActivated.connect(
            self.move_configs_tab_index)
        # rip configuration
        self.chkbox_rip_loopback.stateChanged.connect(
            self.create_rip_configuration)
        self.chkbox_rip_directly.stateChanged.connect(
            self.create_rip_configuration)
        self.btn_push_rip_config.clicked.connect(self.configure_rip)
        self.btn_clear_rip.clicked.connect(self.clear_rip_results)
        # eigrp
        self.chkbox_eigrp_loopback.stateChanged.connect(
            self.create_eigrp_configuration)
        self.chkbox_eigrp_directly.stateChanged.connect(
            self.create_eigrp_configuration)
        self.btn_push_eigrp_config.clicked.connect(self.configure_eigrp)
        self.btn_clear_eigrp.clicked.connect(self.clear_eigrp_results)
        # ospf
        self.chkbox_ospf_loopback.stateChanged.connect(
            self.create_ospf_configuration)
        self.chkbox_ospf_directly.stateChanged.connect(
            self.create_ospf_configuration)
        self.btn_push_ospf_config.clicked.connect(self.configure_ospf)
        self.btn_clear_ospf.clicked.connect(self.clear_ospf_results)
        # dhcp server
        self.chkbox_exclude_range.stateChanged.connect(
            self.toggle_exclude_range)
        self.chkbox_default_gateway.stateChanged.connect(
            self.toggle_default_gateway)
        self.chkbox_dns_server.stateChanged.connect(self.toggle_dns_server)
        self.chkbox_ip_phone_gateway.stateChanged.connect(
            self.toggle_ip_phone_gateway)
        self.dhcp_btn_generate.clicked.connect(
            self.genereate_dhcp_server_config)
        self.btn_push_dhcp_server_config.clicked.connect(
            self.configure_dhcp_server)
        self.btn_clear_dhcp_server.clicked.connect(
            self.clear_dhcp_server_results)
        # dhcp client
        self.btn_configure_dhcp_client.clicked.connect(
            self.configure_dhcp_client)
        # ppp
        self.ppp_remote_all_devices.textActivated.connect(lambda: self.get_all_interfaces(
            self.ppp_remote_all_devices.currentText(), self.ppp_remote_all_interfaces))
        self.btn_ppp_remote_generate_config.toggled.connect(
            self.configure_remote_site)
        self.rb_pap.toggled.connect(self.check_for_authentication_method)
        self.rb_chap.toggled.connect(self.check_for_authentication_method)
        # self.ppp_remote_username.textChanged.connect(partial( self.for_chap_use_same_config,"username"))
        self.ppp_remote_password.textChanged.connect(
            self.for_chap_use_same_config)
        self.btn_ppp_local_generate_config.toggled.connect(
            self.generate_ppp_config)
        self.btn_ppp_push.clicked.connect(self.push_ppp_config)
        self.btn_clear_ppp.clicked.connect(self.clear_ppp_result)

    ###################### handle buttons action ######################

    def handleButtons(self):

        ################### Tab movement #####################
        ##### devices ######

        self.pb_dev_all.clicked.connect(
            lambda: self.tab_movement(1, self.tab_devices, 0)
        )
        self.pb_dev_add.clicked.connect(
            lambda: self.tab_movement(1, self.tab_devices, 1)
        )
        self.pb_dev_edit.clicked.connect(
            lambda: self.tab_movement(1, self.tab_devices, 2)
        )

        ##### basic tasks ######
        self.pb_bt_show_commands.clicked.connect(
            lambda: self.tab_movement(3, self.tab_basic_tasks, 0)
        )
        self.pb_bt_configurations.clicked.connect(
            lambda: self.tab_movement(3, self.tab_basic_tasks, 1)
        )
        ##### custom groups ######
        self.pb_grp_all.clicked.connect(
            lambda: self.tab_movement(2, self.tab_groups, 0)
        )
        self.pb_grp_add.clicked.connect(
            lambda: self.tab_movement(2, self.tab_groups, 1)
        )
        self.pb_grp_edit.clicked.connect(
            lambda: self.tab_movement(2, self.tab_groups, 2)
        )
        ##### users ######
        self.pb_usr_user_settings.clicked.connect(
            lambda: self.tab_movement(0, self.tab_users, 1)
        )
        # search button in all devices
        self.btn_g_all_search.clicked.connect(self.search_group)
        # clear button in all devices
        self.btn_g_all_clear.clicked.connect(self.clear_group_all_user_search)
        ################### button click action #####################
        ##### add device ######

        self.btn_d_add_save.clicked.connect(self.add_host)
        self.dev_add_btn_bulk_add.clicked.connect(self.bulk_device_addition)
        self.dev_add_btn_browse.clicked.connect(self.browse_file)

        ##### all devices ######

        self.btn_d_all_search.clicked.connect(self.search_device)
        self.btn_d_all_clear.clicked.connect(self.clear_device_search_results)
        # browse for export
        self.dev_all_btn_browse.clicked.connect(
            lambda: self.export_file_path(self.dev_all_txt_file_path)
        )
        # Export devices
        self.dev_all_btn_export.clicked.connect(
            lambda: self.export_table(
                self.tbl_devices, self.dev_all_txt_file_path)
        )

        ##### edit or delete devices ######

        self.btn_d_edit_search.clicked.connect(self.edit_search_device)

        self.btn_d_edit_edit.clicked.connect(self.edit_device)
        self.btn_d_edit_delete.clicked.connect(self.delete_device)
        self.btn_d_edit_clear.clicked.connect(self.clear_edit_search_results)

        ##### add, show, delete and edit custom groups ######
        # add a group
        self.g_add_submit.clicked.connect(self.add_group)
        # fill searched group results in edit or delete section
        self.btn_g_edit_search.clicked.connect(self.edit_group_search)
        # delete group
        self.pb_g_delete.clicked.connect(self.delete_group)
        # edit group
        self.pb_g_edit.clicked.connect(self.edit_group)
        # browse export file path
        self.grp_all_btn_browse.clicked.connect(
            lambda: self.export_file_path(self.grp_all_txt_file_path)
        )
        # export user
        self.grp_all_btn_export.clicked.connect(
            lambda: self.export_table(
                self.tbl_groups, self.grp_all_txt_file_path)
        )

        ##### show commands ######
        self.config_show_btn_submit.clicked.connect(self.run_show_command)

        ##### user Section ######
        # add user
        self.btn_usr_add_add.clicked.connect(self.add_user)
        # edit user
        self.btn_user_edit_edit.clicked.connect(self.edit_user)
        # delete user
        self.btn_usr_del_delete.clicked.connect(self.delete_user)
        # fill user search  results
        self.btn_usr_search.clicked.connect(self.fill_usr_edit_search_results)
        # clear fill user search results
        self.btn_usr_search_clear.clicked.connect(self.clear_usr_edit_fields)
        # filter button for all users
        self.btn_usr_filter.clicked.connect(self.filter_all_devices)
        # clear user filter results button for all users
        self.btn_usr_clear_filter.clicked.connect(
            self.clear_users_filter_results)
        # browse export file path
        self.usr_btn_browse.clicked.connect(
            lambda: self.export_file_path(self.usr_txt_file_path)
        )
        # export user
        self.usr_btn_export.clicked.connect(
            lambda: self.export_table(self.tbl_users, self.usr_txt_file_path)
        )


def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
