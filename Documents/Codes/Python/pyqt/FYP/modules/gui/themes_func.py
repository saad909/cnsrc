from PyQt5.QtWidgets import *
import os
class themes_func(QDial):


    def apply_theme(self,theme_name):
        theme_path = os.path.join("themes", theme_name + ".css")
        style = None
        with open(theme_path,"r") as handler:
            style = handler.read()
        self.setStyleSheet(style)
        self.apply_user_defined_changes('theme',theme_name)
    
    def remove_border(self,widget):
        # style = 'QWidget#{0} {border: 0px;}'.format(widget)
        self.setStyleSheet("QtWidget#{widget} {'border: 0px;}")

        

