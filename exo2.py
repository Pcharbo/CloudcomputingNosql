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
collection = db["Lille"]




def get_vlille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=%26&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET",url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

def refresh(duree): #every 60 seconds store data in db
    time.sleep(duree)
    result = get_vlille()
    collection.insert_many(result)
    print("refresh")

while True:
    refresh(60)

    