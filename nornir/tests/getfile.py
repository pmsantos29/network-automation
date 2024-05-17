from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
import json
import os

def retrieve_file(task):
    # Run the cat command remotely
    result = task.run(
        task=netmiko_send_command,
        command_string="cat /home/ar/GNS3/projects/test/test.gns3",
    )
    # Extract the command output
    output = result[0].result

    try:
        # Attempt to parse JSON
        output_json = json.loads(output)

        # Define file path
        file_path = f"/home/ar/Diss_Network/nornir/{task.host.name}_file.json"

        # Save the JSON to a file
        with open(file_path, "w") as f:
            json.dump(output_json, f, indent=4)
        print("File successfully created:", file_path)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        print("Problematic Output:", output)  # Log problematic output
    except Exception as e:
        print("Error:", e)

# Initialize Nornir with the inventory files
nr = InitNornir(config_file="config.yaml")

target_host = "target"  # Replace with the hostname of the target host

# Filter the hosts to include only the target host
target_hosts = nr.filter(name=target_host)

# Run the retrieve_file task on the target hosts
result = target_hosts.run(task=retrieve_file)

# Print the result
print_result(result)
