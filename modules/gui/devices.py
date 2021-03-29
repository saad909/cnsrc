from PyQt5.QtWidgets import *


class devices(QDialog):
    def add_host(self):
        ##### getting the values from the boxes ######

        hostname = self.d_add_hostname.text()
        ip_address = self.d_add_ip_address.text()
        username = self.d_add_username.text()
        password = self.d_add_password.text()
        secret = self.d_add_secret.text()
        device_type_index = self.d_add_device_type.currentIndex()

        ##### checking for empty boxes ######

        if not hostname:
            self.highlight_border(self.d_add_hostname)
            self.statusBar().showMessage("Hostname can not be empty")
            self.d_add_hostname.setFocus()
            return
        else:
            self.highlight_border_false(self.d_add_hostname)
        if self.d_add_ip_address and self.is_ip_complete(self.d_add_ip_address):
            self.highlight_border_false(self.d_add_ip_address)
        else:
            self.highlight_border(self.d_add_ip_address)
            self.statusBar().showMessage("Invalid Ip Address")
            self.d_add_ip_address.setFocus()

            return

        if not username:
            self.highlight_border(self.d_add_username)
            self.statusBar().showMessage("username can not be empty")
            self.d_add_username.setFocus()
            return
        else:
            self.highlight_border_false(self.d_add_username)
        if not password:
            self.highlight_border(self.d_add_password)
            self.statusBar().showMessage("password can not be empty")
            self.d_add_password.setFocus()
            return
        else:
            self.highlight_border_false(self.d_add_password)
        if not secret:
            self.highlight_border(self.d_add_secret)
            self.statusBar().showMessage("Eanble password can not be empty")
            self.d_add_secret.setFocus()
            return
        else:
            self.highlight_border_false(self.d_add_secret)
        if device_type_index == 0:
            self.highlight_border(self.d_add_device_type)
            self.statusBar().showMessage("Please select the device type")
            self.d_add_device_type.setFocus()
            return
        else:
            self.highlight_border_false(self.d_add_device_type)

        # create the dictionary
        password = self.encrypt_password(password)
        secret = self.encrypt_password(secret)
        device = self.create_dictionary(
            hostname, ip_address, username, password, secret, device_type_index
        )

        # add host_into inventory
        added = self.add_host_into_inventory(device)

        if added:
            QMessageBox.information(self, "Success", "Device added successfully")
            # clearing the fileds
            self.clear_add_devices_fileds()

            # Update the all device table
            self.clear_device_search_results()
            # update autocomplete list of ip_addresses and hostnames
            self.auto_complete_edit_results()
            self.auto_complete_search_results()
            # update devices in show commands combo box
            self.update_bt_all_devices()
            # update devices in group addition
            self.add_devices_for_group_selection()
