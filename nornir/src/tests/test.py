from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F

nr = InitNornir(config_file="config.yaml")

filtered_hosts = nr.filter(F(name="r1"))

def send_telnet_commands(task):
    result = task.run(task=netmiko_send_command, command_string="show version") 
    print(result)

results = filtered_hosts.run(task=send_telnet_commands)
print_result(results)
