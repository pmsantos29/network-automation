import getpass
import telnetlib
import socket
import time

try:
    tn = telnetlib.Telnet('localhost', 5002, 1)
    #n = telnetlib.Telnet()
    #tn.open('localhost', 5002, 1)
except socket.timeout:
    print("Connection time out caught.")

#tn.set_debuglevel(1)
tn.write(b"\r\n")
time.sleep(0.1)

tn.write(b"enable\r\n")
time.sleep(0.1)

tn.write(b"conf t\r\n")
time.sleep(0.1)

tn.write(b"int f0/0\r\n")
time.sleep(0.1)

tn.write(b"ip addr 192.168.1.1 255.255.255.0\r\n")
time.sleep(0.1)

tn.write(b"no shut\r\n")
time.sleep(0.1)

tn.write(b"!\r\n")

tn.write(b"end\r\n")
time.sleep(0.1)

tn.write(b"show ip int brief\r\n")
time.sleep(0.1)

tn.write(b"exit\r\n")
time.sleep(0.1)

print(tn.read_until(b"exit").decode('ascii'))
tn.close()
