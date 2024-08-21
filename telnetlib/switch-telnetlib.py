import getpass
import telnetlib
import socket
import time

try:
    tn = telnetlib.Telnet('localhost', 5001, 1)
except socket.timeout:
    print("Connection time out caught.")

#tn.set_debuglevel(1)
tn.write(b"\r\n")
time.sleep(0.1)

tn.write(b"enable\r\n")
time.sleep(0.1)

time.sleep(0.1)

tn.write(b"show int\r\n")
time.sleep(0.1)

tn.write(b"exit\r\n")
time.sleep(0.1)

print(tn.read_until(b"exit").decode('ascii'))
tn.close()
