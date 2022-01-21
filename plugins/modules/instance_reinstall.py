#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pfruck.contabo.plugins.module_utils.contabo_rest_client import ContaboRestClient
from pfruck_contabo import InstancesApi

class ContaboInstanceInfo(ContaboRestClient):
    def __init__(self, module):
        super(ContaboInstanceInfo, self).__init__(module, InstancesApi)

    def reinstall_instance(self):
        instance_id = self.module.params.get("instance_id")
        body = self.map_kwargs({ "image_id": "imageId", "user_data": "userData", "root_password_id": "rootPassword", "ssh_key_ids": "sshKeys" })
        api_response = self._request(self.api_instance.reinstall_instance, instance_id, body=body)
        return self.format_json(api_response)

def argspec():
    return {
        "api_key": {"type": "str", "required": True, "no_log": True},
        "instance_id": {"type": "int", "required": True},
        "image_id": {"type": "str", "required": True},
        "root_password_id": {"type": "int"},
        "ssh_key_ids": {"type": "list", "elements": "int"},
        "user_data": {"type": "str", "required": False, "no_log": True},
    }

def main():
    module = AnsibleModule(argument_spec=argspec(), supports_check_mode=False)
    cntb_mgr = ContaboInstanceInfo(module)
    data = cntb_mgr.reinstall_instance()
    module.exit_json(data=data)

if __name__ == '__main__':
    main()
