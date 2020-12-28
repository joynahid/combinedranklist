import os
import asyncio
import json
from robots.provider.db import db, ds

ref = db.collection('contests')

def vj_stands_from_db(contests):
    doc = ref.document('available_contests').get().to_dict()

    mp = {}

    if doc is None: return ([], contests)
    
    for key in doc:
        mp[key] = 1

    not_found = []
    data = []

    for indx in range(len(contests)):
        i = contests[indx]

        if i in mp:
            filename = "/vjudge/contests/" + i + ".json"
            blob = ds.blob(filename)
            doc = json.loads(blob.download_as_string())
            data.append(doc)
        else: not_found.append(indx)
    
    return (data, not_found)

async def vj_stands_saveto_db(contest_name, res):
    filename = "/vjudge/contests/" + contest_name + ".json"
    blob = ds.blob(filename)
    blob.upload_from_string(json.dumps(res))

    url = blob.public_url

    ref.document("available_contests").update({
        str(contest_name) : url
    })