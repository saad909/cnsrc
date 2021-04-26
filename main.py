import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from imports import *

ui, _ = loadUiType("main.ui")
login, _ = loadUiType("login.ui")


class Login(QWidget, login, password_hashing):
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
            QMessageBox.information(self, "Warning", "username does not exists")
            self.txt_login_username.setText("")
            self.txt_login_password.setText("")
            self.txt_login_username.setFocus()


class Main_Window(
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
    groups,
    users,
    password_hashing,
    password_encryption,
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
        self.get_valid_ip(self.d_edit_ip_address)

        # handle show commands button(enable/disable) state
        # self.cb_bt_all_groups.currentIndexChanged.connect(
        #     lambda: self.disable_box(self.cb_bt_all_groups, self.cb_bt_all_devices)
        # )

        # main_tab_window = self.tab_main.currentWidget().objectName()
        # sub_tab_window = self.tab_basic_tasks.currentWidget().objectName()

        # if main_tab_window == "configs" and sub_tab_window == "show_commands":
        ########## SHow section ##################
        # main toolbox index changed
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
            lambda: self.disable_box(self.cb_bt_all_devices, self.cb_bt_all_groups)
        )
        self.cb_bt_all_groups.textActivated.connect(
            lambda: self.disable_box(self.cb_bt_all_groups, self.cb_bt_all_devices)
        )
        self.show_commands_list.itemSelectionChanged.connect(
            self.show_commands_submit_button
        )
        self.config_show_btn_export.clicked.connect(self.export_show_output)
        self.config_show_btn_custom_commands.clicked.connect(self.add_custom_commands)

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
            lambda: self.export_table(self.tbl_devices, self.dev_all_txt_file_path)
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
            lambda: self.export_table(self.tbl_groups, self.grp_all_txt_file_path)
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
        self.btn_usr_clear_filter.clicked.connect(self.clear_users_filter_results)
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
