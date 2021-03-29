import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pysqlcipher3 import dbapi2 as sqlite3


class users(QDialog):

    # database settingsk
    def clear_usr_add_fields(self):
        self.txt_usr_add_username.setText("")
        self.txt_usr_add_password.setText("")
        self.txt_usr_add_confirm_password.setText("")
        self.txt_usr_add_username.setFocus()

    def db_connection(self):
        self.con = sqlite3.connect("users.db")
        self.cur = self.con.cursor()
        self.cur.execute("PRAGMA key = 'secret'")
        self.cur.execute("PRAGMA kdf_iter = 24000")

    def add_user(self):
        # get values from gui
        username = self.txt_usr_add_username.text()
        password = self.txt_usr_add_password.text()
        confirm_password = self.txt_usr_add_confirm_password.text()

        if username and password and confirm_password:
            # check for password and confirm password matching
            if password != confirm_password:
                QMessageBox.information(self, "Warning", "Passwords does not match")
                self.clear_usr_add_fields()
                return

            query = "insert into users(username, password) values(?,?)"
            self.cur.execute(query, (username, password))
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
        pass

    def delete_user(self):
        pass

    # backend connected and store into databse but need to change the DBMS to MySQL
    # change the backend and complete add, delete and edit user
