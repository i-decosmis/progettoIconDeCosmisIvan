# Importo le librerie necessarie
from experta import *
from src.ClassiSupporto import interfacciaConUtente


# Creo la classe che gestisce il sistema esperto
class ConsigliVestiti(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(azione="chiedereOnline")

    @Rule(Fact(azione="chiedereOnline"), salience=1)
    def chiedere_online(self):
        self.declare(Fact(azione=interfacciaConUtente.chiedi_online()))

    @Rule(Fact(azione='trovareInformazioniOnline'),
          NOT(Fact(risultato=W())), salience=1)
    def ricerca_informazioni(self):
        self.declare(Fact(risultato=interfacciaConUtente.risultati_previsioni()))

    @Rule(Fact(risultato="trovareInformazioniOffline"), salience=0)
    def errore_citta_non_trovata(self):
        self.declare(Fact(scelta=interfacciaConUtente.chiedi_inserimento_manuale()))

    @Rule(AND(NOT(Fact(risultato="trovareInformazioniOffline"))), Fact(risultato=MATCH.risultato), salience=0)
    def greet(self, risultato):
        self.declare(Fact(fascia_oraria=risultato[0]))
        self.declare(Fact(meteo=risultato[1]))
        self.declare(Fact(temperatura=risultato[2]))
        self.declare(Fact(azione="chiediStile"))

    @Rule(Fact(scelta="no"), salience=0)
    def fine_elaborazione(self):
        self.declare(Fact(azione="terminaAnalisi"))
        print("Fine del sistema esperto")

    @Rule(OR(Fact(scelta="si"), Fact(azione="trovareInformazioniOffline")), salience=0)
    def chiedere_informazioni(self):
        self.declare(Fact(fascia_oraria=interfacciaConUtente.chiedi_fascia_oraria()))
        self.declare(Fact(meteo=interfacciaConUtente.chiedi_meteo()))
        self.declare(Fact(temperatura=interfacciaConUtente.chiedi_temperatura()))
        self.declare(Fact(vento=interfacciaConUtente.chiedi_vento()))
        self.declare(Fact(azione="chiediStile"))

    @Rule(Fact(azione="chiediStile"), salience=0)
    def chiedere_stile(self):
        self.declare(Fact(stile=interfacciaConUtente.chiedi_look()))
        self.declare(Fact(azione="chiediDurata"))

    @Rule(Fact(azione="chiediDurata"), salience=0)
    def chiedere_durata(self):
        self.declare(Fact(durata=interfacciaConUtente.chiedi_durata()))
        self.declare(Fact(azione="stampaStile"))

    @Rule(Fact(azione="stampaStile"),
          Fact(stile=MATCH.stile),
          Fact(fascia_oraria=MATCH.fascia_oraria),
          Fact(temperatura=MATCH.temperatura),
          Fact(meteo=MATCH.meteo),
          salience=0)
    def stampare_vestiti(self, stile, fascia_oraria, temperatura, meteo):
        interfacciaConUtente.stampa_risultato(stile, fascia_oraria, temperatura, meteo)
        self.declare(Fact(azione="stampaRicambi"))

    @Rule(Fact(azione="stampaRicambi"), Fact(durata=MATCH.durata), salience=0)
    def stampare_ricambi(self, durata):
        interfacciaConUtente.stampa_ricambi(durata)
        self.declare(Fact(azione="controllaMeteo"))

    @Rule(Fact(azione="controllaMeteo"), salience=0)
    def controllare_meteo(self):
        interfacciaConUtente.stampa_allerta_meteo()
        self.declare(Fact(azione="fineSistemaEsperto"))

    @Rule(Fact(azione="fineSistemaEsperto"), salience=0)
    def test(self):
        print("===============================================")
        print("Esecuzione terminata con successo!")
        exit(0)


def avvia_sistema_esperto():
    sistema = ConsigliVestiti()
    # Prepara il sistema per l'esecuzione
    sistema.reset()
    # Avvia il sistema
    sistema.run()

