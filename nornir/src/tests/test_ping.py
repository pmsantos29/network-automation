from modules.ping import PingLibrary

ping_lib = PingLibrary()

# Perform ping for a hostname
ping_results = ping_lib.ping("r1", "sw1")
print("Ping Results:", ping_results.result)
