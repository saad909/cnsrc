import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os


class users(QDialog):
    # database settings
    def get_all_users(self):
        query = "SELECT * FROM users"
        return self.cur.execute(query).fetchall()

    def clear_usr_add_fields(self):
        self.txt_usr_add_username.setText("")
        self.txt_usr_add_password.setText("")
        self.txt_usr_add_confirm_password.setText("")
        self.txt_usr_add_username.setFocus()

    def db_connection(self):
        self.con = sqlite3.connect("users.db")
        self.cur = self.con.cursor()
        self.cur.execute("PRAGMA key = 'secret'")

    def add_user(self):
        # get values from gui
        username = self.txt_usr_add_username.text()
        password = self.txt_usr_add_password.text()

        # check for user already existance
        all_users = self.get_all_users()
        user_exists = False
        for user in all_users:
            if user[0] == username:
                user_exists = True
                break
        if user_exists:
            QMessageBox.information(self, "Warning", f"{username} already exists")
            self.clear_usr_add_fields()
            return

        # if user does not exists then run this code
        confirm_password = self.txt_usr_add_confirm_password.text()

        if username and password and confirm_password:
            # check for password and confirm password matching
            if password != confirm_password:
                QMessageBox.information(self, "Warning", "Passwords does not match")
                self.txt_usr_add_password.setText("")
                self.txt_usr_add_confirm_password.setText("")
                self.txt_usr_add_password.setFocus()
                return

            # add user into databse with hashed password
            hashed_password = self.hash_password(password)
            print(hashed_password)
            query = "insert into users(username, password) values(?,?)"
            self.cur.execute(query, (username, hashed_password))
            selection = QMessageBox.question(
                self,
                "Attention",
                "Do you really want to add user?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.No,
            )
            if selection == QMessageBox.Yes:
                self.con.commit()
                self.clear_usr_add_fields()

                QMessageBox.information(
                    self, "Note", f"user {username} addedd successfully"
                )
                self.fill_all_users_table(self.get_all_users())
            else:
                self.clear_usr_add_fields()

    def edit_user(self):
        # get values from gui

        username = self.txt_usr_edit_username.text()
        password = self.txt_usr_edit_password.text()
        new_password = self.txt_usr_edit_new_password.text()
        confirm_password = self.txt_usr_edit_confirm_password.text()
        # get the previous values to check for change made

        """
              Algorithm of this function
              # check whether search was done before or not 
                    # if searched -> then check whether the username is changed or not
                        # if username changed ->  then check whether user wants to change to password
                            # want to chang password = yes -> check for same new and confirm password
                                # if not same -> then not same error and clear confirm  password and focus
                                # if same -> edit the user
                        # if username not changed -> check for password change 
                            # password change = yes -> check for same new and confirm password
                                # if not same -> then not same error and clear confirm  password and focus
                            # password not changed -> made no change

        """

        if self.usr_searched:
            username_before = self.user_data[0]
            password_before = self.user_data[1]
            print(f"username before = {username_before}")
            print(f"password before = {password_before}")

            if username_before != username:
                # check for username duplcaton
                all_users = self.get_all_users()
                for user in all_users:
                    if username == user[0]:
                        QMessageBox.information(
                            self, "Warning", "username already exists"
                        )
                        self.txt_usr_edit_username.setFocus()
                        return

                # want to change password
                if new_password and confirm_password:
                    if new_password == confirm_password:
                        # edit user
                        selection = QMessageBox.question(
                            self,
                            "Note",
                            "Want to edit the device",
                            QMessageBox.Yes | QMessageBox.No,
                            QMessageBox.No,
                        )
                        if selection == QMessageBox.Yes:
                            query = f"UPDATE users set username=?, password=? where username={username}"
                            self.cur.execute(
                                query,
                                (
                                    username,
                                    self.hash_password(new_password),
                                ),
                            )
                            self.con.commit()
                            QMessageBox.information(
                                self, "Note", "User edited successfully"
                            )
                            self.fill_all_users_table(self.get_all_users())
                        else:
                            self.clear_usr_edit_fields()
                            return

                    else:
                        QMessageBox.information(
                            self, "Warning", "Passwords does not match"
                        )
                        self.txt_usr_edit_confirm_password.setText("")
                        self.txt_usr_edit_confirm_password.setFocus()
                elif new_password and not confirm_password:
                    QMessageBox.information(
                        self, "Warning", "Confirm password is field is empty"
                    )
                elif confirm_password and not new_password:
                    QMessageBox.information(
                        self, "Warning", "New password is field is empty"
                    )
                # username change but don't want to change the password
                else:
                    # edit user
                    selection = QMessageBox.question(
                        self,
                        "Note",
                        "Want to edit the device",
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.No,
                    )
                    if selection == QMessageBox.Yes:
                        query = f"UPDATE users set username=? where username=?"
                        self.cur.execute(query, (username,))
                        self.con.commit()
                        QMessageBox.information(
                            self, "Note", "User edited successfully"
                        )
                        self.fill_all_users_table()
                    else:
                        self.clear_usr_edit_fields()
                        return
            # username not changed but check for password change
            else:
                # want to change password
                if new_password and confirm_password:
                    if new_password == confirm_password:
                        # edit user
                        selection = QMessageBox.question(
                            self,
                            "Note",
                            "Want to edit the device",
                            QMessageBox.Yes | QMessageBox.No,
                            QMessageBox.No,
                        )
                        if selection == QMessageBox.Yes:
                            query = (
                                f"UPDATE users set password=? where username={username}"
                            )
                            self.cur.execute(query, (self.hash_password(new_password),))
                            self.con.commit()
                            QMessageBox.information(
                                self, "Note", "User edited successfully"
                            )
                            self.fill_all_users_table(self.get_all_users())
                        else:
                            self.clear_usr_edit_fields()
                            return

                    else:
                        QMessageBox.information(
                            self, "Warning", "Passwords does not match"
                        )
                        self.txt_usr_edit_confirm_password.setText("")
                        self.txt_usr_edit_confirm_password.setFocus()
                elif new_password and not confirm_password:
                    QMessageBox.information(
                        self, "Warning", "Confirm password is field is empty"
                    )
                elif confirm_password and not new_password:
                    QMessageBox.information(
                        self, "Warning", "New password is field is empty"
                    )
                else:
                    QMessageBox.information(self, "Note", "You made no changes")
        else:
            QMessageBox.information(self, "Warning", "Please search the user before")
            self.clear_usr_edit_fields()

            # check for password matching
        # username and  password values check
        # if not username and not password:
        #     QMessageBox.information(self, "Warning", "Please search the user first")
        #     self.clear_usr_edit_fields()
        #     return
        # elif (username and not password) or (password and not username):
        #     QMessageBox.information(self, "Warning", "You removed one field")
        #     self.clear_usr_edit_fields()
        #     return
        # elif (username != username.before) or (password != password_before):
        #     QMessageBox.information(self, "Warning", "Results were changed")
        #     self.clear_usr_edit_fields()
        #     return
        # else:
        #     # check for passwords
        #     if new_password and confirm_password:
        #         # passwords are given but not same
        #         if new_password != confirm_password:
        #             QMessageBox.information(self, "Warning", "Passwords does not match")
        #             self.txt_usr_edit_confirm_password.setText("")
        #             self.txt_usr_edit_confirm_password.setFocus()
        #             return
        #         # new password and confirm passwords are given and match
        #         else:
        #             # check for changed password and before password matching
        #             if password_before == password and username_before == username:
        #                 QMessageBox.information(
        #                     self,
        #                     "Note",
        #                     "You made no changes",
        #                 )
        #                 return
        #             else:
        #                 self.hash_password(password)
        #                 selection = QMessageBox.question(
        #                     self,
        #                     "Note",
        #                     "Want to edit the device",
        #                     QMessageBox.Yes | QMessageBox.No,
        #                     QMessageBox.No,
        #                 )
        #         if selection == QMessageBox.Yes:
        #             pass
        #     # new password is given but confirm password is not given
        #     elif new_password and not confirm_password:
        #         self.txt_usr_edit_confirm_password.setFocus()
        #         return
        #     # confirm password is given but new password is not given
        #     elif confirm_password and not new_password:
        #         self.txt_usr_edit_new_password.setFocus()
        #         return
        #     else:
        #         selection = QMessageBox.question(
        #             self,
        #             "Note",
        #             "Want to edit the device",
        #             QMessageBox.Yes | QMessageBox.No,
        #             QMessageBox.No,
        #         )
        #     if selection == QMessageBox.Yes:
        #         query = "UPDATE users set username=?, password=?"

    def delete_user(self):
        username = self.txt_usr_edit_username.text()
        if username:
            selection = QMessageBox.information(
                self,
                "Warning",
                "Do you really want to delete user?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.No,
            )
            # delete the user
            if selection == QMessageBox.Yes:
                query = "DELETE FROM users where username=?"
                self.cur.execute(query, (username,))
                self.con.commit()
                QMessageBox.information(self, "Note", "User deleted successfully")
                self.clear_usr_edit_fields()

            elif selection == QMessageBox.Cancel:
                self.clear_usr_edit_fields()
                return
        else:
            QMessageBox.information(self, "Warning", "Please search the user first")
            self.clear_usr_edit_fields()
            return

    def fill_usr_edit_search_results(self):
        self.searched_user = self.txt_usr_username_search.text()
        if self.searched_user:
            all_users = self.get_all_users()
            # checking the username
            user_exists = False
            self.user_data = list()
            for user in all_users:
                if user[0] == self.searched_user:
                    user_exists = True
                    # username at index 0
                    self.user_data.append(user[0])
                    # password at index 1
                    self.user_data.append(user[1])
                    print("user exists")
                    break
            if user_exists:
                self.txt_usr_edit_username.setText(self.user_data[0])
                self.txt_usr_edit_password.setText(self.user_data[1])
                self.txt_usr_edit_password.setEnabled(False)
                self.usr_searched = True

            else:
                QMessageBox.information(self, "Warning", "No result found")
                self.clear_usr_edit_fields()
                return

    def clear_usr_edit_fields(self):
        self.txt_usr_edit_username.setText("")
        self.txt_usr_edit_password.setText("")
        self.txt_usr_edit_new_password.setText("")
        self.txt_usr_edit_confirm_password.setText("")
        self.txt_usr_username_search.setText("")
        self.txt_usr_username_search.setFocus()
        self.txt_usr_edit_password.setEnabled(True)

    def check_database_file(self):
        database_exists = os.path.isfile("users.db")
        if database_exists:
            return True
        else:
            return False

    def fill_all_users_table(self, all_users):
        # run this on startup for editing device
        self.usr_searched = False

        self.tbl_users.setRowCount(len(all_users))
        i = 0
        for user in all_users:
            username = user[0]
            password = user[1]
            self.tbl_users.setItem(i, 0, QTableWidgetItem(username))
            self.tbl_users.setItem(i, 1, QTableWidgetItem(password))
            i += 1

    def clear_users_filter_results(self):
        self.txt_usr_table_filter.setText("")
        self.txt_usr_table_filter.setFocus()
        self.fill_all_users_table(self.get_all_users())

    def filter_all_devices(self):
        search = self.txt_usr_table_filter.text()
        if search:
            all_users = self.get_all_users()
            searched_users = list()
            for user in all_users:
                if search in user[0]:
                    searched_users.append(user)
            QMessageBox.information(
                self, "Note", "{} user(s) founded".format(len(searched_users))
            )
            self.fill_all_users_table(searched_users)
            return
        else:
            QMessageBox.information(self, "Warning", "Search field can't be empty")
            self.txt_usr_table_filter.setFocus()
            self.fill_all_users_table(self.get_all_users())

            # also check the inventroy file
            # edit users
            # check for database file existance and integrity before showing the table
