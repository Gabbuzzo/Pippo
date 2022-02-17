import asyncio
import pymongo

client = pymongo.MongoClient("mongodb+srv://gabboUser:gabbopsw@cluster0.4ln68.mongodb.net/dbpippo?retryWrites=true&w=majority")
db = client["dbpippo"]
pippoCol=db["Pippo"]
class Pippo():
    def __init__(self,id,idChain):
        self.id=id
        self.idChain=idChain
    

async def GetFamily(pippo):
    PippoFamily=[]
    queryPippos = { "idChain": pippo.id }
    ppsns=pippoCol.find(queryPippos)
    for x in ppsns:
        PippoFamily.append(Pippo(x.get('_id'),x.get('idChain')))
    queryPippos = { "idChain": pippo.idChain }
    ppfth=pippoCol.find_one(queryPippos)
    PippoFamily.append(Pippo(ppfth.get('_id'),ppfth.get('idChain')))
    return PippoFamily

asyncio.run(GetFamily(Pippo('620d427d741cf19625508a42','620d425c741cf19625508a40')))
    