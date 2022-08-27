# Importo librerie utili
import json
import logging
import requests
import pandas
from owlready2 import *
from geopy.geocoders import Nominatim
from datetime import datetime, timezone, timedelta

temp = -1000
vento = ""
tipo = ""
fascia = ""
rete = ""


def chiedi_online():
    while True:
        scelta = input("Effettuare la ricerca online con il nome della tua citta'?(si/no)")
        if scelta == "si":
            scelta = "trovareInformazioniOnline"
            break
        elif scelta == "no":
            scelta = "trovareInformazioniOffline"
            break
        else:
            print("Hai effettuato una scelta sbagliata!")
    return scelta


def risultati_previsioni():
    logging.getLogger(requests.packages.urllib3.__package__).setLevel(logging.ERROR)
    nome_citta = input("Dove ti trovi?")
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        address = geolocator.geocode(nome_citta)
    except Exception as E:
        print("Connessione ad internet assente")
        address = None
    api_key = "4a6951acc894df2c43ce2727b31bb8c0"
    if address is None:
        lat = -1000
        lon = -1000
    else:
        lat = address.latitude
        lon = address.longitude
    if lat != -1000:
        informazioni = ricerca_previsioni_online(lat, lon, api_key)
    else:
        informazioni = "trovareInformazioniOffline"
    return informazioni


def ricerca_previsioni_online(lat, lon, api_key):
    global temp
    global vento
    global tipo
    global fascia
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (
        lat, lon, api_key)
    response = requests.get(url)
    data = json.loads(response.text)
    informazioni = [datetime.fromtimestamp(data['current']['dt'], timezone(-timedelta(hours=-2))).strftime('%H'),
                    data['current']['weather'][0]['main'], data['current']['temp'], ""]
    if informazioni[1] != "Clouds" and informazioni[1] != "Clear":
        informazioni[1] = "Altri"
    if int(informazioni[0]) > 14:
        informazioni[0] = "sera"
        fascia = "sera"
    elif int(informazioni[0]) < 3:
        informazioni[0] = "sera"
        fascia = "sera"
    else:
        informazioni[0] = "mattina"
    temp = informazioni[2]
    if int(informazioni[2]) > 26:
        tipo = "caldo"
        informazioni[2] = "caldo"
        converti_temperatura_caldo()
    elif int(informazioni[2]) >= 15:
        informazioni[2] = "normale"
    elif int(informazioni[2]) < 15:
        tipo = "freddo"
        informazioni[2] = "freddo"
        converti_temperatura_freddo()
        vento = data['current']['wind_speed']
        vento = vento * 60
        vento = vento * 60
        vento = vento / 1000
        converti_vento()
    controlla_situazione_meteorologica(informazioni)
    return informazioni


def controlla_situazione_meteorologica(informazioni):
    global tipo
    if tipo == "caldo" or tipo == "freddo":
        informazioni[3] = "allerta_meteo"


def chiedi_inserimento_manuale():
    while True:
        scelta = input("Citta' non trovata, vuoi inserire manualmente i dati?(si/no)")
        if scelta == "si" or scelta == "no":
            break
        else:
            print("Hai inserito una scelta sbagliata!")
    return scelta


def chiedi_fascia_oraria():
    global fascia
    while True:
        fascia_oraria = input("Scegli la fascia oraria(mattina/sera) ")
        if fascia_oraria == "mattina" or fascia_oraria == "sera":
            if fascia_oraria == "sera":
                fascia = "sera"
            break
        else:
            print("Hai inserito una scelta sbagliata!")
    return fascia_oraria


def chiedi_meteo():
    while True:
        meteo = input("Scegli le condizioni meteo attuali(nuvoloso, scoperto, rovesci) ")
        if meteo == "nuvoloso":
            meteo = "Clouds"
            break
        elif meteo == "scoperto":
            meteo = "Clear"
            break
        elif meteo == "rovesci":
            meteo = "Altri"
            break
        else:
            print("Hai inserito una scelta sbagliata!")
    return meteo


def chiedi_temperatura():
    global temp
    global tipo
    global fascia
    while True:
        temperatura = input("Inserisci la temperatura in gradi celsius ")
        try:
            float(temperatura)
            if int(temperatura) > 26:
                tipo = "caldo"
                temp = int(temperatura)
                temperatura = "caldo"
                converti_temperatura_caldo()
            elif int(temperatura) >= 15:
                temperatura = "normale"
            elif int(temperatura) < 15:
                tipo = "freddo"
                temp = int(temperatura)
                converti_temperatura_freddo()
                temperatura = "freddo"
            break
        except ValueError:
            print("Hai inserito una scelta sbagliata!")
    return temperatura


def chiedi_look():
    while True:
        stile_look = input("Quale look preferisci oggi?(casual/elegante/sportivo) ")
        if stile_look == "casual" or stile_look == "elegante" or stile_look == "sportivo":
            break
        else:
            print("Hai scelto uno stile non gestito dal sistema!")
    return stile_look


def chiedi_durata():
    while True:
        tempo = input("Torni a casa oppure dormi fuori?(casa/fuori) ")
        if tempo == "casa" or tempo == "fuori":
            break
        else:
            print("Hai inserito una risposta errata!")
    return tempo


#chiedo il vento e imposto il grado di pericolosita'
def chiedi_vento():
    while True:
        global vento
        vento = input("Inserisci quanto forte ti sembra il vento(non presente,moderato, "
                      "teso, fresco, forte, molto forte)")
        if vento == "non presente":
            vento = 0
            break
        if vento == "moderato":
            vento = 0
            break
        elif vento == "teso":
            vento = 1
            break
        elif vento == "fresco":
            vento = 2
            break
        elif vento == "forte":
            vento = 3
            break
        elif vento == "molto forte":
            vento = 4
            break
        else:
            print("Hai inserito una risposta errata!")
    return vento

def chiedi_tipo_rete():
    global rete
    print("------------------------------------------------------------------------------")
    print("Rilevata anomalia meteorologia, selezionare il tipo di rete bayesiana da utilizzare:")
    print("(1)Rete bayesiana data \n(2)rete bayesiana con apprendimento dal dataset")
    while True:
        rete = input("Risposta: ")
        if rete == "1" or rete == "2":
            break
        else:
            print("Inserito valore errato!")
    print("Avvio della rete bayesiana selezionata per calcolare il grado di pericolosita'...")



def stampa_risultato(stile, fascia_oraria, temperatura, meteo):
    global tipo
    global reteBayesiana
    # Dati i lunghi tempi di import del file per gestire le retiBayesiane, effettuo l'import e uso la rete solo se
    # viene rilevata un'anomalia meteorologica
    if tipo == "caldo" or tipo == "freddo":
        chiedi_tipo_rete()
        src = __import__('src.ReteBayesiana.retiBayesiane', globals(), locals())
        reteBayesiana = src.ReteBayesiana.retiBayesiane
    print("===============================================")
    print("RISULTATO DELL'ANALISI")
    print("===============================================")
    print("L'abbigliamento consigliato per oggi e':")
    path = os.path.dirname(os.path.abspath("./src/Ontologia/ontologiaIndumenti.owl"))
    path = path.replace("\\", "/")
    path = "file://" + path + "/ontologiaIndumenti.owl"
    onto = get_ontology(path).load()
    set = ["busto", "gambe", "scarpe", "ombrello"]
    i = onto[stile+"_"+fascia_oraria+"_"+temperatura+"_"+meteo].instances()[0]
    indice = 0
    while indice < 4:
        for prop in i.get_properties():
            if set[indice] == prop.python_name:
                indice += 1
                print("%s: %s" % (prop.python_name.capitalize(), prop[i][0]))
                break
    print("-----------------------------------------------")


def stampa_ricambi(durata):
    if durata == "fuori":
        print("Si consiglia di portare una cambiata per la notte")
    else:
        print("Non e' necessaria una cambiata")
    print("-----------------------------------------------")


def stampa_allerta_meteo():
    global vento
    global temp
    global fascia
    global rete
    if tipo == "freddo":
        rete_bayesiana_freddo = reteBayesiana.BayesianaFreddo()
        dataset = pandas.read_csv("src/ClassiSupporto/dataset_freddo.csv")
        if rete == "2":
            rete_bayesiana_freddo.impara_dataset(dataset, "ml")
        dati = {'Vento': vento,
                'Freddo': temp}
        risultato = reteBayesiana.ottieni_risultato_query(rete_bayesiana_freddo.inferenza(dati))
        probabilita = (risultato["p"])[1] * 100
        if 10 <= probabilita <= 35:
            print("E' consigliato portare una sciarpa leggera per coprire il collo")
        elif 35 < probabilita <= 70:
            print("E' fortemente consigliato portare una sciarpa per coprire il collo")
        else:
            print("E' necessario portare una sciarpa pesante per coprire il collo!")
        print("Hai il " + str(round(probabilita,2)) + "% di probabilita' di prendere un colpo di freddo")
    elif tipo == "caldo":
        rete_bayesiana_caldo = reteBayesiana.BayesianaCaldo()
        dataset = pandas.read_csv("src/ClassiSupporto/dataset_caldo.csv")
        if rete == "2":
            rete_bayesiana_caldo.impara_dataset(dataset, "ml")
        dati = {'Caldo': temp}
        risultato = reteBayesiana.ottieni_risultato_query(rete_bayesiana_caldo.inferenza(dati))
        probabilita = (risultato["p"])[1] * 100
        if fascia != "sera":
            if 10 <= probabilita <= 35:
                print("E' consigliato portare un cappello")
            elif 35 < probabilita <= 70:
                print("E' fortemente consigliato portare un cappello")
            else:
                print("E' necessario portare un cappello!")
        print("Ricordati di mantenere il tuo corpo idratato.")
        print("Hai il " + str(round(probabilita,2)) + "% di probabilita' di prendere un colpo di calore!")
    else:
        print("Nessun'allerta meteo")

#converto la temperatura freddo in gradi di pericolosita'
def converti_temperatura_freddo():
    global temp
    if temp < 2:
        temp = 4
    elif temp < 5:
        temp = 3
    elif temp < 8:
        temp = 2
    elif temp < 11:
        temp = 1
    elif temp < 15:
        temp = 0

#converto la temperatura freddo in gradi di pericolosita'
def converti_temperatura_caldo():
    global temp
    if temp > 42:
        temp = 4
    elif temp > 38:
        temp = 3
    elif temp > 34:
        temp = 2
    elif temp > 31:
        temp = 1
    elif temp > 26:
        temp = 0

#converto il vento in gradi di pericolosita'
def converti_vento():
    global vento
    if vento <= 16:
        vento = 0
    elif 16 < vento <= 21:
        vento = 1
    elif 21 < vento <= 27:
        vento = 2
    elif 27 < vento <= 31:
        vento = 3
    elif vento > 31:
        vento = 4
