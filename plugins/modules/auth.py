#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import requests

AUTH_URL = "https://auth.contabo.com/auth/realms/contabo/protocol/openid-connect/token"

def argspec():
    return {
        "client_id": {"type": "str", "required": True, "no_log": True},
        "client_secret": {"type": "str", "required": True, "no_log": True},
        "username": {"type": "str", "required": True, "no_log": True},
        "password": {"type": "str", "required": True, "no_log": True},
    }

def main():
    module = AnsibleModule(argument_spec=argspec(), supports_check_mode=False)
    data = module.params
    data["grant_type"] = "password"
    try:
        oauth_response = requests.post(AUTH_URL, data=data)
        if oauth_response.status_code not in [200]:
            module.fail_json(msg=(oauth_response.status_code, oauth_response.content))
        module.exit_json(msg=oauth_response.json())
    except Exception as e:
        module.fail_json(msg=e)

if __name__ == '__main__':
    main()
