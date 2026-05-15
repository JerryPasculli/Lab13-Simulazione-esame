import copy

import networkx as nx

from database.DAO import DAO
import geopy.distance


class Model:
    def __init__(self):
        self._G = nx.Graph()
        self._nodi = []
        self._archi = []
        self._Dnodi = {}
        self._Darchi = {}

    def getAnni(self):
        lista = DAO.getAnni()
        return lista

    def getForme(self, anno):
        lista = DAO.getForme(anno)
        return lista

    def creaGrafo(self, forma, anno):
        self._G = nx.Graph()
        self._nodi = []
        self._archi = []
        self._Dnodi = {}
        self._Darchi = {}
        self._nodi = DAO.getNodi()
        self._G.add_nodes_from(self._nodi)
        for element in self._nodi:
            self._Dnodi[element._id] = element
        self._archi = DAO.getArchi()
        for element in self._archi:
            stringa = element._state1 + "_" + element._state2
            self._Darchi[stringa] = element
        pesiArchi = DAO.getPesoArchi(forma, anno)
        for element in pesiArchi:
            stringa = element[0] + "_" + element[1]
            arco = self._Darchi[stringa]
            arco.aggiungiPeso(element[2])
        for element in self._archi:
            nodo1 = self._Dnodi[element._state1]
            nodo2 = self._Dnodi[element._state2]
            self._G.add_edge(nodo1, nodo2, weight = element._peso)
        pesiNodi = DAO.getPesoNodi(forma, anno)
        for element in pesiNodi:
            nodo1 = self._Dnodi[element[0]]
            nodo1.aggiungiPeso(element[1])

    def output(self):
        numeroNodi = nx.number_of_nodes(self._G)
        numeroArchi = nx.number_of_edges(self._G)
        titolo = f"Numero di vertici: {numeroNodi} Numero di archi: {numeroArchi}"
        stringa = ""
        for element in self._nodi:
            if stringa == "":
                stringa = f"Nodo {element._id}, somma pesi su archi {element._peso}"
            else:
                stringa = stringa + "\n" + f"Nodo {element._id}, somma pesi su archi {element._peso}"
        return titolo, stringa


    def ricorsione(self):
        self._soluzione = []
        self._top = 0
        for element in self._nodi:
            soluzione = []
            tot = 0
            self.percorsoMigliore(element, soluzione, tot)
        stringa = ""
        for i in range(len(self._soluzione)):
            if i != len(self._soluzione) - 1:
                nodo1 = self._soluzione[i]
                nodo2 = self._soluzione[i + 1]
                coord1 = nodo1._Lat, nodo1._Lng
                coord2 = nodo2._Lat, nodo2._Lng
                lista = [nodo1._id, nodo2._id]
                lista.sort(reverse=True)
                stringa1 = lista[0] + "_" + lista[1]
                arco = self._Darchi[stringa1]
                dist = geopy.distance.distance(coord1, coord2).km
                if i == 0:
                    stringa = f"{nodo1._id} ---> {nodo2._id}: weight {arco._peso} distance {dist}"
                else:
                    stringa = stringa + "\n" + f"{nodo1._id} ---> {nodo2._id}: weight {arco._peso} distance {dist}"
        return self._top, stringa

    def percorsoMigliore(self, element, soluzione, tot):
        daVisitare = list(self._G.neighbors(element))
        soluzione  = [element]
        self.itera(daVisitare, soluzione, tot, 0)

    def itera(self, daVisitare, soluzione, tot, arco0):
        if tot>self._top:
            self._top = tot
            self._soluzione = copy.deepcopy(soluzione)
        for element in daVisitare:
            if element not in soluzione:
                lista = [soluzione[len(soluzione) - 1]._id, element._id]
                lista.sort(reverse = True)
                stringa = lista[0] + "_" + lista[1]
                arco = self._Darchi[stringa]
                if arco._peso>arco0:
                    coord1 = soluzione[len(soluzione) - 1]._Lat, soluzione[len(soluzione) - 1]._Lng
                    coord2 = element._Lat, element._Lng
                    soluzione.append(element)
                    tot1 = tot + geopy.distance.distance(coord1, coord2).km
                    daVisitare2 = self._G.neighbors(element)
                    self.itera(daVisitare2, soluzione, tot1, arco._peso)
                    soluzione.pop()






