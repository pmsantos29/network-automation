from nornir.core.task import Task, Result
from nornir_netmiko.tasks import netmiko_file_transfer
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
import json
import yaml
import os

def transfer_file(task: Task, source_file: str, dest_file: str):    
    try:
        # If the file exists, proceed with the transfer
        result = task.run(
            task=netmiko_file_transfer,
            source_file=source_file,
            dest_file=dest_file,
            direction='get',  # Change direction to 'get' to transfer from remote to local
            file_system='/home/ar'
        )

        return Result(
            host=task.host,
            result=f"File {source_file} transferred to {dest_file}",
            changed=True
        )
    except Exception as e:
        return Result(
            host=task.host,
            result=f"Failed to transfer file {source_file} to {dest_file}: {str(e)}",
            failed=True
        )

def parse_gns3_to_yaml(input_path):
    try:
        with open(input_path, 'r') as json_file:
            data = json.load(json_file)

        hosts = {}

        for node in data['topology']['nodes']:
            if 'console' in node and node['console'] is not None:
                platform = None
                if node['name'].startswith('PC'):
                    platform = 'vpcs'
                elif node['name'].startswith('R'):
                    platform = 'cisco_router'
                elif node['name'].startswith('SW'):
                    platform = 'cisco_switch'
                elif node['name'].startswith('LinuxVM'):
                    platform = 'linuxvm'
                
                hosts[node['name'].lower()] = {
                    'hostname': node['name'].lower(),
                    'port': node['console']        
                }

                if platform:
                    hosts[node['name'].lower()]['platform'] = platform

        with open('hosts.yaml', 'w') as yaml_file:
            yaml.dump(hosts, yaml_file, default_flow_style=False)

        print("hosts.yaml file has been created successfully.")
        return True
    except FileNotFoundError:
        print(f"Error: The file {input_path} was not found.")
        return False
    except json.JSONDecodeError:
        print(f"Error: The file {input_path} is not a valid JSON file.")
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

# Initialize Nornir
try:
    nr = InitNornir(config_file="config.yaml")
except Exception as e:
    print(f"Failed to initialize Nornir: {str(e)}")
    exit(1)

dest_file = "output.gns3"
source_file = "GNS3/projects/test/test.gns3"

filtered_hosts = nr.filter(name="target")

if filtered_hosts.inventory.hosts:
    result = filtered_hosts.run(
        task=transfer_file,
        source_file=source_file,
        dest_file=dest_file
    )
    print_result(result)
    
    # Check if file transfer was successful before parsing
    transfer_successful = all(not r.failed for r in result.values())

    if transfer_successful:
        parse_gns3_to_yaml(dest_file)
    else:
        print("File transfer failed. Skipping JSON to YAML conversion.")
else:
    print("No hosts matched the filter criteria.")
