from netmiko import ConnectHandler

net_connect = ConnectHandler(
    device_type='generic_telnet',
    ip='localhost',
    username='cisco',
    password='cisco',
    port=5004
)

net_connect.enable()
out = net_connect.send_command('show run')
print(out)
