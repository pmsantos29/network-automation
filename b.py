from gns3.qt import QtNetwork
import socket
import struct
import fcntl

for interface in QtNetwork.QNetworkInterface.allInterfaces():
    if interface.name() == "ens18":
        for entry in interface.addressEntries():
            print(entry.ip().toString())
            
for i  in socket.if_nameindex():
    print("interface: ", i)
    
# Create a socket to get the IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Get the IP address using ioctl and SIOCGIFADDR
ip_address = socket.inet_ntoa(fcntl.ioctl(
    s.fileno(),
    0x8915,  # SIOCGIFADDR
    struct.pack('256s', "ens18"[:15].encode())
)[20:24])

print(ip_address)
