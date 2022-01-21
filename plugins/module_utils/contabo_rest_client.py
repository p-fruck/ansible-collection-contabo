# -*- coding: utf-8 -*-

import json
import pfruck_contabo
from pfruck_contabo.rest import ApiException
import uuid

API_URL = "https://api.contabo.com"

class ContaboRestClient():
    def __init__(self, module, api):
        self.module = module
        config = pfruck_contabo.Configuration()
        config.host = API_URL
        config.api_key['Authorization'] = module.params.get('api_key')
        config.api_key_prefix['Authorization'] = 'Bearer'
        self.api_instance = api(pfruck_contabo.ApiClient(config))


    def _request(self, endpoint, *args, **kwargs):
        x_request_id = str(uuid.uuid4())
        body = kwargs.get("body")
        try:
            if body:
                del kwargs["body"]
                return endpoint(body, x_request_id, *args, **kwargs)
            else:
                return endpoint(x_request_id, *args, **kwargs)
        except ApiException as e:
            self.module.fail_json(msg=e)

    def format_json(self, response):
        return json.loads(json.dumps(response.to_dict(), default=str))

    def get_kwargs(self, allowed_params: list):
        kwargs = {}
        for key in allowed_params:
            val = self.module.params.get(key)
            if val:
                kwargs[key] = val
        return kwargs

    def map_kwargs(self, allowed_params_map: dict):
        kwargs = {}
        for key, mapped_key in allowed_params_map.items():
            val = self.module.params.get(key)
            if val:
                kwargs[mapped_key] = val
        return kwargs
