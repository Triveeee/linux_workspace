from pymongo import * 
from paho.mqtt.client import *
from random import *
from datetime import *
from time import *
from cryptography.fernet import Fernet
import json

#------------------------------------------------
#Dati
chiave = 'fM5t5hPaMlRWtmfpnbaaDAsYJvsDnDE5Ehd_9oYirEg='
topic = 'atlas/mongodb/case'
BROKER_HOST = '80.210.122.173'
PORTA_BROKER = 1883

#----------------------------------------------
#definizione chiave

chiave = 'fM5t5hPaMlRWtmfpnbaaDAsYJvsDnDE5Ehd_9oYirEg='
chiave_valore = Fernet(chiave)

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

def cryptation(message):
    message_byte = message.encode('utf-8')  # <-- trasformazione messaggio in formato utf-8 (in bytes)
    message_cryptated = chiave_valore.encrypt(message_byte) # <--criptazione del messaggio in bytes (viene trasformato in stringa)
    return message_cryptated

def createHome(n_casa):
    minimo = 1
    massimo = 100
    data = datetime.date(datetime.now())
    tempo = datetime.time(datetime.now())
    home = {
        "casa": n_casa,
        "data": str(data),
        "tempo": str(tempo),
        "stanze": [
            {"cucina": {"temperatura": randint(minimo , massimo), "umidita": randint(minimo , massimo)}},
            {"soggiorno": {"temperatura": randint(minimo , massimo), "umidita": randint(minimo , massimo)}},
            {"mansarda": {"temperatura": randint(minimo , massimo), "umidita": randint(minimo , massimo)}},
            {"camera_da_letto": {"temperatura": randint(minimo , massimo), "umidita": randint(minimo , massimo)}}
        ]
    }
    home = json.dumps(home , indent= 4)   # <--- trasformazione in stringa json
    home = cryptation(home) # <---  richiama la funzione cryptation
    return home

#--------------------------------------------
#Main

client.loop_start()
try:
    while True:
        n = randint(1 , 4)
        casa = createHome(n) # < -- casa criptata
        print(casa)
        client.publish(topic, casa)  # < --- invia il messaggio criptato al broker in bytes
        sleep(5)

except KeyboardInterrupt:
    print("Stop publisher")
client.loop_stop()
client.disconnect()
