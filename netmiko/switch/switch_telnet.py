from pprint import pprint
import json
import yaml
import csv
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

# sends a set of commands to a specific device and returns the output from the device to each command
def send_to_device(device, commands):
    try:
        net_connect = ConnectHandler(**device)

        #iniliatliza empty JSON object
        json_obj = {}

        for command in commands:
            temp = {}

            #send commands and save the output
            temp[command] = net_connect.send_command(command, use_textfsm=True)

            #add the output from the device to the json object
            json_obj.update(temp)

        return json_obj

    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)

#load the devices specifications from the devices.csv file
def load_devices(csv_file):
    devices_array = []

    with open(csv_file, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        for rows in csvReader:
            devices_array.append(rows)

    return devices_array

#load commands from the commands file
def load_commands(commands_file):
    commands_array = []

    with open(commands_file, 'r') as cmds:
        commands_array = cmds.readlines()

    return commands_array

if __name__ == "__main__":
    result = {}
    devices = load_devices('devices.csv')
    commands = load_commands('commands')

    for device in devices:
        temp = {}

        # create a string which will be the 'key' to access each device output
        string = str(device['host']) + ':' + str(device['port'])
        
        temp[string] = send_to_device(device, commands)
        result.update(temp)

    output = open('output.json', 'w')
    output.write(json.dumps(result, indent = 2))
    output.close()
