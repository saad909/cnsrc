from PyQt5.QtWidgets import *
from modules.networking.connection import ConnectionWithThreading
from PyQt5.QtCore import QThread, Qt, QRegExp
import re
import time
from PyQt5.QtGui import QRegExpValidator
from jinja2 import Environment, FileSystemLoader
from modules.networking.connection import WRITE_CONFIG as WC


class configurations(QDialog):

    # 0000000000000000000000 RIP section 0000000000000000000000000000
    def fill_configurations(self, device_name):
        # all_devices_list = self.convert_host_file_into_list()
        self.tab_configs.setCurrentIndex(0)
        if "Select a Device" in device_name:
            return

        all_devices = self.convert_host_file_into_list()
        my_device = {}
        for device in all_devices:
            if device['hostname'] == device_name:
                my_device = device
                break
        # if my_device['devices_func']
        if my_device['data']['device_type'] == 'cisco_ios':
            # router is selected
            self.configs_all_configurations.clear()
            if my_device['type'] == "Router":
                routing_protocols_list = [
                    '----------- Routing Protocols -----------',
                    'rip',
                    'ospf',
                    'eigrp',
                ]
                dhcp_configurations_list = [
                    '----------- DHCP -----------',
                    # "dhcp_server",
                    "dhcp",
                    # "dhcp_snooping",
                ]
                self.configs_all_configurations.addItems(
                    routing_protocols_list)
                self.configs_all_configurations.addItems(
                    dhcp_configurations_list)
                others_list = [
                    "----------- OTHER -----------",
                    "configure_static_ip",
                    "port channeling",
                    "ppp",
                    "clock",
                    "snmp",
                    "local users",
                    "loopback interface",
                    "hostname"
                ]
                self.configs_all_configurations.addItems(others_list)
                return
            elif my_device['type'] == "Switch":
                self.configs_all_configurations.clear()
                configs_list = [
                    "vlans",
                    "dns",
                    "default gateway",
                    "loopback",
                    "hostname"
                ]
                self.configs_all_configurations.addItems(configs_list)
                return
        else:
            QMessageBox.critical(
                self, "Warning", "Software currently supports only cisco_ios devices")
            return

    # def fill_device_interfaces(self, device_name):
        # print(type(all_interfaces))
        # print(all_interfaces)
        # self.dhcp_client_all_interfaces.addItems(all_interfaces)

    def move_configs_tab_index(self, config_selected):
        if not "-" in config_selected:
            page = self.tab_configs.findChild(QWidget, config_selected)
            index = self.tab_configs.indexOf(page)
            print(self.tab_configs.tabText(index))
            if self.tab_configs.tabText(index) == "dhcp":
                # fill the interfaces into box
                self.get_all_interfaces(
                    self.configs_all_devices.currentText(), self.dhcp_client_all_interfaces)
                # self.statusBar().showMessage("")
            print(f"INdex is {index}")
            self.tab_configs.setCurrentIndex(index)
        else:
            self.tab_configs.setCurrentIndex(0)
            return

    def genereate_rip_config(self, output):

        networks = list()
        if self.chkbox_rip_loopback.isChecked() == True:
            for line in output.splitlines():
                regex = re.compile(
                    r"^(G|E|F|L)[\w\/]+\s+(?P<ip_address>[\d.]+)\s+YES.+up\s+up.*")
                result = re.fullmatch(regex, line)
                if result:
                    # print(result)
                    networks.append(result.group("ip_address"))
        else:
            for line in output.splitlines():
                regex = re.compile(
                    r"^(G|E|F)[\w\/]+\s+(?P<ip_address>[\d.]+)\s+YES.+up\s+up.*")
                result = re.fullmatch(regex, line)
                if result:
                    # print(result)
                    networks.append(result.group("ip_address"))
        if networks:
            print(networks)
            rip_version = "1"
            if self.chkbox_rip_version.isChecked():
                rip_version = "2"

            rip_dict = {
                "networks": networks,
                "version": rip_version,
            }
            j2_env = Environment(
                loader=FileSystemLoader("hosts/templates/configurations"), trim_blocks=True, autoescape=True
            )
            template = j2_env.get_template("cisco_ios_rip.j2")
            configuration = template.render(data=rip_dict)
            if configuration:
                print(configuration)
                self.te_rip_config.clear()
                self.te_rip_config.insertPlainText(str(configuration))

            return

    def show_rip_errors(self, error):
        QMessageBox.critical(self, "Warning", error)
        self.clear_rip_results()
        return

    def create_rip_configuration(self):
        if (not self.chkbox_rip_loopback.isChecked() == True) and (not self.chkbox_rip_directly.isChecked() == True):
            self.te_rip_config.clear()

        if self.chkbox_rip_loopback.isChecked() == True or self.chkbox_rip_directly.isChecked() == True:

            device_name = self.configs_all_devices.currentText()
            all_devices = self.convert_host_file_into_list()
            my_device = {}
            for device in all_devices:
                if device['hostname'] == device_name:
                    my_device = device
                    break
            all_commands = ['show ip int br']

            # decrypt password
            my_device['data']['password'] = self.decrypt_password(
                my_device['data']['password'])
            my_device['data']['secret'] = self.decrypt_password(
                my_device['data']['secret'])

            try:
                # getting output
                self.thread = QThread()
                # Step 3: Create a worker object
                self.worker = ConnectionWithThreading(my_device, all_commands)
                # Step 4: Move worker to the thread
                self.worker.moveToThread(self.thread)
                # Step 5: Connect signals and slots
                self.thread.started.connect(self.worker.run)
                self.worker.finished_signal.connect(self.thread.quit)
                self.worker.finished_signal.connect(self.worker.deleteLater)
                self.worker.error_signal.connect(self.show_rip_errors)
                # rps -> routing protocols
                self.worker.output_signal.connect(self.genereate_rip_config)
                # Step 6: Start the thread
                self.thread.start()
                time.sleep(3)
            except Exception as error:
                QMessageBox.critical(self, "Warning", str(error))

    def write_config(self, device, configuration, output_box):
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = WC(device, configuration)
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.worker.finished_signal.connect(self.thread.quit)
        self.worker.finished_signal.connect(self.worker.deleteLater)
        self.thread.started.connect(self.worker.run)
        self.worker.error_signal.connect(self.show_errors)
        output_box.insertPlainText("\n\n---------Output-----------\n\n")
        self.worker.output_signal.connect(output_box.insertPlainText)
        # Step 6: Start the thread
        self.thread.start()
        return

    def clear_rip_results(self):
        self.chkbox_rip_directly.setChecked(False)
        self.chkbox_rip_loopback.setChecked(False)
        self.chkbox_rip_version.setChecked(False)
        self.te_rip_config.clear()

    def configure_rip(self):
        configurations = self.te_rip_config.toPlainText().splitlines()
        if configurations:
            print(configurations)
            # get the name of device and send the config
            device_name = self.configs_all_devices.currentText()
            all_devices = self.convert_host_file_into_list()
            my_device = {}
            for device in all_devices:
                if device['hostname'] == device_name:
                    my_device = device
                    break
            selection = QMessageBox.question(
                self,
                "Alert",
                "Do you want to apply configurations",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if selection == QMessageBox.Yes:
                my_device['data']['password'] = self.decrypt_password(
                    my_device['data']['password'])
                my_device['data']['secret'] = self.decrypt_password(
                    my_device['data']['secret'])
                self.write_config(my_device, configurations,
                                  self.te_rip_config)
                return
            else:
                return

    # 00000000000000000000000000 EIGRP 000000000000000000000000000000000
    def get_valid_as_no(self, widget):
        # check autonomous system number
        regexp = QRegExp(
            r"^()([1-9]|[1-5]?[0-9]{2,4}|6[1-4][0-9]{3}|65[1-4][0-9]{2}|655[1-2][0-9]|6553[1-5])$")
        validator = QRegExpValidator(regexp)
        widget.setValidator(validator)

    def genereate_eigrp_config(self, output):

        networks = list()
        if self.chkbox_eigrp_loopback.isChecked() == True:
            for line in output.splitlines():
                regex = re.compile(
                    r"^(G|E|F|L)[\w\/]+\s+(?P<ip_address>[\d.]+)\s+YES.+up\s+up.*")
                result = re.fullmatch(regex, line)
                if result:
                    # print(result)
                    networks.append(result.group("ip_address"))
        else:
            for line in output.splitlines():
                regex = re.compile(
                    r"^(G|E|F)[\w\/]+\s+(?P<ip_address>[\d.]+)\s+YES.+up\s+up.*")
                result = re.fullmatch(regex, line)
                if result:
                    # print(result)
                    networks.append(result.group("ip_address"))
        if networks:
            as_sys_no = self.txt_eigrp_as_number.text()
            print(networks)

            eigrp_dict = {
                "as_sys_no": as_sys_no,
                "networks": networks,
            }
            j2_env = Environment(
                loader=FileSystemLoader("hosts/templates/configurations"), trim_blocks=True, autoescape=True
            )
            template = j2_env.get_template("cisco_ios_eigrp.j2")
            configuration = template.render(data=eigrp_dict)
            if configuration:
                print(configuration)
                self.te_eigrp_config.clear()
                self.te_eigrp_config.insertPlainText(str(configuration))
                return
            else:
                QMessageBox.critical(
                    self, "Warning", "Configuration generation failed")
                return

    def clear_eigrp_results(self):
        self.txt_eigrp_as_number.setText("")
        self.chkbox_eigrp_directly.setChecked(False)
        self.chkbox_eigrp_loopback.setChecked(False)
        self.te_eigrp_config.clear()
        self.txt_eigrp_as_number.setFocus()

    def show_eigrp_errors(self, error):
        QMessageBox.critical(self, "Warning", error)
        self.clear_eigrp_results()
        return

    def create_eigrp_configuration(self):
        if (not self.chkbox_eigrp_loopback.isChecked() == True) and (not self.chkbox_eigrp_directly.isChecked() == True):
            self.te_eigrp_config.clear()

        if self.chkbox_eigrp_loopback.isChecked() == True or self.chkbox_eigrp_directly.isChecked() == True:
            # check for autonomous system number
            if not self.txt_eigrp_as_number.text():
                self.te_eigrp_config.clear()
                if self.chkbox_eigrp_directly.isChecked() == True:
                    self.chkbox_eigrp_directly.setChecked(False)
                elif self.chkbox_eigrp_loopback.isChecked() == True:
                    self.chkbox_eigrp_loopback.setChecked(False)
                QMessageBox.critical(
                    self, "Warning", "Please enter the autonomous system number")
                self.te_eigrp_config.clear()
                self.txt_eigrp_as_number.setFocus()
                return

            device_name = self.configs_all_devices.currentText()
            all_devices = self.convert_host_file_into_list()
            my_device = {}
            for device in all_devices:
                if device['hostname'] == device_name:
                    my_device = device
                    break
            all_commands = ['show ip int br']

            # decrypt password
            my_device['data']['password'] = self.decrypt_password(
                my_device['data']['password'])
            my_device['data']['secret'] = self.decrypt_password(
                my_device['data']['secret'])

            try:
                # getting output
                self.thread = QThread()
                # Step 3: Create a worker object
                self.worker = ConnectionWithThreading(my_device, all_commands)
                # Step 4: Move worker to the thread
                self.worker.moveToThread(self.thread)
                # Step 5: Connect signals and slots
                self.thread.started.connect(self.worker.run)
                self.worker.finished_signal.connect(self.thread.quit)
                self.worker.finished_signal.connect(self.worker.deleteLater)
                self.worker.error_signal.connect(self.show_eigrp_errors)
                # rps -> routing protocols
                self.worker.output_signal.connect(self.genereate_eigrp_config)
                # Step 6: Start the thread
                self.thread.start()
                time.sleep(3)
            except Exception as error:
                QMessageBox.critical(self, "Warning", str(error))

    def configure_eigrp(self):
        configurations = self.te_eigrp_config.toPlainText().splitlines()
        if configurations:
            print(configurations)
            # get the name of device and send the config
            device_name = self.configs_all_devices.currentText()
            all_devices = self.convert_host_file_into_list()
            my_device = {}
            for device in all_devices:
                if device['hostname'] == device_name:
                    my_device = device
                    break
            selection = QMessageBox.question(
                self,
                "Alert",
                "Do you want to apply configurations",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if selection == QMessageBox.Yes:
                my_device['data']['password'] = self.decrypt_password(
                    my_device['data']['password'])
                my_device['data']['secret'] = self.decrypt_password(
                    my_device['data']['secret'])
                self.write_config(my_device, configurations,
                                  self.te_eigrp_config)
                return
            else:
                return

    # 00000000000000000000000000 OSPF Section 000000000000000000000000000000000
    def get_valid_area_no(self, widget):
        # check autonomous system number
        regexp = QRegExp(
            r"^()([1-9]|[1-5]?[0-9]{2,4}|6[1-4][0-9]{3}|65[1-4][0-9]{2}|655[1-2][0-9]|6553[1-5])$")
        validator = QRegExpValidator(regexp)
        widget.setValidator(validator)

    def genereate_ospf_config(self, output):

        networks = list()
        if self.chkbox_ospf_loopback.isChecked() == True:
            for line in output.splitlines():
                regex = re.compile(
                    r"^(G|E|F|L)[\w\/]+\s+(?P<ip_address>[\d.]+)\s+YES.+up\s+up.*")
                result = re.fullmatch(regex, line)
                if result:
                    # print(result)
                    networks.append(result.group("ip_address"))
        else:
            for line in output.splitlines():
                regex = re.compile(
                    r"^(G|E|F)[\w\/]+\s+(?P<ip_address>[\d.]+)\s+YES.+up\s+up.*")
                result = re.fullmatch(regex, line)
                if result:
                    # print(result)
                    networks.append(result.group("ip_address"))
        if networks:
            process_id = self.txt_process_id.text()
            area_number = self.txt_ospf_area.text()
            print(networks)

            ospf_dict = {
                "process_id": process_id,
                "networks": networks,
                "area_number": area_number,
            }
            j2_env = Environment(
                loader=FileSystemLoader("hosts/templates/configurations"), trim_blocks=True, autoescape=True
            )
            template = j2_env.get_template("cisco_ios_ospf_single_area.j2")
            configuration = template.render(data=ospf_dict)
            if configuration:
                print(configuration)
                self.te_ospf_config.clear()
                self.te_ospf_config.insertPlainText(str(configuration))
                return
            else:
                QMessageBox.critical(
                    self, "Warning", "Configuration generation failed")
                return

    def clear_ospf_results(self):
        self.txt_process_id.setText("")
        self.txt_ospf_area.setText("")
        self.chkbox_ospf_directly.setChecked(False)
        self.chkbox_ospf_loopback.setChecked(False)
        self.te_ospf_config.clear()
        self.txt_process_id.setFocus()

    def show_ospf_errors(self, error):
        QMessageBox.critical(self, "Warning", error)
        self.clear_ospf_results()
        return

    def create_ospf_configuration(self):

        if (not self.chkbox_ospf_loopback.isChecked() == True) and (not self.chkbox_ospf_directly.isChecked() == True):
            self.te_ospf_config.clear()

        if self.chkbox_ospf_loopback.isChecked() == True or self.chkbox_ospf_directly.isChecked() == True:
            # check for process id and area number
            if (not self.txt_process_id.text()) or (not self.txt_ospf_area.text()):
                self.te_ospf_config.clear()
                if self.chkbox_ospf_directly.isChecked() == True:
                    self.chkbox_ospf_directly.setChecked(False)
                elif self.chkbox_ospf_loopback.isChecked() == True:
                    self.chkbox_ospf_loopback.setChecked(False)
                QMessageBox.critical(
                    self, "Warning", "Please fill both fields")
                self.te_ospf_config.clear()

                if self.txt_process_id.text():
                    self.txt_ospf_area.setFocus()
                elif self.txt_ospf_area.text():
                    self.txt_process_id.setFocus()
                else:
                    self.txt_process_id.setFocus()
                return

            device_name = self.configs_all_devices.currentText()
            all_devices = self.convert_host_file_into_list()
            my_device = {}
            for device in all_devices:
                if device['hostname'] == device_name:
                    my_device = device
                    break
            all_commands = ['show ip int br']

            # decrypt password
            my_device['data']['password'] = self.decrypt_password(
                my_device['data']['password'])
            my_device['data']['secret'] = self.decrypt_password(
                my_device['data']['secret'])

            try:
                # getting output
                self.thread = QThread()
                # Step 3: Create a worker object
                self.worker = ConnectionWithThreading(my_device, all_commands)
                # Step 4: Move worker to the thread
                self.worker.moveToThread(self.thread)
                # Step 5: Connect signals and slots
                self.thread.started.connect(self.worker.run)
                self.worker.finished_signal.connect(self.thread.quit)
                self.worker.finished_signal.connect(self.worker.deleteLater)
                self.worker.error_signal.connect(self.show_ospf_errors)
                # rps -> routing protocols
                self.worker.output_signal.connect(self.genereate_ospf_config)
                # Step 6: Start the thread
                self.thread.start()
                time.sleep(3)
            except Exception as error:
                QMessageBox.critical(self, "Warning", str(error))

    def configure_ospf(self):
        configurations = self.te_ospf_config.toPlainText().splitlines()
        if configurations:
            print(configurations)
            # get the name of device and send the config
            device_name = self.configs_all_devices.currentText()
            all_devices = self.convert_host_file_into_list()
            my_device = {}
            for device in all_devices:
                if device['hostname'] == device_name:
                    my_device = device
                    break
            selection = QMessageBox.question(
                self,
                "Alert",
                "Do you want to apply configurations",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if selection == QMessageBox.Yes:
                my_device['data']['password'] = self.decrypt_password(
                    my_device['data']['password'])
                my_device['data']['secret'] = self.decrypt_password(
                    my_device['data']['secret'])
                self.write_config(my_device, configurations,
                                  self.te_ospf_config)
                return
            else:
                return

    # 00000000000000000000000000 DHCP Server 000000000000000000000000000000000

    def hide_dhcp_server_optional_arguments(self):
        self.dhcp_exclude_start.setVisible(False)
        self.dhcp_exclude_end.setVisible(False)
        self.dhcp_default_gateway.setVisible(False)
        self.dhcp_dns_server.setVisible(False)
        self.dhcp_ip_phone_gateway.setVisible(False)

    def toggle_exclude_range(self, state):
        if state == 2:
            self.dhcp_exclude_start.setVisible(True)
            self.dhcp_exclude_end.setVisible(True)
            self.te_dhcp_server_config.clear()
            self.dhcp_btn_generate.setChecked(False)
        else:
            self.dhcp_exclude_start.setVisible(False)
            self.dhcp_exclude_end.setVisible(False)
            self.te_dhcp_server_config.clear()
            self.dhcp_btn_generate.setChecked(False)

    def toggle_ip_phone_gateway(self, state):
        if state == 2:
            self.dhcp_ip_phone_gateway.setVisible(True)
            self.te_dhcp_server_config.clear()
            self.dhcp_btn_generate.setChecked(False)
        else:
            self.dhcp_ip_phone_gateway.setVisible(False)
            self.te_dhcp_server_config.clear()
            self.dhcp_btn_generate.setChecked(False)

    def toggle_default_gateway(self, state):
        if state == 2:
            self.dhcp_default_gateway.setVisible(True)
            self.te_dhcp_server_config.clear()
            self.dhcp_btn_generate.setChecked(False)
        else:
            self.dhcp_default_gateway.setVisible(False)
            self.te_dhcp_server_config.clear()
            self.dhcp_btn_generate.setChecked(False)

    def toggle_dns_server(self, state):
        if state == 2:
            self.dhcp_dns_server.setVisible(True)
            self.te_dhcp_server_config.clear()
            self.dhcp_btn_generate.setChecked(False)
        else:
            self.dhcp_dns_server.setVisible(False)
            self.te_dhcp_server_config.clear()
            self.dhcp_btn_generate.setChecked(False)

    def genereate_dhcp_server_config(self, state):
        # get the values
        print(state)
        if state:
            pool_name = self.dhcp_pool_name.text()
            network_address = self.dhcp_network_address.text()
            subnet_mask = self.dhcp_subnet_mask.text()

            if not pool_name:
                QMessageBox.critical(
                    self, "Warning", "Please enter the pool name")
                self.dhcp_pool_name.setFocus()
                self.dhcp_btn_generate.setChecked(False)
                return
            elif not network_address:
                QMessageBox.critical(
                    self, "Warning", "Please enter the network address")
                self.dhcp_network_address.setFocus()
                self.dhcp_btn_generate.setChecked(False)
                return
            if not subnet_mask:
                QMessageBox.critical(
                    self, "Warning", "Please enter the subnet mask")
                self.dhcp_subnet_mask.setFocus()
                self.dhcp_btn_generate.setChecked(False)
                return
            default_gateway = "None"
            dns_server = "None"
            ip_phone_gateway = "None"
            start_range = "None"
            end_range = "None"

            if self.chkbox_exclude_range.isChecked():
                start_range = self.dhcp_exclude_start.text()
                end_range = self.dhcp_exclude_end.text()
                if not start_range:
                    QMessageBox.critical(
                        self, "Warning", "Please enter the excluding start address")
                    self.dhcp_btn_generate.setChecked(False)
                    self.dhcp_exclude_start.setFocus()
                    return
                if not end_range:
                    QMessageBox.critical(
                        self, "Warning", "Please enter the excluding end address")
                    self.dhcp_btn_generate.setChecked(False)
                    self.dhcp_exclude_end.setFocus()
                    return

            if self.chkbox_default_gateway.isChecked():
                default_gateway = self.dhcp_default_gateway.text()
                if not default_gateway:
                    QMessageBox.critical(
                        self, "Warning", "Please enter the default gateway")
                    self.dhcp_btn_generate.setChecked(False)
                    self.dhcp_default_gateway.setFocus()
                    return

            if self.chkbox_dns_server.isChecked():
                dns_server = self.dhcp_dns_server.text()
                if not dns_server:
                    QMessageBox.critical(
                        self, "Warning", "Please enter the dns server")
                    self.dhcp_btn_generate.setChecked(False)
                    self.dhcp_dns_server.setFocus()
                    return

            if self.chkbox_ip_phone_gateway.isChecked():
                ip_phone_gateway = self.dhcp_ip_phone_gateway.text()
                if not ip_phone_gateway:
                    QMessageBox.critical(
                        self, "Warning", "Please enter the ip phone gateway")
                    self.dhcp_btn_generate.setChecked(False)
                    self.dhcp_ip_phone_gateway.setFocus()
                    return

            # check for valid ip addresses
            if not self.is_ip_complete(self.dhcp_network_address):
                QMessageBox.critical(
                    self, "Warning", "Please enter valid network address")
                self.dhcp_btn_generate.setChecked(False)
                self.dhcp_network_address.setFocus()
                return

            if not self.is_subnet_mask_complete(self.dhcp_subnet_mask):
                QMessageBox.critical(
                    self, "Warning", "Please enter valid subnet mask")
                self.dhcp_btn_generate.setChecked(False)
                self.dhcp_subnet_mask.setFocus()
                return

            if not self.is_ip_complete(self.dhcp_exclude_start) and self.chkbox_exclude_range.isChecked():
                QMessageBox.critical(
                    self, "Warning", "Please enter valid ip address")
                self.dhcp_btn_generate.setChecked(False)
                self.dhcp_exclude_start.setFocus()
                return
            if not self.is_ip_complete(self.dhcp_exclude_end) and self.chkbox_exclude_range.isChecked():
                QMessageBox.critical(
                    self, "Warning", "Please enter valid ip address")
                self.dhcp_btn_generate.setChecked(False)
                self.dhcp_exclude_end.setFocus()
                return
            if not self.is_ip_complete(self.dhcp_default_gateway) and self.chkbox_default_gateway.isChecked():
                QMessageBox.critical(
                    self, "Warning", "Please enter valid ip address")
                self.dhcp_btn_generate.setChecked(False)
                self.dhcp_default_gateway.setFocus()
                return
            if not self.is_ip_complete(self.dhcp_dns_server) and self.chkbox_dns_server.isChecked():
                QMessageBox.critical(
                    self, "Warning", "Please enter valid ip address")
                self.dhcp_btn_generate.setChecked(False)
                self.dhcp_dns_server.setFocus()
                return
            if not self.is_ip_complete(self.dhcp_ip_phone_gateway) and self.chkbox_ip_phone_gateway.isChecked():
                QMessageBox.critical(
                    self, "Warning", "Please enter valid ip address")
                self.dhcp_btn_generate.setChecked(False)
                self.dhcp_ip_phone_gateway.setFocus()
                return

            enabled_exclude_range = self.chkbox_exclude_range.isChecked()
            enabled_default_gateway = self.chkbox_default_gateway.isChecked()
            enabled_dns_server = self.chkbox_dns_server.isChecked()
            enabled_ip_phone_gateway = self.chkbox_ip_phone_gateway.isChecked()
            dhcp_server_dict = {
                "enabled_exclude_range": enabled_exclude_range,
                "enabled_default_gateway": enabled_default_gateway,
                "enabled_dns_server": enabled_dns_server,
                "enabled_ip_phone_gateway": enabled_ip_phone_gateway,
                "exclude_start": start_range,
                "exclude_end": end_range,
                "pool_name": pool_name,
                "network_address": network_address,
                "subnet_mask": subnet_mask,
                "default_gateway": default_gateway,
                "dns_server": dns_server,
                "ip_phone_gateway": ip_phone_gateway,
            }
            j2_env = Environment(
                loader=FileSystemLoader("hosts/templates/configurations"), trim_blocks=True, autoescape=True
            )
            template = j2_env.get_template("cisco_ios_dhcp_server.j2")
            configuration = template.render(data=dhcp_server_dict)
            if configuration:
                print(configuration)
                self.te_dhcp_server_config.clear()
                self.te_dhcp_server_config.insertPlainText(str(configuration))

        else:
            self.te_dhcp_server_config.clear()
            return

    def configure_dhcp_server(self):
        configurations = self.te_dhcp_server_config.toPlainText().splitlines()
        if configurations:
            print(configurations)
            # get the name of device and send the config
            device_name = self.configs_all_devices.currentText()
            all_devices = self.convert_host_file_into_list()
            my_device = {}
            for device in all_devices:
                if device['hostname'] == device_name:
                    my_device = device
                    break
            selection = QMessageBox.question(
                self,
                "Alert",
                "Do you want to apply configurations",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if selection == QMessageBox.Yes:
                my_device['data']['password'] = self.decrypt_password(
                    my_device['data']['password'])
                my_device['data']['secret'] = self.decrypt_password(
                    my_device['data']['secret'])
                self.write_config(my_device, configurations,
                                  self.te_dhcp_server_config)
                return
            else:
                return
        else:
            QMessageBox.information(
                self, "Note", "Please generate the config first!")
            self.dhcp_pool_name.setFocus()
            return

    def clear_dhcp_server_results(self):
        self.dhcp_pool_name.setText("")
        self.dhcp_network_address.setText("")
        self.dhcp_subnet_mask.setText("")
        self.chkbox_exclude_range.setChecked(False)
        self.chkbox_default_gateway.setChecked(False)
        self.chkbox_dns_server.setChecked(False)
        self.chkbox_ip_phone_gateway.setChecked(False)
        self.dhcp_exclude_start.setText("")
        self.dhcp_exclude_end.setText("")
        self.dhcp_default_gateway.setText("")
        self.dhcp_dns_server.setText("")
        self.dhcp_ip_phone_gateway.setText("")
        self.dhcp_btn_generate.setChecked(False)
        self.te_dhcp_server_config.clear()
        self.dhcp_pool_name.setFocus()
        return

    def configure_dhcp_client(self):
        intf_name = self.dhcp_client_all_interfaces.currentText()
        device_name = self.configs_all_devices.currentText()

        all_devices = self.convert_host_file_into_list()
        my_device = {}
        for device in all_devices:
            if device['hostname'] == device_name:
                my_device = device
                break
        all_commands = ['show ip int br']

        # decrypt password
        my_device['data']['password'] = self.decrypt_password(
            my_device['data']['password'])
        my_device['data']['secret'] = self.decrypt_password(
            my_device['data']['secret'])

        dhcp_client_dict = {
            "intf_name": intf_name,
        }
        j2_env = Environment(
            loader=FileSystemLoader("hosts/templates/configurations"), trim_blocks=True, autoescape=True
        )
        template = j2_env.get_template("cisco_ios_dhcp_client.j2")
        configuration = template.render(data=dhcp_client_dict)
        self.write_config(my_device, configuration.split("\n"),
                          self.te_dhcp_server_config)

