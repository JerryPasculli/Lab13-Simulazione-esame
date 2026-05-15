from model.model import Model

modello = Model()
modello.creaGrafo("circle", 2010)
titolo, stringa = modello.output()
print(titolo)
print(stringa)
tes1, tes2 = modello.ricorsione()
print(tes1)
print(tes2)