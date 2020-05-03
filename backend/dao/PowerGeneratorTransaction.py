from backend.config.dbconfig import pg_config
import psycopg2


class PowerGeneratorTransactionDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllPowerGeneratorTransactions(self):
        cursor = self.conn.cursor()
        query = "select * from powergeneratortransactions"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionById(self, tid):
        cursor = self.conn.cursor()
        query = "select * from powergeneratortransactions where generator_trans_id = %s;"
        cursor.execute(query, tid)
        result = cursor.fetchone()
        return result

    def getTransactionByFulfillerID(self, pid):
        cursor = self.conn.cursor()
        query = "select * from powergeneratortransactions where person_id = %s"
        cursor.execute(query, pid)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByFulfillerEmail(self, email):
        cursor = self.conn.cursor()
        query = "select * from powergeneratortransactions inner join persons inner join account " \
                "where email = %s;"
        cursor.execute(query, email)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByFulfillerName(self, first, last):
        cursor = self.conn.cursor()
        query = "select * " \
                "from powergeneratortransactions inner join persons " \
                "where first_name = %s" \
                "and last_name = %s;"
        cursor.execute(query, first, last)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPost(self, generator_id):
        cursor = self.conn.cursor()
        query = "select * " \
                "from powergeneratortransactions " \
                "where generator_id = %s;"
        cursor.execute(query, generator_id)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPosterEmail(self, email):
        cursor = self.conn.cursor()
        query = "select * " \
                "from powergeneratortransactions as t inner join powergenerator as r " \
                "where r.person_id = (" \
                "select person_id " \
                "from account inner join persons inner join powergenerator " \
                "where email = %s);"
        cursor.execute(query, email)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPosterName(self, first, last):
        cursor = self.conn.cursor()
        query = "select * " \
                "from powergeneratortransactions as t inner join powergenerator as r " \
                "where r.person_id = (" \
                "select person_id " \
                "from account inner join persons inner join powergenerator " \
                "where first_name = %s " \
                "and last_name = %s);"
        cursor.execute(query, first, last)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, generator_id, person_id, tquantity, tunit_price, trans_total, date_completed):
        cursor = self.conn.cursor()
        query = "insert into powergeneratortransactions(generator_id, person_id, tquantity, tunit_price, trans_total, date_completed) " \
                "values (%s, %s, %s, %s, %s, %s) " \
                "returning generator_trans_id;"
        cursor.execute(query, (generator_id, person_id, tquantity, tunit_price, trans_total, date_completed,))
        tid = cursor.fetchone()[0]
        self.conn.commit()
        return tid

    def delete(self, tid):
        cursor = self.conn.cursor()
        query = "delete from powergeneratortransactions " \
                "where generator_trans_id = %s;"
        cursor.execute(query, (tid,))
        self.conn.commit()
        return tid
