from flask import Flask, render_template
from flask_mqtt import Mqtt
import json
from  cryptography.fernet import Fernet

app = Flask(__name__)

# configurazione Mqtt Server
app.config['MQTT_BROKER_URL'] = '80.210.122.173'
app.config['MQTT_BROKER_PORT'] = 1883
#

mqtt = Mqtt(app)

# chiave Fernet
chiave = 'fM5t5hPaMlRWtmfpnbaaDAsYJvsDnDE5Ehd_9oYirEg='
chiave_valore = Fernet(chiave)
#

#lettura file
f = open('casa.config.txt' , 'r')
list = f.read().split(' = ')
#

#parametri
topic = 'home/temperatura/' + list[1]
refresh = 5
dati_json = ""
#


@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/stanza/<param>')
def room(param):
    nome = 'dati.html'
    dati= json.loads(dati_json)
    obj = dati['stanze'][param]
    obj = {**obj , "tempo": dati['tempo'] , 'data': dati['data']}

    return render_template(nome , dati=obj , REFRESH=refresh)

@mqtt.on_connect()
def gestione_conessione(client , userdata , flasgs , rc):
    mqtt.subscribe(topic)

@mqtt.on_message()
def gestione_messaggio(client , userdata , message):
    global dati_json
    dati_criptati = message.payload.decode()
    dati_json_bytes = chiave_valore.decrypt(dati_criptati) # <--- decriptazione del messaggio in bytes (string criptato-> bytes decriptato)
    dati_json = dati_json_bytes.decode('utf-8')
    return(dati_json)



