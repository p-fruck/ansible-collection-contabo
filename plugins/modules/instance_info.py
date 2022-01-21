#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pfruck.contabo.plugins.module_utils.contabo_rest_client import ContaboRestClient
from pfruck_contabo import InstancesApi

class ContaboInstanceInfo(ContaboRestClient):
    def __init__(self, module):
        super(ContaboInstanceInfo, self).__init__(module, InstancesApi)

    def get_instance(self, instance_id):
        api_response = self._request(self.api_instance.retrieve_instance, instance_id)
        return self.format_json(api_response)

    def get_instances(self):
        api_response = self._request(self.api_instance.retrieve_instances_list)
        return self.format_json(api_response)

def argspec():
    return {
        "api_key": {"type": "str", "required": True, "no_log": True},
        "instance_id": {"type": "int", "required": False},
    }

def main():
    module = AnsibleModule(argument_spec=argspec(), supports_check_mode=False)
    cntb_mgr = ContaboInstanceInfo(module)
    if module.params.get("instance_id"):
        result = cntb_mgr.get_instance(module.params["instance_id"])
    else:
        result = cntb_mgr.get_instances()
    module.exit_json(result=result)

if __name__ == '__main__':
    main()
