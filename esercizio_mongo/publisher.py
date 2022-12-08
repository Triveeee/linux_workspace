from pymongo import * 
from paho.mqtt.client import *
from random import *
from datetime import *
from time import *
import json

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

def createHome(n_casa):
    minimo = 1
    massimo = 100
    tempo = datetime.time(datetime.now())
    data = datetime.date(datetime.now())
    home = {
        "casa": n_casa,
        "data": data,
        "tempo": tempo,
        "stanze": [
            {"cucina": {"temperatura": randint(minimo , massimo), "umidita": randint(minimo , massimo)}},
            {"soggiorno": {"temperatura": randint(minimo , massimo), "umidita": randint(minimo , massimo)}},
            {"mansarda": {"temperatura": randint(minimo , massimo), "umidita": randint(minimo , massimo)}},
            {"camera_da_letto": {"temperatura": randint(minimo , massimo), "umidita": randint(minimo , massimo)}}
        ]
    }
    home = json.dumps(home , indent=4)
    return home

#--------------------------------------------
#Main

client.loop_start()

try:
    while True:
        n = randint(1 , 4)
        casa = createHome(n)
        print(casa)
        client.publish(topic, casa)
        sleep(5)

except KeyboardInterrupt:
    print("Stop publisher")
client.loop_stop()
client.disconnect()








