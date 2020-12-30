import re
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pprint import pprint

class devices_func(QDial):


    # clear the text boxes
    def clear_text_box(self,widget):
        widget.setText("")

    def highlight_border_false(self,widget):
        widget.setStyleSheet("")


##### higlight the border-> make red if left empty ###### 


    def highlight_border(self,widget):
        widget.setStyleSheet("border-color: darkred;")


    ###################### get ip in correct form  ###################### 


    def get_valid_ip(self,textBox):
        # validate ip address input
        octet = "(?:[0-1]?[0-9]?[0-9]|2?[0-4]?[0-9]|25?[0-4])"
        ipRegExp = QRegExp('^' + octet + r'\.' + octet + r'\.' + octet + r'\.' + octet + '$')
        ipValidator = QRegExpValidator(ipRegExp)
        textBox.setValidator(ipValidator)
        
        


    def is_ip_complete(self,ipTextBox):

        ip_address = ipTextBox.text()
        octet = "(?:[0-1]?[0-9]?[0-9]|2?[0-4]?[0-9]|25?[0-4])"
        reg_exp = '^' + octet + r'\.' + octet + r'\.' + octet + r'\.' + octet + '$'
        result = list()
        result = re.findall(reg_exp,ip_address)
        if len(result) == 1:
            return True
        else:
            return False
        
    

    def clear_add_devices_fileds(self):
        self.clear_text_box(self.d_add_hostname)
        self.clear_text_box(self.d_add_ip_address)
        self.clear_text_box(self.d_add_username)
        self.clear_text_box(self.d_add_password)
        self.clear_text_box(self.d_add_secret)
        self.d_add_device_type.setCurrentIndex(0)

    

################################ ALL Devices Section ################################# 

    def fill_devices_table(self,devices):
        devices_count = len(devices)
        self.tbl_devices.setRowCount(devices_count)
        i = 0
        for device in devices:
            
            # get the values
            hostname = device['hostname']
            ip = device['data']['host']
            username = device['data']['username']
            password = device['data']['password']
            secret = device['data']['secret']
            groups = device['groups']
            device_type = device['type']
                
            
            self.tbl_devices.setItem(i,0,QTableWidgetItem(hostname))
            self.tbl_devices.setItem(i,1,QTableWidgetItem(ip))
            self.tbl_devices.setItem(i,2,QTableWidgetItem(username))
            self.tbl_devices.setItem(i,3,QTableWidgetItem(password))
            self.tbl_devices.setItem(i,4,QTableWidgetItem(secret))

            all_groups = ""
            if len(groups) == 1:
                all_groups = str(groups[0])
            else:
                for group in groups:
                    if len(group) != 1:
                        all_groups += str(group) + ", "

            self.tbl_devices.setItem(i,5,QTableWidgetItem(all_groups))

            self.tbl_devices.setItem(i,6,QTableWidgetItem(device_type))



            i += 1
    def update_devices_table(self):
        not_empty = self.check_for_host_file()
        if not_empty:
            print("host file is not empty")
        else:
            print("host file is empty") 
        if not_empty:
            test_devices = self.convert_host_file_into_list()


            host_file = self.get_host_file_path()
            devices = self.read_yaml_file(host_file)
            # fill the table
        else:
            self.fill_devices_table(devices)

    ###################### search device ###################### 
    def auto_complete_search_results(self):
        all_ip_addresses_list = self.get_all_devices_ip()
        all_hostnames_list = self.get_all_devices_hostname()
        self.auto_fill(all_ip_addresses_list,self.txt_d_all_ip_address)
        self.auto_fill(all_hostnames_list,self.txt_d_all_hostname)

    def get_all_devices_hostname(self):
        devices = self.convert_host_file_into_list()
        all_hostnames = list()
        for device in devices:
            all_hostnames.append(device['hostname'])
        return all_hostnames

    def get_all_devices_ip(self):
        devices = self.convert_host_file_into_list()
        all_ips = list()
        for device in devices:
            all_ips.append(device['data']['host'])
        return all_ips

        


    def auto_fill(self,completion_list,destination_box):
       completer = QCompleter(completion_list)
       destination_box.setCompleter(completer)

    def search_device(self):
        # check the empty values
        hostname = self.txt_d_all_hostname.text()
        ip_address = self.txt_d_all_ip_address.text()
        print(hostname,ip_address)

        # ip address and hostname both are empty
        if not (hostname  or ip_address):
            QMessageBox.information(self,"Note","Please enter ip address or hostname")
            self.txt_d_all_ip_address.setFocus()
            self.highlight_border(self.txt_d_all_hostname)
            return
        search_key = None

        # ip address and hostname both are given
        if hostname and ip_address:
            # default search is by ip_address

            search_key = ip_address

            devices = self.convert_host_file_into_list()

            searched_devices = list()

            for device in devices:
                if search_key in device['data']['host']:
                    searched_devices.append(device)

            if searched_devices:
                self.clear_device_search_results()
                QMessageBox.information(self,"Infromation","{} result(s) were found".format(len(searched_devices)))
                pprint(searched_devices)
                self.fill_devices_table(searched_devices)
                return
            else:
                QMessageBox.information(self,"Note","No match found for ip now searching using hostname")

                search_key = hostname
                devices = self.convert_host_file_into_list()
                searched_devices = list()
                for device in devices:
                    if search_key.lower() in device['hostname'].lower():
                        searched_devices.append(device)
                if searched_devices:
                    self.clear_device_search_results()
                    QMessageBox.information(self,"Infromation","{} result(s) were found".format(len(searched_devices)))
                    pprint(searched_devices)
                    self.fill_devices_table(searched_devices)
                    return
                else:
                    QMessageBox.information(self,"Note","No result(s) found using hostname ")
                    self.clear_device_all_user_search()
                    self.txt_d_all_ip_address.setFocus()
                    return

        
        # only hostname is given
        if hostname and not (ip_address):
            search_key = hostname
            devices = self.convert_host_file_into_list()
            searched_devices = list()
            for device in devices:
                if search_key.lower() in device['hostname'].lower():
                    searched_devices.append(device)
            if searched_devices:
                self.clear_device_search_results()
                QMessageBox.information(self,"Infromation","{} result(s) were found".format(len(searched_devices)))
                pprint(searched_devices)
                self.fill_devices_table(searched_devices)
                return
            else:
                QMessageBox.information(self,"Note","No result found")
                self.clear_device_search_results()
                self.txt_d_all_hostname.setFocus()
                return

        # only  ip address is given
        if ip_address and not (hostname):
            search_key = ip_address
            devices = self.convert_host_file_into_list()
            searched_devices = list()
            for device in devices:
                if search_key in device['data']['host']:
                    searched_devices.append(device)
            if searched_devices:
                self.clear_device_search_results()
                QMessageBox.information(self,"Infromation","{} result(s) were found".format(len(searched_devices)))
                pprint(searched_devices)
                self.fill_devices_table(searched_devices)
                return
            else:
                QMessageBox.information(self,"Note","No result found")
                self.clear_device_search_results()
                self.txt_d_all_ip_address.setFocus()
                return

                    

        
    
    
    
    def clear_device_search_results(self):
        self.clear_text_box(self.txt_d_all_ip_address)
        self.clear_text_box(self.txt_d_all_hostname)

        self.fill_devices_table(self.convert_host_file_into_list())








################################ Delete or edit the device ################################# 

    ##### clear top bar search results ###### 
    def auto_complete_edit_results(self):
        all_ip_addresses = self.get_all_devices_ip()
        all_hostnames = self.get_all_devices_hostname()
        self.auto_fill(all_ip_addresses,self.txt_d_edit_ip_address)
        self.auto_fill(all_hostnames,self.txt_d_edit_hostname)


    ###################### edit the deivce ###################### 

    def clear_edit_search_results(self):
        self.d_edit_hostname.setText("")
        self.d_edit_ip_address.setText("")
        self.d_edit_username.setText("")
        self.d_edit_password.setText("")
        self.d_edit_secret.setText("")
        self.d_edit_device_type.setCurrentIndex(0)


    def fill_edit_search_results(self,device):
        self.d_edit_hostname.setText(device['hostname'])
        self.d_edit_ip_address.setText(device['data']['host'])
        self.d_edit_username.setText(device['data']['username'])
        self.d_edit_password.setText(device['data']['password'])
        self.d_edit_secret.setText(device['data']['secret'])
        if device['type'] == 'router':
            self.d_edit_device_type.setCurrentIndex(1)
        elif device['type'] == 'switch':
            self.d_edit_device_type.setCurrentIndex(2)



    def edit_search_device(self):
        self.clear_edit_search_results()
        # check the empty values
        hostname = self.txt_d_edit_hostname.text()
        ip_address = self.txt_d_edit_ip_address.text()
        print(hostname,ip_address)

        # ip address and hostname both are empty
        if not (hostname  or ip_address):
            QMessageBox.information(self,"Note","Please enter ip address or hostname")
            self.txt_d_edit_ip_address.setFocus()
            self.highlight_border(self.txt_d_edit_hostname)
            return


        # ip address and hostname both are given
        search_key = None
        if hostname and ip_address:

            # default search is by ip_address

            if not self.is_ip_complete(self.txt_d_edit_ip_address):
                self.highlight_border(self.txt_d_edit_ip_address)
                QMessageBox.information(self,"Warning","Entered a wrong ip address.Now searching using hostname")

                search_key = hostname
                devices = self.convert_host_file_into_list()
                searched_device = None
                for device in devices:
                    if search_key == device['hostname']:
                        searched_device = device
                        break
                if searched_device:
                    pprint(searched_device)
                    self.fill_edit_search_results(searched_device)
                    self.device_before = searched_device
                    return
                else:
                    QMessageBox.information(self,"Note","hostname is not found")
                    self.clear_device_edit_user_search()
                    self.txt_d_edit_ip_address.setFocus()
                    return
            else: 
                self.highlight_border_false(self.d_add_ip_address)
                self.highlight_border_false(self.d_add_hostname)
                search_key = ip_address
                devices = self.convert_host_file_into_list()
                searched_device = None
                for device in devices:
                    if search_key == device['data']['host']:
                        searched_device = device
                        break

                if searched_device:
                    pprint(searched_device)
                    self.fill_edit_search_results(searched_device)
                    self.device_before = searched_device
                    return
                else:
                    QMessageBox.information(self,"Note","ip address not found. Now searching using hostname")
                    searched_key = hostname
                    devices = self.convert_host_file_into_list()
                    searched_device = None
                    for device in devices:
                        if search_key == device['hostname']:
                            searched_device = device
                            break
                    if searched_device:
                        pprint(searched_device)
                        self.fill_edit_search_results(searched_device)
                        self.device_before = searched_device
                        return
                    else:
                        QMessageBox.information(self,"Note","hostname is not found")
                        self.clear_device_edit_user_search()
                        self.txt_d_edit_ip_address.setFocus()
                        return
                        



        # only hostname is given
        if hostname and not (ip_address):
            search_key = hostname
            devices = self.convert_host_file_into_list()
            searched_device = None
            for device in devices:
                if search_key == device['hostname']:
                    searched_device = device
                    break
            if searched_device:
                pprint(searched_device)
                self.fill_edit_search_results(searched_device)
                self.device_before = searched_device
                return
            else:
                QMessageBox.information(self,"Note","Host not found")
                self.clear_device_edit_user_search()
                self.txt_d_edit_hostname.setFocus()

        # only  ip is given
        if ip_address and not (hostname):

            if not self.is_ip_complete(self.txt_d_edit_ip_address):
                self.highlight_border(self.txt_d_edit_ip_address)
                self.txt_d_edit_ip_address.setFocus()
                QMessageBox.information(self,"Warning","Entered a wrong ip address")
                self.clear_device_edit_user_search()
                self.txt_d_edit_ip_address.setFocus()
                return

            else: 
                self.highlight_border_false(self.d_add_ip_address)

            search_key = ip_address
            devices = self.convert_host_file_into_list()
            searched_device = None
            for device in devices:
                if search_key == device['data']['host']:
                    searched_device = device
                    break
            if searched_device:
                pprint(searched_device)
                self.fill_edit_search_results(searched_device)
                self.device_before = searched_device
                return
            else:
                QMessageBox.information(self,"Note","Host not found")
                return

                    

    def change_group_type(self,device,group_type):
        # get the device before group
        if self.device_before['groups'][0] == group_type:
            return
        else:
            device['groups'][0] = group_type
        

    def edit_device(self):
        hostname = self.d_edit_hostname.text()
        ip_address = self.d_edit_ip_address.text()
        username = self.d_edit_username.text()
        password = self.d_edit_password.text()
        secret = self.d_edit_secret.text()
        device_type_index = self.d_edit_device_type.currentIndex()
        
        
        device = self.create_dictionary(hostname,ip_address,username,password,secret,device_type_index)
        
            
            
        ##### check for empty boxes ###### 

        if not hostname:
            self.highlight_border(self.d_edit_hostname)
            self.statusBar().showMessage("Hostname can not be empty")
            self.d_edit_hostname.setFocus()
            return
        else:
            self.highlight_border_false(self.d_edit_hostname)
        if self.d_edit_ip_address and self.is_ip_complete(self.d_edit_ip_address):
            self.highlight_border_false(self.d_edit_ip_address)
        else:
            self.highlight_border(self.d_edit_ip_address)
            self.statusBar().showMessage("Invalid Ip Address")
            self.d_edit_ip_address.setFocus()
            
            return
            
        if not username:
            self.highlight_border(self.d_edit_username)
            self.statusBar().showMessage("username can not be empty")
            self.d_edit_username.setFocus()
            return
        else:
            self.highlight_border_false(self.d_edit_username)
        if not password:
            self.highlight_border(self.d_edit_password)
            self.statusBar().showMessage("password can not be empty")
            self.d_edit_password.setFocus()
            return
        else:
            self.highlight_border_false(self.d_edit_password)
        if not secret:
            self.highlight_border(self.d_edit_secret)
            self.statusBar().showMessage("Eanble password can not be empty")
            self.d_edit_secret.setFocus()
            return
        else:
            self.highlight_border_false(self.d_edit_secret)
            
        if device == self.device_before:
            QMessageBox.information(self,"Warning","You made no changes")
            return

        else:
            
            ##### check for ip or hostname duplication ###### 
            
            
            hostname_before = self.device_before['hostname']
            ip_before = self.device_before['data']['host']
            
            hostname_changed = None
            if hostname != hostname_before:
                hostname_changed = True
                # hostname check
                all_hostnames = self.get_all_devices_hostname()
                status = None
                if hostname in all_hostnames:
                    status = True
                if status: 
                    self.d_edit_hostname.setFocus()
                    self.highlight_border(self.d_edit_hostname)
                    QMessageBox.information(self,"Waring","A device with the same hostname already exists")
                    return
            if ip_address != ip_before:
                # ip check
                all_ip_addresses = self.get_all_devices_ip()
                status = None
                if ip_address in all_ip_addresses:
                    status = True
                if status:
                    self.d_edit_ip_address.setFocus()
                    self.highlight_border(self.d_edit_ip_address)
                    QMessageBox.information(self,"Waring","A device with the same ip address already exists")
                    return

            selection = QMessageBox.question(self,"Alert","Do you want to make changes",
                    QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel,
                    QMessageBox.No
            )
            if selection == QMessageBox.Yes:
                devices = self.convert_host_file_into_list()
                # get the index
                device_index = None
                i = 0
                print("---------------- Devices Before ----------------")
                pprint(devices)
                for device in devices:
                    if self.device_before['hostname'] == device['hostname']:
                        device_index = i
                    i += 1
                devices[device_index]['hostname'] = hostname
                devices[device_index]['data']['host'] = ip_address
                devices[device_index]['data']['username'] = username
                devices[device_index]['data']['password'] = password
                devices[device_index]['data']['secret'] = secret

                # setting device type
                if device_type_index == 1:
                    devices[device_index]['type'] = 'router'

                elif device_type_index == 2:
                    devices[device_index]['type'] = 'switch'

                # device group based on type
                if devices[device_index]['type'] == 'router':
                    self.change_group_type(devices[device_index],'router')

                elif devices[device_index]['type'] == 'switch':
                    self.change_group_type(devices[device_index],'switch')

                print("---------------- Devices After Editing ----------------")
                pprint(devices)

                # write to the inventory file
                self.write_inventory(devices)

                QMessageBox.information(self,"Success","Data modified successfully")
                # update all devices table
                self.clear_device_search_results()
                # update autocomplete list of ip_addresses and hostnames
                self.auto_complete_edit_results()
                self.auto_complete_search_results()
                # clear search results
                self.clear_edit_search_results()
                self.clear_device_edit_user_search()
            elif selection == QMessageBox.Cancel:
                self.clear_edit_search_results()
                self.clear_device_edit_user_search()

                
    ##################### delete the device ###################### 
    
    def clear_device_edit_user_search(self):
        self.txt_d_edit_ip_address.setText("")
        self.txt_d_edit_hostname.setText("")

    def delete_device(self):
        hostname_before = self.device_before['hostname']
        hostname = self.d_edit_hostname.text()
        
        if hostname:
            if hostname == hostname_before:
                selection = QMessageBox.question(self,"Warning","Do you want to delete the device ?",
                
                        QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel,
                        QMessageBox.No
                )
                if selection == QMessageBox.Yes:
                    devices = self.convert_host_file_into_list()
                    # getting the deletion device index
                    index = None
                    i = 0
                    for device in devices:
                        if device['hostname'] == hostname:
                            index = i
                            break
                        i += 1

                    devices.pop(index)

                    # write to the inventory file
                    self.write_inventory(devices)

                    QMessageBox.information(self,"Success","host deleted successfully")
                    # update all devices table
                    self.clear_device_search_results()
                    # update autocomplete list of ip_addresses and hostnames
                    self.auto_complete_edit_results()
                    self.auto_complete_search_results()
                    # clear search results
                    self.clear_edit_search_results()
                    self.clear_device_edit_user_search()
                        
                else:
                    self.clear_edit_search_results()
                    self.clear_device_edit_user_search()
            else:
                QMessageBox.information(self,"Failed","You alterd the results")
                self.clear_edit_search_results()
                self.clear_device_edit_user_search()
        else:
            QMessageBox.information(self,"Failed","hostname can't be empty")
            self.clear_edit_search_results()
            self.clear_device_edit_user_search()
