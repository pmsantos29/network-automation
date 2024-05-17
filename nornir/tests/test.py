from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F

nr = InitNornir(config_file="config.yaml")

# Filter devices based on platform
filtered_hosts = nr.filter(F(name="linux1"))

def send_telnet_commands(task):
    print(f"Sending ...")
    result = task.run(task=netmiko_send_command, command_string="ping 10.0.0.2 -c 2") 
    print(result)

results = filtered_hosts.run(task=send_telnet_commands)
print_result(results)
