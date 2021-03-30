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
            else:
                self.clear_usr_add_fields()

    def edit_user(self):
        # get values from gui
        pass

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
        searched_user = self.txt_usr_username_search.text()
        if searched_user:
            all_users = self.get_all_users()
            # checking the username
            user_exists = False
            user_data = list()
            for user in all_users:
                if user[0] == searched_user:
                    user_exists = True
                    # username at index 0
                    user_data.append(user[0])
                    # password at index 1
                    user_data.append(user[1])
                    print("user exists")
                    break
            if user_exists:
                self.txt_usr_edit_username.setText(user_data[0])
                self.txt_usr_edit_password.setText(user_data[1])

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

    def check_database_file(self):
        database_exists = os.path.isfile("users.db")
        if database_exists:
            return True
        else:
            return False

    def fill_all_users_table(self):
        database_exists = self.check_database_file()
        if database_exists:
            all_users = self.get_all_users()
            self.tbl_users.setRowCount(len(all_users))
            i = 0
            for user in all_users:
                username = user[0]
                password = user[1]
                self.tbl_users.setItem(i, 0, QTableWidgetItem(username))
                self.tbl_users.setItem(i, 1, QTableWidgetItem(password))
                i += 1

    # backend connected and store into databse but need to change the DBMS to MySQL
    # change the backend and complete add, delete and edit user
