#!/usr/bin/env python

import json
import os
import uuid

folders = []
items = []
output = {"folders": folders, "items": items}

def parse_file(path):
    password = None
    uris = []
    fields = []

    lines = [line.strip() for line in open(path).readlines()]
    if ': ' not in lines[0]:
        password = lines[0]
        del lines[0]
    for i, line in enumerate(lines):
        if not line:
            continue
        if ': ' not in line:
            if password:
                print(f"file {path} has a duplicate password or soemthing (line {i})")
                continue
            else:
                password = line
        else:
            k, v = line.split(": ")
            if k.lower() in ('url', 'link', 'site'):
                uris.append({
                    "match": None,
                    "uri": v,
                })
            else:
                fields.append({
                    "name": k,
                    "value": v,
                    "type": 0,
                })
    return password, fields, uris

for dir_name, subdir_list, file_list in os.walk('root'):
    #print(dir_name, subdir_list, file_list)
    if dir_name.startswith('root/'):
        folder_id = str(uuid.uuid4())
        folders.append({"name": dir_name[5:], "id": folder_id})
    else:
        # Gets filed under "No Folder"
        folder_id = None

    for fname in file_list:
        password, fields, uris = parse_file(os.path.join(dir_name, fname))

        if folder_id is None:
            item_name = fname
        else:
            item_name = os.path.join(dir_name[5:], fname)

        items.append({
            "id": str(uuid.uuid4()),
            "organizationId": None,
            "folderId": folder_id,
            "type": 1,
            "name": item_name,
            "notes": None,
            "favorite": False,
            "fields": fields,
            "login": {
                "password": password,
                "totp": None,
                "uris": uris,
            },
            "collectionIds": None,
        })
        
print(json.dumps(output))
