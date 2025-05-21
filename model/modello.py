import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._airports= DAO.getAllAirports()

        self._idMapAirports={}
        for a in self._airports:
            self._idMapAirports[a.ID]=a

    # -----------------------------------------------------------------------------------------------------------------------------------------
    def buildGraph(self, minCompagnie):

        nodes= DAO.getAllNodes( minCompagnie, self._idMapAirports)
        self._grafo.add_nodes_from(nodes)
        #print(len(self._grafo.nodes) )
        #self.addAllArchiPython()
        #print(f"1) Num nodi: {len(self._grafo.nodes())} \nNum archi: {len(self._grafo.edges())} ")
        #self._grafo.clear_edges()
        self.addAllArchiQuery()
        #print(f"2) Num nodi: {len(self._grafo.nodes())} \nNum archi: {len(self._grafo.edges())} ")


    def getGraphDetails(self):
        return len(self._grafo.nodes()), len(self._grafo.edges())

    def getAllNodes(self):
        nodes = list(self._grafo.nodes())
        nodes.sort(key=lambda x: x.IATA_CODE )
        return nodes

    # -----------------------------------------------------------------------------------------------------------------------------------------
    def addAllArchiPython(self):
        # DAO --> prende tutto
        allEdges= DAO.getAllEdgesPython(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._grafo and e.aeroportoA in self._grafo: #devo filtrare e aggiungere archi solo dove i nodi ci sono
                if self._grafo.has_edge(e.aeroportoP, e.aeroportoA):
                    self._grafo[e.aeroportoP][e.aeroportoA]["weight"] += e.peso  #se c'è già sommo il peso
                else:
                    self._grafo.add_edge( e.aeroportoP, e.aeroportoA, weight=e.peso )

    # -----------------------------------------------------------------------------------------------------------------------------------------
    def addAllArchiQuery(self):
        # DAO --> risultato pulito
        allEdges= DAO.getAllEdgesQuery(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._grafo and e.aeroportoA in self._grafo:
                self._grafo.add_edge(e.aeroportoP, e.aeroportoA, weight=e.peso) #sono sicura che non ci sono righe ripetute

    # -----------------------------------------------------------------------------------------------------------------------------------------
    def getSortedNeighbors(self, node):

        neighbors= self._grafo.neighbors(node) #self._grafo[node]
        neighborsTuples = []

        for n in neighbors:
            neighborsTuples.append( (n, self._grafo[node][n]["weight"]) ) #(nodo, peso dell'arco)

        neighborsTuples.sort(key=lambda x: x[1], reverse=True) #secondo elemento della chaive-->il peso
        return neighborsTuples

    # -----------------------------------------------------------------------------------------------------------------------------------------
    def getPath(self, u, v):
        pathDijkstra = nx.dijkstra_path(self._grafo, u, v, weight=None)  #cosi trova il cammino con il num inferiore di archi
        pathMinimo = nx.shortest_path(self._grafo, u, v, weight=None)    #implementa o dijkstra o bellanford

        # myDict = dict(nx.bfs_predecessors(self._grafo, u) )
        # path=[v]
        # while path[0] != u:
        #     path.insert(0, myDict[path[0]])
        return pathDijkstra

# -----------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    m = Model()
    m.buildGraph(5)  #mi dice che ho 98 compagnie