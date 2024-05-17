from modules.ping import PingLibrary

ping_lib = PingLibrary()

# Perform ping for a hostname
ping_results = ping_lib.ping("rt1", "10.0.0.1")
print("Ping Results:", ping_results.result)
