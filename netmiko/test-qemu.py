from netmiko import ConnectHandler, ReadTimeout, NetmikoTimeoutException, NetmikoAuthenticationException

# Define the connection parameters
connection_params = {
    'device_type': 'generic_termserver_telnet',
    'ip': '192.168.56.176',
    'port': 5009,
    'username': 'ar',
    'password': 'admredes23',
    'global_delay_factor': 2,
}

# Establish the connection
net_connect = ConnectHandler(**connection_params)
out = net_connect.send_command('cat text.txt')

# Print the output
print(out)
