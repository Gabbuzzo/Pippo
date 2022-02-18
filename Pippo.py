import asyncio
from collections import defaultdict
from bson.objectid import ObjectId
import motor
import motor.motor_asyncio
from asyncio.windows_events import NULL
from typing import DefaultDict, List
import pymongo

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://gabboUser:gabbopsw@cluster0.4ln68.mongodb.net/dbpippo?retryWrites=true&w=majority")
db = client["pippodb"]
pippoCol=db["pippo"]
async def GetFamily(idPippo):
    lsp= db.pippo.aggregate([
        {
            "$graphLookup":{
                'from': 'pippo',
                'startWith': '$ID',
                'connectFromField': 'ID',
                'connectToField': 'IDChain',
                #'restrictSearchWithMatch': { "ID" : "1" },
                'as': 'chain'
            }
         }
        ])
    #pippoobj=pippoCol.find_one({'_id': ObjectId('620f56842c357ed1ca5c7830')})
    lst=defaultdict(list)
    async for x in lsp:
        idP=str(x.get("_id"))
        idChain=x.get("IDChain")
        #if idP==pippo.get("IDChain"):
        #    lst[x.get("ID")].append(x.get("IDChain"))
        if idP==idPippo:
            lst[x.get("ID")].append(x.get("IDChain"))
        else:
            if idChain==idPippo:
                lst[x.get("ID")].append(x.get("IDChain"))
            #if x.get("")

    for x in lst.items():
        print(x)
    return lst    

asyncio.get_event_loop().run_until_complete(GetFamily("620f56842c357ed1ca5c7830"))
#asyncio.run(GetFamily())

