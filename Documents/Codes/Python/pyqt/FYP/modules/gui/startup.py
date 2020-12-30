###################### startup settings ###################### 

from re import sub
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import glob
class startup_settings(QDial):

    def startup(self):

        ###################### load user settings ###################### 
        
        # update all devices table
        self.clear_device_search_results()

        self.load_settings() 

        #update devices in show commands section
        self.update_bt_all_devices()
        

        ###################### hide the tabs ###################### 
        # main tab
        self.tab_main.tabBar().setVisible(False)
        # self.tab_devices.tabBar().setVisible(False)
        ###################### devices ###################### 

        ##### ALL Devices Table ###### 

        # set auto completion for search boxes
        self.auto_complete_search_results()
        
        
        ##### edit or delete device ###### 
        
        # set auto completion for search boxes
        self.auto_complete_edit_results()
        
        
        ###################### remove border ###################### 
        self.remove_border(self.tab_main)
        self.remove_border(self.tab_devices)
        
        

