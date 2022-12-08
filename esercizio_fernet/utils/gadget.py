# stampa del menu su console
def menuStamp():
    print('\n------------------------------------ \n')
    print('#1 --> tempo reale')
    print('#2 --> media')
    print('\n------------------------------------ \n') 
    

#agoinge in un dizionario vuoto i valori di uno specifico 
#elemento di mongodb per ogni stanza
def addElement(empty_dictionary, contenuto , nome ):
     empty_dictionary['cucina'].append(contenuto[0]['cucina'][nome])
     empty_dictionary['soggiorno'].append(contenuto[1]['soggiorno'][nome])
     empty_dictionary['mansarda'].append(contenuto[2]['mansarda'][nome])
     empty_dictionary['camera_da_letto'].append(contenuto[3]['camera_da_letto'][nome])
     return(empty_dictionary)   


# funzione che ti calcola la media di una specifica tabella
#di dati per ogni colonna 
def media(table):
    table_medie = {"cucina": 0, "soggiorno": 0, "mansarda": 0, "camera_da_letto": 0}
    medie = []
    for i in table:
        somma = 0
        for element in table[i]:
            somma = somma + element
        media = somma/len(table[i])
        medie.append(media)
    
    i = 0    
    for element in table_medie:
        table_medie[element] = medie[i]
        i+=1

    return(table_medie)