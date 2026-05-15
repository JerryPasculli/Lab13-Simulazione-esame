class Arco():
    def __init__(self, state1, state2):
        self._state1 = state1
        self._state2 = state2
        self._peso = 0

    def aggiungiPeso(self, peso):
        self._peso = peso