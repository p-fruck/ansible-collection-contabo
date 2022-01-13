#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pfruck.contabo.plugins.module_utils.contabo_rest_client import ContaboRestClient
from pfruck_contabo import SnapshotsApi, SnapshotResponse

DOCUMENTATION = r"""
---
module: snapshot

short_description: Manage snapshots for a given instance

description:
    - Create, update or delete a snapshot by its name.

version_added: "1.0.0"

author: "Philipp Fruck (@p-fruck)"

options:
    api_key:
        description:
            - Bearer authentication token for the Contabo API.
        required: True
        default: None
    instance_id:
        description:
            - ID of the Contabo compute instance.
        required: True
        default: None
    snapshot_id:
        description:
            - ID of the compute instance snapshot.
        required: False
        default: None
    name:
        description:
            - Name of the compute instance snapshot.
        required: True
        default: None
    description:
        description:
            - Description of the compute instance snapshot.
            - The description is currently not shown in the Contabo web interface.
        required: False
        default: None
    state:
        description:
            - Desirated state of the snapshot.
        required: False
        default: present
        choices:
            - present
            - absent

requirements:
    - pfruck-contabo >= 1.0.0
"""

class ContaboSnapshot(ContaboRestClient):
    def __init__(self, module):
        super(ContaboSnapshot, self).__init__(module, SnapshotsApi)

    def create_snapshot(self):
        instance_id = self.module.params.get("instance_id")
        body = self.get_kwargs(["name", "description"])
        api_response = self._request(self.api_instance.create_snapshot, instance_id, body=body)
        return self.format_json(api_response)

    def delete_snapshot(self, snapshot_id: str) -> None:
        instance_id = self.module.params.get("instance_id")
        self._request(self.api_instance.delete_snapshot, instance_id, snapshot_id)

    def get_snapshot_by_name(self) -> SnapshotResponse | None:
        instance_id = self.module.params.get("instance_id")
        kwargs = self.get_kwargs(["name"])
        kwargs["order_by"] = "name:asc",
        api_response = self._request(self.api_instance.retrieve_snapshot_list, instance_id, **kwargs)
        if api_response.data and api_response.data[0].name.lower() == kwargs["name"].lower():
            return api_response.data[0]
        return None

    def get_snapshot_id(self) -> int | None:
        if "snapshot_id" in self.module.params:
            return self.module.params["snapshot_id"]

        snapshot = self.get_snapshot_by_name()
        if snapshot:
            return snapshot.snapshot_id

    def update_snapshot(self, snapshot_id: str) -> None:
        instance_id = self.module.params.get("instance_id")
        body = self.get_kwargs(["name", "description"])
        self._request(self.api_instance.update_snapshot, instance_id, snapshot_id, body=body)

def argspec():
    return {
        "api_key": {"type": "str", "required": True, "no_log": True},
        "instance_id": {"type": "int", "required": True},
        "snapshot_id": {"type": "str", "required": False},
        "name": {"type": "str", "required": True},
        "description": {"type": "str"},
        "state": {
            "type": "str",
            "choices": ["present", "absent"],
            "default": "present",
        },
    }

def main():
    module = AnsibleModule(argument_spec=argspec(), supports_check_mode=False)
    cntb_mgr = ContaboSnapshot(module)

    snapshot_id = cntb_mgr.get_snapshot_id()
    state = module.params.get("state")
    data = None

    if (state == "absent" and snapshot_id):
        cntb_mgr.delete_snapshot(snapshot_id)
    elif (state == "present"):
        if snapshot_id:
            cntb_mgr.update_snapshot(snapshot_id)
        else:
            data = cntb_mgr.create_snapshot()

    module.exit_json(data=data)

if __name__ == '__main__':
    main()
