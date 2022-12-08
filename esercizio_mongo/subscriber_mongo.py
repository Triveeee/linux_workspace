from pymongo import * 
from paho.mqtt.client import *
from random import *
from datetime import *
from time import *
from json import *

#------------------------------------------------
#Dati

topic = 'atlas/mongodb/case'
BROKER_HOST = '80.210.122.173'
PORTA_BROKER = 1883


#-----------------------------------------------
#Conessione al broker

client = Client()
client.connect(BROKER_HOST,PORTA_BROKER)


#-----------------------------------------------
#Conessione ad Atlas

password = 'trive004'
uri = 'mongodb+srv://riccardo:'+ password + '@cluster0.zzvi9yy.mongodb.net/test'
atlas = MongoClient(uri)
db = atlas.cluster0
collection = db.case

#----------------------------------------------
#Funzioni

def findLastIndex():
    id_msg = 1
    res = collection.find_one({'_id': id_msg})
    if(res != None):
        while(res != None):
            id_msg+=1
            res = collection.find_one({'_id': id_msg})
    return(id_msg)

def on_message(client , userdata , msg):
    id_msg = findLastIndex()
    dati_json = msg.payload.decode("utf-8")
    data = {'_id': id_msg , 'payload': loads(dati_json)}
    collection.insert_one(data)

#---------------------------------------------
#CallBack
client.on_message = on_message

#---------------------------------------------
#Main
client.subscribe(topic)
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("stop_subscriber")
