from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from utils.file_transfer import transfer_file
from utils.gns3_to_yaml import parse_gns3_to_yaml
from nornir.core.filter import F

# Initialize Nornir
try:
    nr = InitNornir(config_file="config.yaml")
except Exception as e:
    print(f"Failed to initialize Nornir: {str(e)}")
    exit(1)

source_file = "test/test.gns3"

up_linux = nr.filter(F(name__startswith='up2') & F(platform__eq='linux'))

print(f"Total: {len(up_linux.inventory.hosts.items())}")

if up_linux.inventory.hosts:
    result = up_linux.run(
        task=transfer_file,
        source_file=source_file,
    )

    print_result(result)
    
    # Check if file transfer was successful before parsing
    #transfer_successful = all(not r.failed for r in result.values())

    #if transfer_successful:
        #parse_gns3_to_yaml(dest_file, '192.168.56.176',)
    #else:
        #print("File transfer failed. Skipping JSON to YAML conversion.")
else:
    print("No hosts matched the filter criteria.")
