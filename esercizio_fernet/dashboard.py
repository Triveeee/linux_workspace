from pymongo import * 
from random import *
from datetime import *
from time import *
from json import *
from cryptography.fernet import Fernet
import utils.index as utils
from paho.mqtt.client import *

#------------------------------------------------
#Dati
topic = 'atlas/mongodb/casa'
BROKER_HOST = '80.210.122.173'
PORTA_BROKER = 1883

#-----------------------------------------------
#Conessione al broker

client = Client()
client.connect(BROKER_HOST,PORTA_BROKER)

#---------------------------------------------
# definizione chiave

f = open('key.txt' , 'r')
chiave = f.read()
f.close()
chiave_valore = Fernet(chiave)

#-----------------------------------------------
#Conessione ad Atlas

password = 'trive004'
uri = 'mongodb+srv://riccardo:'+ password + '@cluster0.zzvi9yy.mongodb.net/test'
atlas = MongoClient(uri)
db = atlas.cluster0
collection = db.case

#-----------------------------------------------
# Funzioni_di_callback
def on_message(client , userdata , msg):
    message_cryptated = msg.payload# <--- decodificazione del messaggio inviato dal broher (bytes criptato -> string criptato)
    message_bytes = chiave_valore.decrypt(message_cryptated) # <--- decriptazione del messaggio in bytes (string criptato-> bytes decriptato) 
    message_json = message_bytes.decode("utf-8") # <ms-- decodifica del messaggio decriptato in bytes  (bytes decriptato -> string decriptato)
    message = loads(message_json)   # conversione stringa json a dizionario
    n = message['casa']
    if(n == numero_casa):
        print(message_json)

#---------------------------------------------
#CallBack
client.on_message = on_message

#----------------------------------------------
# Funzioni
# scelta 1 visualizzazione in tempo reale
def stream(n_casa):
    global numero_casa 
    numero_casa = n_casa
    client.subscribe(topic)

    try:
        while(True):
            client.loop_forever()
    except KeyboardInterrupt:
        print('stop')
        utils.clear() # <--- pulizia schermo quando esci

#scelta 2 media (mi fa vedere le varie tabelle ogni 2 secondi)
def media(n_casa):
    try : 
        while(True):
            utils.clear()   # <-- pulizia schermo
            dati = collection.find({"payload.casa": n_casa})
            dati = list(dati)
            dati = utils.createDataFrameArray(dati , 5)
            utils.show(dati)
            sleep(2)
    except KeyboardInterrupt:
        print('stop')
        utils.clear()   # <--- pulizia schermo quando esci

#---------------------------------------------
# Main
item = utils.menu()



if(item[0] == 1):
    stream(item[1])
if(item[0] == 2):
    media(item[1])


