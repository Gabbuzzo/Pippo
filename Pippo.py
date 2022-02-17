import asyncio
from asyncio.windows_events import NULL
from collections import defaultdict
from typing import List
import pymongo
baseCollection=[("A0","0"),("A1","A0"),("A2","A0"),("A3","A0"),("A4","A1"),("A5","A1")]
client = pymongo.MongoClient("mongodb+srv://gabboUser:gabbopsw@cluster0.4ln68.mongodb.net/dbpippo?retryWrites=true&w=majority")
db = client["dbpippo"]
pippoCol=db["Pippo"]
class Pippo():
    def __init__(self,idChain,chain):
        self.idChain=idChain
        self.chain=chain
    

async def GetFamily(pippo):
    res = defaultdict(list)
    for child,parent in pippo:
        res[parent].append(child)
    #PippoFamily=[]
    #queryPippos = { "idChain": pippo.id }
    #ppsns=pippoCol.find(queryPippos)
    #for x in ppsns:
    #    PippoFamily.append(Pippo(x.get('_id'),x.get('idChain')))
    #queryPippos = { "idChain": pippo.idChain }
    #ppfth=pippoCol.find_one(queryPippos)
    #PippoFamily.append(Pippo(ppfth.get('_id'),ppfth.get('idChain')))
    return res

#asyncio.run(GetFamily(Pippo('620d427d741cf19625508a42','620d425c741cf19625508a40')))
a=asyncio.run(GetFamily(baseCollection))
print(a)