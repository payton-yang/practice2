import json

import requests


class BCModel:
    def __init__(self):
        self.endpoint = 'https://api.bigcommerce.com/stores/1i6zpxpe3g'
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Auth-Token": 'h119c0mn6qc8xly25rrkrbb3tbyl8cm'
        }

    def get_method(self, uri, param: dict):
        url = f'{self.endpoint}{uri}'
        resp = requests.get(url, param, headers=self.headers)
        if resp.status_code == 200:
            result = resp.json()
        else:
            result = False
        return result

    def post_method(self, uri, data):
        url = f'{self.endpoint}{uri}'
        resp = requests.post(url, data=json.dumps(data), headers=self.headers)
        if resp.status_code == 200:
            result = resp.json()
        else:
            result = False
        return result

    def put_method(self, uri, data):
        url = f'{self.endpoint}{uri}'
        resp = requests.put(url, data=json.dumps(data), headers=self.headers)
        if resp.status_code == 200:
            result = resp.json()
        else:
            result = False
        return result

    def delete_method(self):
        pass
