from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
import time

nr = InitNornir(config_file="config.yaml")

# Filter devices based on platform
filtered_hosts = nr.filter(F(name="vpc1"))

def send_telnet_commands(task):
    print(f"Sending ...")

    # Manually create Netmiko connection
    # net_connect = task.host.get_connection("netmiko", task.nornir.config)
    # print()
    # print("#" * 8)

    # output=net_connect.send_command("\r\n")
    # print(net_connect.find_prompt())

    # print("#" * 8)

    # output = net_connect.send_command("admredes23")

    # print(output)
    # print()
    result = task.run(task=netmiko_send_command, command_string="ls") 
    print(result)

results = filtered_hosts.run(task=send_telnet_commands)
print_result(results)
