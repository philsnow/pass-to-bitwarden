#!/usr/bin/env python

import json
import os
import uuid

folders = []
items = []
output = {"folders": folders, "items": items}

for dir_name, subdir_list, file_list in os.walk('dump'):
    #print(dir_name, subdir_list, file_list)
    if dir_name.startswith("dump/"):
        folder_id = str(uuid.uuid4())
        folders.append({"name": dir_name[5:], "id": folder_id})
    else:
        folder_id = None

    for fname in file_list:
        lines = [line.strip() for line in open(os.path.join(dir_name, fname)).readlines()]
        password = None
        if ': ' not in lines[0]:
            password = lines[0]
            del lines[0]
        fields = []
        for i, line in enumerate(lines):
            if not line:
                continue
            if ': ' not in line:
                if password:
                    print(f"file {os.path.join(dir_name, fname)} has a duplicate password or soemthing (line {i})")
                    continue
                else:
                    password = line
            else:
                k, v = line.split(": ")
                fields.append({
                    "name": k,
                    "value": v,
                    "type": 0,
                })
        items.append({
            "id": str(uuid.uuid4()),
            "organizationId": None,
            "folderId": folder_id,
            "type": 1,
            "name": fname,
            "notes": None,
            "favorite": False,
            "fields": fields,
            "login": {
                "password": password,
                "totp": None,
            },
            "collectionIds": None,
        })
        
print(json.dumps(output))
