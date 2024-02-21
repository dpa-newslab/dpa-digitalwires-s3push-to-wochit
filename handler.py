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

import json
import logging
import os 
import random
import string

from os.path import basename
from urllib.parse import urlparse

import boto3
import requests

from utils.convert import convert_to_wochit_format
from utils.api import send_to_wochit

logging.getLogger().setLevel(logging.INFO)

ssm = boto3.client("ssm")
WOCHIT_API_KEY = ssm.get_parameter(Name=os.environ["SSM_WOCHIT_API_KEY"], WithDecryption=True)["Parameter"]["Value"]
WOCHIT_CLIENT_ID = ssm.get_parameter(Name=os.environ["SSM_WOCHIT_CLIENT_ID"], WithDecryption=True)["Parameter"]["Value"]
WOCHIT_CLIENT_SECRET = ssm.get_parameter(Name=os.environ["SSM_WOCHIT_CLIENT_SECRET"], WithDecryption=True)["Parameter"]["Value"]

BUCKET_NAME = os.environ["S3_BUCKET_NAME"]
BUCKET_PREFIX_ASSOCIATIONS = os.environ["S3_BUCKET_PREFIX_ASSOCIATIONS"]
s3 = boto3.client("s3")


def handle(event, context):
    logging.info(event)

    records = event.get("Records", [])
    logging.info(f"Received {len(records)} messages")

    for record in records:
        message = json.loads(record["body"])

        if message.get("Records") is None:
            logging.warn(f"Message has no records: {message}")
            continue 

        bucket = message["Records"][0]["s3"]["bucket"]["name"]
        key = message["Records"][0]["s3"]["object"]["key"]

        logging.info(f"Get {key} from {bucket}")

        obj = s3.get_object(
            Bucket=bucket,
            Key=key
        )

        dw_entry = json.loads(obj["Body"].read().decode("utf-8"))

        # Save associations to s3
        for i, a in enumerate(dw_entry.get("associations", [])):
            for j, rend in enumerate(a.get("renditions", [])):
                if not rend.get("url"):
                    logging.warning("Rendition has no url")
                    continue 

                outfile = basename(urlparse(rend["url"]).path) or ''.join(random.choice(string.ascii_lowercase) for i in range(16))

                r = requests.get(rend["url"], stream=True)
                r.raise_for_status()

                s3.put_object(
                    Bucket=BUCKET_NAME,
                    Key=f"{BUCKET_PREFIX_ASSOCIATIONS}/{outfile}",
                    Body=r.content,
                    ContentType=rend.get("mimetype")
                )

                # Use public s3-URL because wochit api might not accept expiring signed urls
                dw_entry["associations"][i]["renditions"][j]["url"] = f"https://{BUCKET_NAME}.s3.eu-central-1.amazonaws.com/{BUCKET_PREFIX_ASSOCIATIONS}/{outfile}"
                logging.info(f"Saved association to s3 bucket. Key: {BUCKET_PREFIX_ASSOCIATIONS}/{outfile}")


        wochit_entry = convert_to_wochit_format(dw_entry)

        logging.debug("Converting to wochit format done:")
        logging.debug(wochit_entry)
        
        try:
            send_to_wochit(WOCHIT_API_KEY, WOCHIT_CLIENT_ID, WOCHIT_CLIENT_SECRET, wochit_entry, dry_run=False)
        except Exception as e:
            raise e
