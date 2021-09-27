# Import des modules
import pymongo
from pymongo import MongoClient
import requests
import json
from urllib.parse import urlparse
import pprint
import time

# Connexion au cluster
cluster=MongoClient("mongodb+srv://admin:12345@cluster0.tvafg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#Connexion à la db
db=cluster["bycicle_services"]
collection = db["LilleSingle"] #collection with single data for each station

#Find a station with some letters and case insensitive
def findaStation(recherche):
    result = collection.find({"fields.nom":{"$regex": recherche, "$options":'i'}})
    for i in result:
        print(i)

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
        print(i)

deactivate()

def ratiobike():
    collection = db["Lille"] #change collection to db with hostorical data of around 10 minutes
    result = collection.aggregate([{
   "$group":{ 
       "_id": { "id":"$id","hourofday": { "$hour": "7" } },
       "total":{"$avg":"nbvelosdispo","$avg":"nbplacesdispo"}
   },
   }])
    print(result)

ratiobike()