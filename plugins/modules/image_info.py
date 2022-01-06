#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pfruck.contabo.plugins.module_utils.contabo_rest_client import ContaboRestClient
from pfruck_contabo import ImagesApi

class ContaboImageInfo(ContaboRestClient):
    def __init__(self, module):
        super(ContaboImageInfo, self).__init__(module, ImagesApi)

    def get_images(self):
        kwargs = self.get_kwargs(["name", "order_by"])
        api_response = self._request(self.api_instance.retrieve_image_list, **kwargs)
        return self.format_json(api_response)

def argspec():
    return {
        "api_key": {"type": "str", "required": True, "no_log": True},
        "name": {"type": "str", "required": False},
        "order_by": {"type": "list", "required": False},
    }

def main():
    module = AnsibleModule(argument_spec=argspec(), supports_check_mode=False)
    cntb_mgr = ContaboImageInfo(module)
    data = cntb_mgr.get_images()
    module.exit_json(msg=data)

if __name__ == '__main__':
    main()
