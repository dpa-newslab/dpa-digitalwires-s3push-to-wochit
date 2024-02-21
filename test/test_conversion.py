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

import json, os

from utils.convert import convert_to_wochit_format

def test_conversion():
    for filename in os.listdir("test/input"):
        with open(f"test/input/{filename}") as f:
            dw_entry = json.load(f)

        api_entry = convert_to_wochit_format(dw_entry)

        with open(f"test/output/{filename}", "w") as f:
            json.dump(api_entry, f)