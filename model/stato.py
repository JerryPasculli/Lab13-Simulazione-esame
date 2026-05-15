from dataclasses import dataclass


class Stato:

    def __init__(self, id, name, Lat, Lng):
        self._id = id
        self._name = name
        self._Lat = Lat
        self._Lng = Lng
        self._peso = 0

    def aggiungiPeso(self, peso):
        self._peso = peso