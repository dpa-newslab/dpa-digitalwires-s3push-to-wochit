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

import arrow
import jmespath

def jmespath_search(entry, path):
    result = jmespath.search(path, entry)
    return result[0] if result is not None and len(result) == 1 else result

def map_dw_language(lang):
    languages = {
        "de": "GERMAN",
        "en": "ENGLISH"
    }

    return languages.get(lang)

def get_collection(entry):
    return next((c for c in entry["categories"] if c["qcode"] in ["dpasrv:video-digital-raw", "dpasrv:video-digital-rtp"]), {}).get("qcode")

def convert_to_wochit_format(dw_entry):
    return {
        "id": dw_entry["urn"],
        "downloadUrl": jmespath_search(dw_entry,"associations[?type=='video'].renditions | [0][?role=='raw'].url"),
        "posterUrl": jmespath_search(dw_entry, "associations[?type=='video'].renditions | [0][?role=='poster'].url"),
        "type": "VIDEO",
        "title": dw_entry["headline"],
        "caption": jmespath_search(dw_entry, "associations[?type=='video'].caption"),
        "publicationDate": arrow.get(dw_entry.get("version_created")).to("utc").format("YYYY-MM-DDTHH:mm:ss[Z]"),
        "contentType": "Editorial",
        "transcript": jmespath_search(dw_entry, "associations[?type=='video'].transcript"),
        "keywords": jmespath_search(dw_entry, "categories[?contains(type, 'dnltype:keyword')].name"),
        "appearingPeople": [],
        "restrictions": None,
        "attribution": "dpa",
        "takenByArtist": None,
        "collection": get_collection(dw_entry),
        "language": map_dw_language(jmespath_search(dw_entry, "language || `de`")),
        "credits": dw_entry.get("creditline", "dpa"),
        "expirationDate": None
    }
