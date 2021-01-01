from PyQt5.QtWidgets import *
from pprint import pprint
from netmiko import ConnectHandler,NetMikoTimeoutException
class connection(QDialog):

    # craete the connection handler and return
    def create_handler(device):
        device = device['data']
        try:
            net_conn =  connecthandler(**device)
            return net_conn
        except netmikotimeoutexception:
            print("devices in not reachable")
            QMessageBox.information(self,"Note","devices in not reachable")
        except netmikoauthenticationexception:
            print("authentication failure")
            QMessageBox.information(self,"Note","authentication failure")
        except netmikosshexception:
            print("make sure ssh is enabled on device")
            QMessageBox.information(self,"Note","make sure ssh is enabled on device")

    def write_commad_output(command_output):
        with open('logs.txt', 'a') as filehandle:
                filehandle.writelines("%s\n" % line for line in command_output)

    def write_message(message):
        with open("logs.txt",'a') as handler:
            handler.write(message)

    def show_commands():
        devices = read_yaml_file()
        print(f"================= Total = {len(devices)} =================")
        pprint(devices)

        for device in devices:
            message = f"-------------------- {device['hostname']}--------------------\n"
            print(message)

            write_message(message)
            net_conn = create_handler(device['data'])
            if net_conn:
                output = net_conn.send_command("show ip int br",use_textfsm=True)
                write_to_file(output)

                print(f"ALL interfaces")
                print(f"Total Interfaces = {len(output)}")

                for interface in output:
                    print(interface['intf'])


                print(f"ALL up interfaces are")

                up_count = 0
                for interface in output:
                    if interface['status'] == 'up' and interface['proto'] == 'up':
                        print(interface['intf'])
                        up_count += 1

                print(f"Total up = {up_count}")


                print(f"ALL down interfaces are")

                down_count = 0
                for interface in output:
                    if interface['status'] == 'down' or interface['proto'] == 'down':
                        print(interface['intf'])
                        down_count += 1

                print(f"Total down  = {down_count}")


