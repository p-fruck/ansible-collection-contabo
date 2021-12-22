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
        try:
            return endpoint(x_request_id, *args, **kwargs)
        except ApiException as e:
            self.module.fail_json(msg=e)

    def format_json(self, response):
        if isinstance(response.data, list):
            data = [ item.to_dict() for item in response.data ]
        else:
            data = reponse.data
        return json.loads(json.dumps(data, default=str))
