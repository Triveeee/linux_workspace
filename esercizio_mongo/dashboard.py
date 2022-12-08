from pymongo import * 
from random import *
from datetime import *
from time import *
from json import *
import utils.index as utils


#-----------------------------------------------
#Conessione ad Atlas

password = 'trive004'
uri = 'mongodb+srv://riccardo:'+ password + '@cluster0.zzvi9yy.mongodb.net/test'
atlas = MongoClient(uri)
db = atlas.cluster0
collection = db.case

#----------------------------------------------
#Funzioni
# scelta 1 visualizzazione in tempo reale
def stream(n_casa):
    try:
        while(True):
            utils.clear() # <-- pulizia schermo
            dati = collection.find({"payload.casa": n_casa})
            utils.showSeries(dati)
            sleep(5)
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
#Main
item = utils.menu()

if(item[0] == 1):
    stream(item[1])
if(item[0] == 2):
    media(item[1])


