#Pierric Charbonnier et Simon Goncalves
#Exo1

# Import des modules
import pymongo
from pymongo import MongoClient
import requests
import json
from urllib.parse import urlparse
from datetime import datetime
import config

# Connexion au cluster
cluster=MongoClient("mongodb+srv://"+config.id+"@cluster0.tvafg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#Connexion à la db
db=cluster["bycicle_services"]


# Test

def get_vlille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=%26&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET",url)
    response_json = json.loads(response.text.encode('utf8'))
    for i in response_json["records"]:
        datetimeObj = datetime.strptime(i['record_timestamp'][:19], '%Y-%m-%dT%H:%M:%S')
        i['record_timestamp']= datetimeObj
    return response_json.get("records", [])

collection=db["LilleSingle"]
collection.remove()
result = get_vlille()
collection.insert_many(result)

    
    


def get_vRennes():
    url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=stations_vls&q=%26&rows=3000"
    response = requests.request("GET",url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

collection=db["Rennes"]
collection.remove()
collection.insert_many(get_vRennes())

def get_vParis():
    url="https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=2000&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes&refine.nom_arrondissement_communes=Paris"
    response = requests.request("GET",url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

collection=db["Paris"]
collection.remove()
collection.insert_many(get_vParis())

def get_vLyon():
    url="https://api.jcdecaux.com/vls/v3/stations?apiKey=frifk0jbxfefqqniqez09tw4jvk37wyf823b5j1i&contract=lyon"
    response = requests.request("GET",url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

collection=db["Lyon"]
collection.remove()
collection.insert_many(get_vLyon())

