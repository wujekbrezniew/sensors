from .sensors import *
import asyncio
import json
import datetime
import pymongo
from websockets.sync.client import connect

w100 = 17300

def send():
    w = (moisture.get()/17300)*100
    print(w)
    try:
        with connect("ws://clinostate.local:8080") as websocket:
            websocket.send(json.dumps({
                "action": "pump",
                "data" : {
                    "type": "cultivation",
                    "value": w,
                }
            }))
    except:
        print("No connection to clinostate backend!")
    
    results = {
        "w": w,
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    
    mongo_client = pymongo.MongoClient("mongodb://golfserver:27017")
    clinostate_db = mongo_client["clinostate"]
    cultivation_col = clinostate_db["watering"]
    try:
        cultivation_col.insert_one(results)
    except:
        print("No connection to mongodb")

