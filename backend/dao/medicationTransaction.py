from backend.config.dbconfig import pg_config
import psycopg2

class MedicationTransactionDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllMedicationTransactions(self):
        cursor = self.conn.cursor()
        query = "select med_trans_id, med_id as initial_post, person_id as fulfiller " \
                "from medicationTransactions;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionById(self, tid):
        cursor = self.conn.cursor()
        query = "select med_trans_id, med_id as initial_post, person_id as fulfiller " \
                "from medicationTransactions " \
                "where med_trans_id = %s;"
        cursor.execute(query, tid)
        result = cursor.fetchone()
        return result

    def getTransactionByFulfillerID(self, pid):
        cursor = self.conn.cursor()
        query = "select med_trans_id, med_id as initial_post, tquantity as quantity, trans_total as total, date_completed " \
                "from medicationTransactions " \
                "where person_id = %s;"
        cursor.execute(query, pid)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByFulfillerEmail(self, email):
        cursor = self.conn.cursor()
        query = "select med_trans_id, med_id as initial_post, tquantity as quantity, trans_total as total, date_completed " \
                "from medicationTransactions inner join persons inner join account " \
                "where email = %s;"
        cursor.execute(query, email)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByFulfillerName(self, first, last):
        cursor = self.conn.cursor()
        query = "select med_trans_id, med_id as initial_post, tquantity as quantity, trans_total as total, date_completed " \
                "from medicationTransactions inner join persons " \
                "where first_name = %s " \
                "or last_name = %s;"
        cursor.execute(query, first, last)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPost(self, wid):
        cursor = self.conn.cursor()
        query = "select med_trans_id, person_id as fulfiller, tquantity as quantity, trans_total as total, date_completed " \
                "from medicationTransactions " \
                "where med_id = %s;"
        cursor.execute(query, wid)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPosterEmail(self, email):
        cursor = self.conn.cursor()
        query = "select med_trans_id, person_id as fulfiller, tquantity as quantity, trans_total as total, date_completed " \
                "from medicationTransactions as t inner join medications as w " \
                "where w.person_id = (" \
                "select person_id " \
                "from account inner join persons inner join medications " \
                "where email = %s);"
        cursor.execute(query, email)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPosterName(self, first, last):
        cursor = self.conn.cursor()
        query = "select med_trans_id, person_id as fulfiller, tquantity as quantity, trans_total as total, date_completed " \
                "from medicationTransactions as t inner join medications as w " \
                "where w.person_id = (" \
                "select person_id " \
                "from account inner join persons inner join medications " \
                "where first_name = %s " \
                "or last_name = %s);"
        cursor.execute(query, first, last)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByMaxCost(self, cost):
        cursor = self.conn.cursor()
        query = "select med_trans_id, med_id as initial_post, person_id as fulfiller, trans_total as total, date_completed " \
                "from medicationTransactions " \
                "where trans_total <= %s;"
        cursor.execute(query, cost)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByMinCost(self, cost):
        cursor = self.conn.cursor()
        query = "select med_trans_id, med_id as initial_post, person_id as fulfiller, trans_total as total, date_completed " \
                "from medicationTransactions " \
                "where trans_total >= %s;"
        cursor.execute(query, cost)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByMaxQuantity(self, quantity):
        cursor = self.conn.cursor()
        query = "select med_trans_id, med_id as initial_post, person_id as fulfiller, tquantity as quantity, date_completed " \
                "from medicationTransactions " \
                "where tquantity <= %s;"
        cursor.execute(query, quantity)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByMinQuantity(self, quantity):
        cursor = self.conn.cursor()
        query = "select med_trans_id, med_id as initial_post, person_id as fulfiller, tquantity as quantity, date_completed " \
                "from medicationTransactions " \
                "where tquantity >= %s;"
        cursor.execute(query, quantity)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, med_id, person_id, tquantity, tunit_price, trans_total):
        cursor = self.conn.cursor()
        query = "insert into medicationTransactions(med_id, person_id, tquantity, tunit_price, trans_total) " \
                "values (%s, %s, %s, %s, %s, %s) " \
                "returning med_trans_id;"
        cursor.execute(query, (med_id, person_id, tquantity, tunit_price, trans_total,))
        tid = cursor.fetchone()[0]
        self.conn.commit()
        return tid

    def delete(self, tid):
        cursor = self.conn.cursor()
        query = "delete from medicationTransactions " \
                "where med_trans_id = %s;"
        cursor.execute(query, (tid,))
        self.conn.commit()
        return tid

    def update(self, tid, med_id, person_id, tquantity, tunit_price, trans_total):
        cursor = self.conn.cursor()
        query = "update medicationTransactions " \
                "set med_id = %s, person_id = %s, tquantity = %s, tunit_price = %s, trans_total = %s " \
                "where med_trans_id = %s;"
        cursor.execute(query, (med_id, person_id, tquantity, tunit_price, trans_total, tid,))
        self.conn.commit()
        return tid