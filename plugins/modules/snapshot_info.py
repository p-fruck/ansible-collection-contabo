#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pfruck.contabo.plugins.module_utils.contabo_rest_client import ContaboRestClient
from pfruck_contabo import SnapshotsApi

class ContaboSnapshotInfo(ContaboRestClient):
    def __init__(self, module):
        super(ContaboSnapshotInfo, self).__init__(module, SnapshotsApi)

    def get_snapshots(self):
        instance_id = self.module.params.get("instance_id")
        api_response = self._request(self.api_instance.retrieve_snapshot_list, instance_id)
        return self.format_json(api_response)

def argspec():
    return {
        "api_key": {"type": "str", "required": True, "no_log": True},
        "instance_id": {"type": "int", "required": True},
    }

def main():
    module = AnsibleModule(argument_spec=argspec(), supports_check_mode=False)
    cntb_mgr = ContaboSnapshotInfo(module)
    data = cntb_mgr.get_snapshots()
    module.exit_json(msg=data)

if __name__ == '__main__':
    main()
