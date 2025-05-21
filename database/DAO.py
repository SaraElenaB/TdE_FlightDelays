from database.DB_connect import DBConnect
from model.airport import Airport
from model.arco import Arco


class DAO():

    @staticmethod
    def getAllAirports():

        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    # -----------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllNodes( minCompagnie, idMapAirports):

        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.ID, t.IATA_CODE, count(*) as numCompagnie
                   from (select a.ID, a.IATA_CODE, f.AIRLINE_ID, count(*) as numVoli
                   from airports a , flights f 
                   where a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID
                   group by a.ID, a.IATA_CODE, f.AIRLINE_ID) t
                   group by t.ID, t.IATA_CODE
                   having numCompagnie>=%s
                   order by numCompagnie asc"""

        cursor.execute(query, (minCompagnie,))

        for row in cursor:
            result.append(idMapAirports[row["ID"]])

        cursor.close()
        conn.close()
        return result

    # -----------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllEdgesPython(idMapAirports):

        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as numVoli
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID """

        cursor.execute(query)

        for row in cursor:
            # result.append(idMapAirports[row["ORIGIN_AIRPORT_ID"]],
            #               idMapAirports[row["DESTINATION_AIRPORT_ID"]],
            #               row["numVoli"] )
            result.append( Arco( idMapAirports[row["ORIGIN_AIRPORT_ID"]],
                                 idMapAirports[row["DESTINATION_AIRPORT_ID"]],
                                 row["numVoli"] ))

        cursor.close()
        conn.close()
        return result

    # -----------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllEdgesQuery(idMapAirports):

        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        # modifico query --> left join vuol dire che inverto la tabella, ho la speculare
        # left join --> sono sicura che l'arco c'è: non è vero ci sono dei NULL
        # tolgo tutto e aggiungo dei filtri: 1. where con < per togliere i doppioni
        #                                    2. COALESCE --> funzione che restituisce il primo elemento che non è null
        # on --> specifica la condizione con cui unire le righe del join
        # or --> quando ho solo andata, il where mi toglie l'andata perciò lo reinserisco

        query = """select t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, COALESCE(t1.numvoli,0) + coalesce(t2.numvoli,0) as numVoli
                   from (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as numVoli
                         from flights f 
                         group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                         order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID) t1
                   left join (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as numVoli
                              from flights f 
                              group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                              order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID) t2
                   on t1.origin_airport_id = t2.destination_airport_id
                   and t1.destination_airport_id = t2.origin_airport_id
                   where t1.origin_airport_id < t1.destination_airport_id 
                   or t2.origin_airport_id  is NULL"""

        cursor.execute(query)

        for row in cursor:
            # result.append(idMapAirports[row["ORIGIN_AIRPORT_ID"]],
            #               idMapAirports[row["DESTINATION_AIRPORT_ID"]],
            #               row["numVoli"] )
            result.append(Arco(idMapAirports[row["ORIGIN_AIRPORT_ID"]],
                               idMapAirports[row["DESTINATION_AIRPORT_ID"]],
                               row["numVoli"]))

        cursor.close()
        conn.close()
        return result


    # -----------------------------------------------------------------------------------------------------------------------------------------

