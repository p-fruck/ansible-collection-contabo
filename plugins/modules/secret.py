#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pfruck.contabo.plugins.module_utils.contabo_rest_client import ContaboRestClient
from pfruck_contabo import SecretsApi

class ContaboSecret(ContaboRestClient):
    def __init__(self, module):
        super(ContaboSecret, self).__init__(module, SecretsApi)

    def create_secret(self):
        body = self.get_kwargs(["name", "value", "type"])
        api_response = self._request(self.api_instance.create_secret, body=body)
        return self.format_json(api_response)

    def delete_secret(self):
        secret_id = self.module.params.get("secret_id")
        api_response = self._request(self.api_instance.delete_secret, secret_id)

    def get_secrets(self):
        kwargs = self.get_kwargs(["name", "type"])
        api_response = self._request(self.api_instance.retrieve_secret_list, **kwargs)
        return api_response

    def update_secret(self, secret_id: int, body: dict):
        api_response = self._request(self.api_instance.update_secret, secret_id, body=body)
        return self.format_json(api_response)

def argspec():
    return {
        "api_key": {"type": "str", "required": True, "no_log": True},
        "secret_id": {"type": "int"},
        "name": {"type": "str"},
        "value": {"type": "str", "no_log": True},
        "type": {
            "type": "str",
            "choices": ["password", "ssh"],        },
        "state": {
            "type": "str",
            "choices": ["present", "absent"],
            "default": "present",
        },
    }

def main():
    module = AnsibleModule(
        argument_spec=argspec(),
        required_one_of=[
            ("secret_id", "value"),
        ],
        required_if=[
            ("state", "present", ("name", "value", "type")),
            ("state", "absent", ("secret_id",), False),
        ],
        supports_check_mode=False,
    )

    cntb_mgr = ContaboSecret(module)
    result = None
    if module.params.get("state") == "present":
        secrets = cntb_mgr.get_secrets()
        if len(secrets.data):
            body = cntb_mgr.get_kwargs(["name", "value"])
            cntb_mgr.update_secret(int(secrets.data[0].secret_id), body)
            result = {**secrets.to_dict(), **body}
        else:
            result = cntb_mgr.create_secret()
    else:
        cntb_mgr.delete_secret()
    module.exit_json(result=result)

if __name__ == "__main__":
    main()
