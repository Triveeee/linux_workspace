import os
from platform import *
from pandas import *
from utils.gadget import *

# creazione menu nel terminale
def menu():
    n = 0
    while(n > 4 or n < 1):
        n =  int(input('scegli numero casa (1 / 4): '))
    print(menuStamp())
    choose = int(input('scegli : '))
    return (choose , n)

#comando di pulizia schermo
def clear():
    if(system() == 'Windows'):
        os.system('cls')
    if(system() == 'Linux'):
        os.system('clear')  
    
#crazione di una lista di DataFrame e Series per la stampa dei dati con pandas
def createDataFrameArray(items , n):
    table_temp = {"cucina": [], "soggiorno": [], "mansarda": [] , "camera_da_letto": []}
    table_umidita = {"cucina": [], "soggiorno": [], "mansarda": [] , "camera_da_letto": []}
    items = items[(len(items) - n): ]

    for i in items:
        stanze = i['payload']['stanze']
        table_temp = addElement(table_temp, stanze , 'temperatura')
        table_umidita = addElement(table_umidita , stanze , 'umidita')
    
    table_medie_temp = media(table_temp)
    table_medie_umid = media(table_umidita)   

    return(DataFrame(table_temp) , DataFrame(table_umidita) , Series(table_medie_temp) , Series(table_medie_umid))

#crea una Series di dati
def showSeries(dati):
    count = 1
    for i in dati:
        print("[" + str(count) + "] --> ", i , '\n')
        count+=1

#mostra i vari dataframe
def show(dati):
    print('**TEMPERATURA**\n',dati[0], '\n')
    print('------------------------------------------------------------', '\n')
    print('**UMIDITA**\n',dati[1], '\n')
    print('------------------------------------------------------------', '\n')
    print('**MEDIA_TEMP**\n',dati[2],'\n')
    print('------------------------------------------------------------', '\n')
    print('**MEDIA_UMIDITA**\n',dati[3],'\n')


