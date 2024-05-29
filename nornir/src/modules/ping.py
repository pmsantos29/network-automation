from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir.core.filter import F
from .constants import CONFIG_FILE

class PingLibrary:
    def __init__(self):
        self.nr = InitNornir(config_file=CONFIG_FILE)
    
    def ping(self, source, destination):
        # Get the platform group of the source
        platform = self._get_platform(source)

        if platform == "ios_router":
            return self._ping_router(source, destination)
        elif platform == "ios_switch":
            return self._ping_switch(source, destination)
        elif platform == "vpcs":
            return self._ping_vpc(source, destination)
        elif platform == "linux":
            return self._ping_linux(source, destination)
        else:
            return f"Unsupported platform for source {source}"
    
    def _get_platform(self, source):
        # Get the platform group of the source
        host = self.nr.inventory.hosts.get(source)
        if host:
            return str(next(iter(host.groups), None))
        else:
            return None   
                                                                                   
    def _ping_router(self, source, destination):
        return self._send_ping_command(source, destination, "")
    
    def _ping_switch(self, source, destination):
        return self._send_ping_command(source, destination, "")
    
    def _ping_vpc(self, source, destination):
        return self._send_ping_command(source, destination, "-c 2")
    
    def _ping_linux(self, source, destination):
        return self._send_ping_command(source, destination, "-c 2")
    
    def _send_ping_command(self, source, destination, options):
        filter = self.nr.filter(F(name__contains=source))
        results = filter.run(
            task=netmiko_send_command,
            command_string=f"ping {destination} {options}"
        )
        
        return results
