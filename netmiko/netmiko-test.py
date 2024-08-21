from netmiko import ConnectHandler

net_connect = ConnectHandler(
    device_type='generic_telnet',
    ip='192.168.56.176',
    username='ar',
    password='admredes23',
    port=5009,
    global_delay_factor=2

)
out = net_connect.send_command('ping 10.0.0.2 -c 3')
print(out)
