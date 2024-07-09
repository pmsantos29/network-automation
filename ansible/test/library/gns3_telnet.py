from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from netmiko import ConnectHandler

class ActionModule:

    def run(self, tmp=None, task_vars=None):
        module_args = dict(
            host=dict(type='str', required=True),
            user=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True),
            port=dict(type='int', default=23),
            timeout=dict(type='int', default=120),
            pause=dict(type='int', default=1),
            commands=dict(type='list', required=True)
        )

        result = dict(
            changed=False,
            failed=False,
            msg='',
            stdout='',
            stdout_lines=[]
        )

        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True,
            gather_facts=False
        )

        host = module.params['host']
        user = module.params['user']
        password = module.params['password']
        port = module.params['port']
        timeout = module.params['timeout'] 
        pause = module.params['pause']
        commands = module.params['commands']

        device = {
            'device_type': 'terminal_server',
            'ip': host,
            'port': port,
            'username': user,
            'password': password,
            'timeout': timeout
        }

        try:
            net_connect = ConnectHandler(**device)
            
            for cmd in commands:
                cmd_response = net_connect.send_command(cmd)
                result['stdout'] += cmd_response
                result['stdout_lines'].append(cmd_response)
                module.log(f"Sent command: {cmd}, Received response: {cmd_response}")
                module.log(f"Sleeping for {pause} seconds")
                net_connect.send_command_timing('sleep ' + str(pause))

            net_connect.disconnect()
            
            result['changed'] = True

        except Exception as e:
            result['failed'] = True
            result['msg'] = f"Netmiko error: {str(e)}"

        module.exit_json(**result)


def main():
    ActionModule().run()


if __name__ == '__main__':
    main()
