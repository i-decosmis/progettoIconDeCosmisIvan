# Importo le librerie necessarie
import pandas
import bnlearn
from pgmpy.factors.discrete import TabularCPD


# Classe che grazie a una rete bayesiana calcola la probabilita' di prendersi un mal di gola
class BayesianaFreddo:
    def __init__(self):
        # Creo i bordi DAG
        self.Bordi = [('Vento', 'Colpo_di_freddo'),
                      ('Freddo', 'Colpo_di_freddo')]
        # Assegno il CPT(conditional probability distribution) per ogni nodo nel DAG
        self.CPD_vento = TabularCPD(variable='Vento', variable_card=5,
                                    values=[[0.05],
                                            [0.1],
                                            [0.2],
                                            [0.25],
                                            [0.4]])
        self.CPD_freddo = TabularCPD(variable='Freddo', variable_card=5,
                                     values=[[0.05],
                                             [0.1],
                                             [0.2],
                                             [0.25],
                                             [0.4]])
        self.CPD_colpo_di_freddo = TabularCPD(variable='Colpo_di_freddo', variable_card=2,
                                           values=[[0.90, 0.70, 0.65, 0.50, 0.35,
                                                    0.80, 0.60, 0.45, 0.35, 0.15,
                                                    0.70, 0.55, 0.40, 0.20, 0.05,
                                                    0.60, 0.40, 0.30, 0.10, 0.05,
                                                    0.45, 0.30, 0.15, 0.05, 0.01],
                                                   [0.10, 0.30, 0.35, 0.50, 0.65,
                                                    0.20, 0.40, 0.55, 0.65, 0.85,
                                                    0.30, 0.45, 0.60, 0.80, 0.95,
                                                    0.40, 0.60, 0.70, 0.90, 0.95,
                                                    0.55, 0.70, 0.85, 0.95, 0.99]],
                                           evidence=['Vento', 'Freddo'],
                                           evidence_card=[5, 5])
        # Collego il DAG con ogni CPT
        self.DAG = bnlearn.make_DAG(self.Bordi, CPD=[
            self.CPD_vento,
            self.CPD_freddo,
            self.CPD_colpo_di_freddo
        ], verbose=0)

    # Esegue un'operazione di inferenza avendo in input una rete funzionante e i dati necessari
    def inferenza(self, dati): return bnlearn.inference.fit(self.DAG,
                                                            variables=['Colpo_di_freddo'],
                                                            evidence=dati,
                                                            verbose=0)

    # Funzione che disegna la struttura della DAG
    def DEBUG_dag(self):
        bnlearn.plot(self.DAG)

    # Funzione che stampa per ogni nodo il CPD
    def DEBUG_cpd(self):
        bnlearn.print_CPD(self.DAG)

    def impara_dataset(self, dataset, metodo):
        self.DAG = bnlearn.make_DAG(self.Bordi,
                                    verbose=0)
        self.DAG = bnlearn.parameter_learning.fit(self.DAG,
                                                  dataset,
                                                  methodtype=metodo,
                                                  verbose=0)


# Classe che grazie a una rete bayesiana calcola la probabilita' di prendersi un colpo di sole
class BayesianaCaldo:
    def __init__(self):
        # Creo i bordi DAG
        self.Bordi = [('Caldo', 'Colpo_di_sole')]
        # Assegno il CPT(conditional probability distribution) per ogni nodo nel DAG
        self.CPD_caldo = TabularCPD(variable='Caldo',
                                    variable_card=5,
                                    values=[[0.05],
                                            [0.1],
                                            [0.2],
                                            [0.25],
                                            [0.4]])
        self.CPD_colpo_di_sole = TabularCPD(variable='Colpo_di_sole',
                                            variable_card=2,
                                            values=[[0.90, 0.70, 0.65, 0.45, 0.15],
                                                    [0.10, 0.30, 0.35, 0.55, 0.85]],
                                            evidence=['Caldo'],
                                            evidence_card=[5])

        # Collego il DAG con ogni CPT
        self.DAG = bnlearn.make_DAG(self.Bordi, CPD=[
            self.CPD_caldo,
            self.CPD_colpo_di_sole
        ], verbose=0)

    # Esegue un'operazione di inferenza avendo in input una rete funzionante e i dati necessari
    def inferenza(self, dati):
        return bnlearn.inference.fit(self.DAG,
                                     variables=['Colpo_di_sole'],
                                     evidence=dati,
                                     verbose=0)

    # Funzione di debug che disegna la struttura della DAG
    def DEBUG_dag(self):
        bnlearn.plot(self.DAG)

    # Funzione di debug che stampa per ogni nodo il CPD
    def DEBUG_cpd(self):
        bnlearn.print_CPD(self.DAG)

    def impara_dataset(self, dataset, metodo):
        self.DAG = bnlearn.make_DAG(self.Bordi,
                                    verbose=0)
        self.DAG = bnlearn.parameter_learning.fit(self.DAG,
                                                  dataset,
                                                  methodtype=metodo,
                                                  verbose=0)



# Data una query ritorna il risultato
def ottieni_risultato_query(query) -> pandas.DataFrame:
    return bnlearn.bnlearn.query2df(query, verbose=0)
