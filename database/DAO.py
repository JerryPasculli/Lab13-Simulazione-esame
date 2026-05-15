from database.DB_connect import DBConnect
from model.arco import Arco
from model.stato import Stato


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getAnni():
        db = DBConnect.get_connection()
        cursor = db.cursor()
        query = """select distinct year(datetime)
from sighting s """
        cursor.execute(query)
        lista = []
        for element in cursor:
            lista.append(element[0])
        cursor.close()
        db.close()
        return lista

    @staticmethod
    def getForme(anno):
        db = DBConnect.get_connection()
        cursor = db.cursor()
        query = """select distinct shape
from sighting where year(datetime) = %s and shape != "" """
        cursor.execute(query, [anno])
        lista = []
        for element in cursor:
            lista.append(element[0])
        cursor.close()
        db.close()
        return lista

    @staticmethod
    def getNodi():
        db = DBConnect.get_connection()
        cursor = db.cursor(dictionary = True)
        query = """select id, name, Lat, Lng
from state
"""
        cursor.execute(query)
        lista = []
        for element in cursor:
            nodo = Stato(**element)
            lista.append(nodo)
        cursor.close()
        db.close()
        return lista

    @staticmethod
    def getArchi():
        db = DBConnect.get_connection()
        cursor = db.cursor(dictionary = True)
        query = """SELECT *
from neighbor
where state1>state2"""
        cursor.execute(query)
        lista = []
        for element in cursor:
            arco = Arco(**element)
            lista.append(arco)
        cursor.close()
        db.close()
        return lista

    @staticmethod
    def getPesoArchi(forma, anno):
        db = DBConnect.get_connection()
        cursor = db.cursor()
        query = """with numeroAvvistamento as (select s.id, count(*) as numero
from state s, sighting s1 where upper(s1.state) = s.id and s1.shape = %s 
and YEAR(datetime) = %s
group by s.id)

select n.state1, n.state2, sum(numero) as peso
from neighbor n, numeroAvvistamento n1
where n.state1>n.state2 and (n.state1 = n1.id or n.state2 = n1.id)
group by n.state1, n.state2"""
        cursor.execute(query, [forma, anno])
        lista = []
        for element in cursor:
            lista.append(element)
        cursor.close()
        db.close()
        return lista

    @staticmethod
    def getPesoNodi(forma, anno):
        db = DBConnect.get_connection()
        cursor = db.cursor()
        query = """with numeroAvvistamento as (select s.id, count(*) as numero
from state s, sighting s1 where upper(s1.state) = s.id and s1.shape = %s 
and YEAR(datetime) = %s
group by s.id), 

ultimo as (select n.state1, n.state2, sum(numero) as peso
from neighbor n, numeroAvvistamento n1
where n.state1>n.state2 and (n.state1 = n1.id or n.state2 = n1.id)
group by n.state1, n.state2)

select id, sum(peso)
from ultimo, state
where id = state1 or id = state2
group by id"""
        cursor.execute(query, [forma, anno])
        lista = []
        for element in cursor:
            lista.append(element)
        cursor.close()
        db.close()
        return lista


