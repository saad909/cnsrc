from PyQt5.QtWidgets import *
import os


class basic_tasks(QDialog):
    def create_vlan(self):
        vlan_id = self.bt_set_vlan_no.text()
        vlan_desc = self.bt_set_vlan_desc.toPlainText()
        data_dictionary = {
            "vlan_id": vlan_id,
            "vlan_desc": vlan_desc,
        }
        filename = os.path.join("basic_tasks", "create_vlan")
        my_config = self.gen(data_dictionary, filename)
        print(my_config)
