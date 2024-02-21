#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 dpa-IT Services GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging
import requests

# Possible improvement: Keep the api token until expiration
def get_api_token(api_key, client_id, client_secret):
    r = requests.post("https://ingest-api.wochit.com/api/v1/oauth/access_token", auth=(client_id, client_secret), headers={"x-api-key": api_key})
                      
    r.raise_for_status()

    return r.json()["token"]

def send_to_wochit(api_key, client_id, client_secret, entry, dry_run=False):
    if dry_run:
        logging.info(f"Dry running api call")
        return

    api_token = get_api_token(api_key, client_id, client_secret)
    
    r = requests.post("https://ingest-api.wochit.com/api/v1/assets", 
        headers={"Authorization": f"Bearer {api_token}", "x-api-key": api_key},
        json={
            "mediaProviderAssetModels": [entry]
        }
    )
    
    logging.info(r.content)
    r.raise_for_status() 
    
    logging.info("Sending to wochit-API done")
    logging.info(r.json())