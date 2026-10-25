import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapR = {}

    def getAllYears(self):
        return DAO.getAllYears()

    def creaGrafo(self, anno1, anno2):
        self._grafo.clear()
        self._idMapR.clear()

        circuiti = DAO.getAllNodes()
        for a in circuiti:
            self._idMapR[a.circuitId] = a
            self._grafo.add_node(a)
            # aggiungo i nodi
        print("2 - Nodi aggiunti")

        for a in circuiti:
            a.risultati_per_anno=0
            a.gare_completate = 0
            a.risultati_per_anno=DAO.getRisultatiPerCircuito(a.circuitId, anno1, anno2)

            for year, pilota, position in a.risultati_per_anno:
                if position is not None:
                    a.gare_completate +=1

        print("3 - Informazioni recuperate")

        for i in range(len(circuiti)):
            a1 = circuiti[i]

            for j in range(i + 1, len(circuiti)):
                a2 = circuiti[j]

                # Entrambi devono aver corso nel periodo
                if (len(a1.risultati_per_anno) > 0 and len(a2.risultati_per_anno) > 0):
                    peso = a1.gare_completate + a2.gare_completate

                    self._grafo.add_edge(a1, a2, weight=peso)


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    def getConnessaInfo(self):
        components = list(nx.connected_components(self._grafo))
        if len(components) == 0:
            return 0, set(), []

        largest = max(components, key=len)
        pesi = {}
        for nodo in largest:
            maxPeso = None

            for vicino in self._grafo.neighbors(nodo):
                peso = self._grafo[nodo][vicino]["weight"]
                if maxPeso is None or peso >maxPeso:
                    maxPeso = peso

            pesi[nodo] = maxPeso
        ordered_nodes = sorted(largest, key=lambda n: pesi[n], reverse=True)
        details = [(n, pesi[n]) for n in ordered_nodes]

        return len(components), largest, details
    # SE ALL'ESAME CHIEDESSERO MAX PESO ARCHI IO DEVO CAMBIARE CON:
    # maxPeso= None
    # if maxPeso is None or peso > maxPeso:
    # maxPeso = peso

    def _indiceEmozionante(self, team):
        if team.gare_totali == 0:
            return 0
        return 1 - team.gare_completate / team.piloti_totali

    def getGruppoTeamChampion(self, K, M):
        self._best_path = []
        self._best_score = -1

        components = list(nx.connected_components(self._grafo))
        if len(components) == 0:
            return None, 0

        # Individuo la componente connessa maggiore
        largest = max(components, key=len)
        candidati = []
        for team in largest:
            # Conto gli anni distinti in cui il team ha partecipato
            anni = set()
            for anno, pilota, time in team.risultati_per_anno:
                anni.add(anno)
            if len(anni) >= M:
                candidati.append(team)

        # Verifico che ci siano almeno K team validi
        if len(candidati) < K:
            return None, 0
        # Il percorso parziale  NONparte con il nodo selezionato
        parziale = []
        self._ricorsione(parziale, parziale, 0, K, 0)

        return self._best_path, self._best_score

    def _ricorsione(self, candidati, parziale, start, K, score):
        # Caso terminale: ho scelto K team
        if len(parziale) == K:
            if score > self._best_score:
                self._best_score = score
                self._best_path = list(parziale)
            return

        # Provo ad aggiungere un team
        for i in range(start, len(candidati)):
            circuito = candidati[i]

            indice = self._indiceEmozionante(circuito)
            parziale.append(circuito)

            self._ricorsione(candidati, parziale, i + 1, K, score + indice)

            # Tolgo il team e provo un'altra combinazione
            parziale.pop()



