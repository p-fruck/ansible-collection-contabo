#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import json
import pfruck_contabo
from pfruck_contabo.rest import ApiException
import uuid

API_URL = "https://api.contabo.com"

class ContaboInstanceInfo():
    def __init__(self, module):
        self.module = module
        config = pfruck_contabo.Configuration()
        config.host = API_URL
        print(module.params.get('api_key'))
        config.api_key['Authorization'] = module.params.get('api_key')
        config.api_key_prefix['Authorization'] = 'Bearer'
        self.api_instance = pfruck_contabo.InstancesApi(pfruck_contabo.ApiClient(config))

    def get_instances(self):
        x_request_id = str(uuid.uuid4())
        return self.api_instance.retrieve_instances_list(x_request_id)


def argspec():
    return {
        "api_key": {"type": "str", "required": True},
    }

def main():
    module = AnsibleModule(argument_spec=argspec(), supports_check_mode=False)
    contabo_instance_mgr = ContaboInstanceInfo(module)
    try:
        api_response = contabo_instance_mgr.get_instances()
        instances = [ instance.to_dict() for instance in api_response.data ]
        module.exit_json(msg=json.loads(json.dumps(instances, default=str)))
    except ApiException as e:
        module.fail_json(msg=e)

if __name__ == '__main__':
    main()
