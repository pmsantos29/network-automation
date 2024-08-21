import getpass
import telnetlib

HOST = "localhost"
user = input("Enter your remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST, 5030)
tn.set_debuglevel(1)

#tn.write(b"\r\n")

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write(b"systemctl status serial-getty@ttyS0.service\n")
tn.write(b"exit\n")

print(tn.read_all().decode('ascii'))
