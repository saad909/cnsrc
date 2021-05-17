from PyQt5.QtWidgets import *
from modules.networking.connection import ConnectionWithThreading
from PyQt5.QtCore import  QThread,Qt
import re,time
from jinja2 import Environment, FileSystemLoader
from modules.networking.connection import WRITE_CONFIG as WC


class configurations(QDialog):
    cmds_output = None


    def fill_configurations(self,device_name):
        # all_devices_list = self.convert_host_file_into_list()
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
                    "dhcp server",
                    "dhcp client",
                    "dhcp snooping",
                ]
                self.configs_all_configurations.addItems(routing_protocols_list)
                self.configs_all_configurations.addItems(dhcp_configurations_list)
                others_list =  [
                "port channeling",
                "----------- OTHER -----------",
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
            QMessageBox.critical(self,"Warning","Software currently supports only cisco_ios devices")
            return


    def move_configs_tab_index(self,config_selected):
        if not "-" in config_selected:
            page = self.tab_configs.findChild(QWidget,config_selected)
            index = self.tab_configs.indexOf(page)
            print(f"INdex is {index}")
            self.tab_configs.setCurrentIndex(index)
        else:
            self.tab_configs.setCurrentIndex(0)
            return


    def genereate_rip_config(self,output):


        networks = list()
        if self.chkbox_rip_loopback.isChecked() == True:
            for line in output.splitlines():
                regex = re.compile(r"^(G|E|F|L)[\w\/]+\s+(?P<ip_address>[\d.]+)\s+YES.+up\s+up.*")
                result = re.fullmatch(regex,line)
                if result:
                    # print(result)
                    networks.append(result.group("ip_address"))
        else:
            for line in output.splitlines():
                regex = re.compile(r"^(G|E|F)[\w\/]+\s+(?P<ip_address>[\d.]+)\s+YES.+up\s+up.*")
                result = re.fullmatch(regex,line)
                if result:
                    # print(result)
                    networks.append(result.group("ip_address"))
        if networks:
            print(networks)
            rip_version = "1"
            if self.chkbox_rip_version.isChecked():
                rip_version = "2"

            rip_dict = {
                "networks":networks,
                "version":rip_version,
            }
            j2_env = Environment(
                loader=FileSystemLoader("hosts/templates/configurations"), trim_blocks=True, autoescape=True
            )
            template = j2_env.get_template("cisco_ios_rip.j2")
            configuration = template.render(data=rip_dict)
            if configuration:
                print(configuration)
                self.te_rip_config.clear()
                self.te_rip_config.insertPlainText(str( configuration ))

            return


    def create_rip_configuration(self):
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
            my_device['data']['password'] = self.decrypt_password(my_device['data']['password'])
            my_device['data']['secret'] = self.decrypt_password(my_device['data']['secret'])


            # if not self.cmds_output:
            try:
                # getting output
                self.thread = QThread()
                # Step 3: Create a worker object
                self.worker = ConnectionWithThreading(my_device,all_commands)
                # Step 4: Move worker to the thread
                self.worker.moveToThread(self.thread)
                # Step 5: Connect signals and slots
                self.thread.started.connect(self.worker.run)
                self.worker.finished_signal.connect(self.thread.quit)
                self.worker.finished_signal.connect(self.worker.deleteLater)
                self.worker.error_signal.connect(self.show_errors)
                # rps -> routing protocols
                self.worker.output_signal.connect(self.genereate_rip_config)
                # Step 6: Start the thread
                self.thread.start()
                time.sleep(3)
            except Exception as error:
                QMessageBox.critical(self,"Warning",str(error))


    def write_config(self,device,configuration):
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = WC(device,configuration)
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.error_signal.connect(self.show_errors)
        self.te_rip_config.insertPlainText("\n\n---------Output-----------\n\n")
        self.worker.output_signal.connect(self.te_rip_config.insertPlainText)
        # Step 6: Start the thread
        self.thread.start()

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
                            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                            QMessageBox.No,
                        )
            if selection == QMessageBox.Yes:
                my_device['data']['password'] = self.decrypt_password(my_device['data']['password'])
                my_device['data']['secret'] = self.decrypt_password(my_device['data']['secret'])
                self.write_config(my_device,configurations)
                return
            else:
                # remove selections and quit
                return



