# Import des modules
import pymongo
from pymongo import MongoClient
import requests
import json
import pprint
import time
import config

# Connexion au cluster
cluster=MongoClient("mongodb+srv://"+config.id+"@cluster0.tvafg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#Connexion à la db
db=cluster["bycicle_services"]
collection = db["LilleSingle"] #collection with single data for each station

#Find a station with some letters and case insensitive
def findaStation(recherche):
    result = collection.find({"fields.nom":{"$regex": recherche, "$options":'i'}})
    return result

findaStation("treiLLE") #will print the N.D. DE LA TREILLE station

# Update a station
def update(station):
    collection.update_one(
        {"fields.nom":station},
        {'$set': {'fields.etat':'HORS SERVICE'}} # passe l'etat de la station a hors service
    )

#update("N.D. DE LA TREILLE")
# Remove station and data
def remove(station):
    query={"fields.nom":station}
    collection.delete_one(query)

#remove("N.D. DE LA TREILLE")

def deactivate(): #put stations around a polygon in state : HORS SERVICE
    result = collection.find({"geometry": { 
    "$near" : {
        "$geometry": {
            "type": "Polygon",
            "coordinates":[ 3.0629778380918538 ,50.64105303104528]
            },
        "$maxDistance": 300,
        "$minDistance": 0
}
}})
    for i in result:
        update(i["fields"]["nom"])
        

deactivate()

def ratiobike():
    collection = db["Lille"] #change collection to db with historical data of around 10 minutes
    result = collection.aggregate([{ #return a cursor that give all stations with a ratio bike/total_stand under 20% for the 10 minutes
   "$group":{ 
       "_id": {"name":"$fields.nom","hourofday": { "$hour": "$record_timestamp" },"totalplace":{"$sum":["$fields.nbvelosdispo","$fields.nbplacesdispo"]}},
       "bike":{"$avg":"$fields.nbvelosdispo"},
   },
   },
   {"$project" : {"_id":1, "ratio": { "$cond": [ { "$eq": [ "$_id.totalplace", 0 ] }, "N/A", {"$divide":["$bike","$_id.totalplace"]}]}}},
   { "$match": { "ratio" : { "$lt": 0.2 }}},

   ])

    
    return result

for i in ratiobike():
    print(i)