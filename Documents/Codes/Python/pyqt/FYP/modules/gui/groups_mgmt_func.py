from PyQt5.QtWidgets import QDialog, QMessageBox
from netmiko import ConnectHandler
from yaml import safe_load
import yaml
from pprint import pprint
import os



class groups_mgmt_func(QDialog):


    
    def create_groups_dictionary(self):
        return{
            'routers': [],
            'switches': []
        }

    
    def get_groups_file_path(self):
            return os.path.join("hosts","groups.yaml")


    def write_groups_yaml_file(self,hostname,groupname):
        if groupname == 'switch':
            groupname = 'switches'
        if groupname == 'router':
            groupname = 'routers'
        self.check_for_groups_file()
        groups_file = self.get_groups_file_path()
        groups = self.read_yaml_file(groups_file)
        groups[groupname].append(hostname)
        f = open(groups_file,'w')
        yaml.dump(f ,groups, allow_unicode=True)
        
    def check_for_groups_file(self):
        dir_exists = os.path.isdir("hosts")
        if not dir_exists:
            os.mkdir("hosts")
        file = os.path.join("hosts","groups.yaml")
        groups_file_exists = os.path.isfile(file)
        if groups_file_exists:
            print("groups file exists")
            return True
        else:
            print("groups file does not exist")
            # create the empty file
            groups_file = self.create_groups_dictionary()
            f = open(os.path.join("hosts","groups.yaml"),'w') 
            yaml.dump(groups_file,f, allow_unicode=True)
            return False


