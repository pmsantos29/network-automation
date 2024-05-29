import json
import yaml

def parse_gns3_to_yaml(gns3_json, host_ip, mec_number):
    try:
        hosts = {}

        for node in gns3_json['topology']['nodes']:
            if 'console' in node and node['console'] is not None:
                platform = None
                port = node['console']
                
                if node['name'].startswith('PC'):
                    platform = 'vpcs'

                elif node['name'].startswith('R'):
                    platform = 'cisco_router'

                elif node['name'].startswith('SW'):
                    platform = 'cisco_switch'

                # Should be used also for Linux routers
                elif node['name'].startswith('Linux'):
                    platform = 'linuxvm'
                    # Extract the port from properties -> options
                    options = node['properties'].get('options', '')
                    # Get the port from the format "telnet:0.0.0.0:5012"
                    port = int(options.split(':')[-1].split(',')[0])

                hostname = node['name'].lower()

                if platform != 'linuxvm':
                    host = {
                        'hostname': host_ip,
                        'port': port,
                        'groups': [platform]
                    }
                else:
                    host = {
                        'hostname': host_ip,
                        'port': port,
                        'groups': [platform],
                        'username': 'ar',
                        'password': 'admredes23'
                    }

                hosts[hostname] = host

        with open(f'{mec_number}_hosts.yaml', 'w') as yaml_file:
            yaml.dump(hosts, yaml_file, default_flow_style=False)

        print("hosts.yaml file has been created successfully.")
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False