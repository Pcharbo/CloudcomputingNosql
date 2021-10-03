# Import des modules
import pymongo
from pymongo import MongoClient
import requests
import json
from urllib.parse import urlparse
import pprint
import config

# Connexion au cluster
cluster=MongoClient("mongodb+srv://"+config.id+"@cluster0.tvafg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#Connexion à la db
db=cluster["bycicle_services"]
collection = db["LilleSingle"]


result = collection.find({"geometry": { 
    "$near" : {
        "$geometry": {
            "type": "Point",
            "coordinates":[ 3.0629778380918538 ,50.64105303104528]
            },
        "$maxDistance": 300,
        "$minDistance": 0
}
}})

for i in result:
    pprint.pprint(i)
    


