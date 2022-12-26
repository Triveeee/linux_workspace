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
f = open('key.txt' , 'r')
chiave = f.read()
f.close()
chiave_valore = Fernet(chiave)
#

#lettura file
f = open('casa.config.txt' , 'r')
list = f.read().split(' = ')
#

#parametri
topic = 'home/misurazioni/' + list[1]   
refresh = 5
dati = {
    "casa": 0,
    "data": "",
    "tempo": "",
    "stanze": {
        "cucina": {"temperatura": 0, "umidita": 0},
        "soggiorno": {"temperatura": 0, "umidita": 0 },
        "mansarda": {"temperatura": 0 , "umidita": 0 },
        "camera_da_letto": {"temperatura": 0 , "umidita": 0}
    }
} 


@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/stanza/<param>')
def room(param):
    nome = 'dati.html'
    obj = dati['stanze'][param]
    obj = {**obj , "tempo": dati['tempo'] , 'data': dati['data']}
    print(dati)
    return render_template(nome , dati=obj , REFRESH=refresh)

@mqtt.on_connect()
def gestione_conessione(client , userdata , flasgs , rc):
    mqtt.subscribe(topic)

@mqtt.on_message()
def gestione_messaggio(client , userdata , msg):
    global dati
    dati_criptati = msg.payload
    dati_json_bytes = chiave_valore.decrypt(dati_criptati) # <--- decriptazione del messaggio in bytes (string criptato-> bytes decriptato)
    dati_json = dati_json_bytes.decode('utf-8')
    dati = json.loads(dati_json)
    print(dati)
    return(dati_json)



