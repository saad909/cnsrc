import sqlite3
from PyQt5.QtWidgets import *


class user_auth(QDialog):
    def check_login_credentials(self):
        username = self.txt_login_username.text()
        password = self.txt_login_password.text()

        all_users = self.get_all_users()
        user_authenticated = False
        for user in all_users:
            if username == user[0]:
                if self.verify_hashed_password(user[1], pasword):
                    user_authenticated = True
                    break

        if user_authenticated:
            main_window = Main_Window()
            main_window.show()
