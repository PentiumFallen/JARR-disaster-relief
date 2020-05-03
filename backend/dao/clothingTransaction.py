from backend.config.dbconfig import pg_config
import psycopg2


class ClothingTransactionDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllClothingTransactions(self):
        cursor = self.conn.cursor()
        query = "select * from clothingtransactions"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionById(self, tid):
        cursor = self.conn.cursor()
        query = "select * from clothingtransactions where clothing_trans_id = %s;"
        cursor.execute(query, tid)
        result = cursor.fetchone()
        return result

    def getTransactionByFulfillerID(self, pid):
        cursor = self.conn.cursor()
        query = "select * from clothingtransactions where person_id = %s"
        cursor.execute(query, pid)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByFulfillerEmail(self, email):
        cursor = self.conn.cursor()
        query = "select * from clothingtransactions inner join persons inner join account " \
                "where email = %s;"
        cursor.execute(query, email)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByFulfillerName(self, first, last):
        cursor = self.conn.cursor()
        query = "select * " \
                "from clothingtransactions inner join persons " \
                "where first_name = %s" \
                "and last_name = %s;"
        cursor.execute(query, first, last)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPost(self, clothing_id):
        cursor = self.conn.cursor()
        query = "select * " \
                "from clothingtransactions " \
                "where clothing_id = %s;"
        cursor.execute(query, clothing_id)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPosterEmail(self, email):
        cursor = self.conn.cursor()
        query = "select * " \
                "from clothingtransactions as t inner join clothing as r " \
                "where r.person_id = (" \
                "select person_id " \
                "from account inner join persons inner join clothing " \
                "where email = %s);"
        cursor.execute(query, email)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPosterName(self, first, last):
        cursor = self.conn.cursor()
        query = "select * " \
                "from clothingtransactions as t inner join clothing as r " \
                "where r.person_id = (" \
                "select person_id " \
                "from account inner join persons inner join clothing " \
                "where first_name = %s " \
                "and last_name = %s);"
        cursor.execute(query, first, last)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, clothing_id, person_id, tquantity, tunit_price, trans_total, date_completed):
        cursor = self.conn.cursor()
        query = "insert into clothingtransactions(clothing_id, person_id, tquantity, tunit_price, trans_total, date_completed) " \
                "values (%s, %s, %s, %s, %s, %s) " \
                "returning clothing_trans_id;"
        cursor.execute(query, (clothing_id, person_id, tquantity, tunit_price, trans_total, date_completed,))
        tid = cursor.fetchone()[0]
        self.conn.commit()
        return tid

    def delete(self, tid):
        cursor = self.conn.cursor()
        query = "delete from clothingtransactions " \
                "where clothing_trans_id = %s;"
        cursor.execute(query, (tid,))
        self.conn.commit()
        return tid
