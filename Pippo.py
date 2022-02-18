import asyncio
from collections import defaultdict
from bson.objectid import ObjectId
import motor
import motor.motor_asyncio
from asyncio.windows_events import NULL
from typing import DefaultDict, List
import pymongo
from enum import Enum
import bson

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://gabboUser:gabbopsw@cluster0.4ln68.mongodb.net/dbpippo?retryWrites=true&w=majority")
db = client["pippodb"]
pippoCol=db["pippo"]
parCol=db["parentela"]

class parentela:
    def __init__(self,main_object_id,chain):
        self.main_object_id=main_object_id
        self.chain=chain

class chain_obj:
    def __init__(self,id_chain,type_name):
        self.id_chain=id_chain
        self.type_name=FamilyType(type_name)

class FamilyType(Enum):
    Selected=0
    Father=1
    Son=2

c=[{0,"Selected"},{1,"Father"},{2,"Son"}]

async def GetFamily(idPippo):
    lsp= db.pippo.aggregate([
        {
            "$graphLookup":{
                'from': 'pippo',
                'startWith': '$ID',
                'connectFromField': 'ID',
                'connectToField': 'IDChain',
                'restrictSearchWithMatch': { "ID" : idPippo },
                'as': 'chain'
            }
         }
        ])
    #pippoobj=pippoCol.find_one({'_id': ObjectId('620f56842c357ed1ca5c7830')})
    lst=parentela(ObjectId(idPippo),[])
    async for x in lsp:
        idP=str(x.get("_id"))
        idChain=x.get("IDChain")
        if not idChain:
            #p=chain(None,c[1])
            p=chain_obj(None,FamilyType(1))
            lst.chain.append(p)
        else:
            if idP==idPippo:
                p=chain_obj(idChain,FamilyType(0))
                lst.chain.append(p)
            else:
                if idChain==idPippo:
                    p=chain_obj(idP,FamilyType(2))
                    lst.chain.append(p)
            #if x.get("")
    for x in lst.chain:
        print(x.type_name.name)
    pipposDict=defaultdict(list)
    for i in lst.chain:
        if i.id_chain!=None:
            pipposDict[i.id_chain].append(i.type_name.name)
        else:
            pipposDict["0"].append(i.type_name.name)
    family=parentela(lst.main_object_id,pipposDict)
    a=bson.BSON.encode(family.__dict__)
    result = await parCol.insert_one(family.__dict__)
    return lst    

asyncio.get_event_loop().run_until_complete(GetFamily("620f56842c357ed1ca5c7830"))
#asyncio.run(GetFamily())

