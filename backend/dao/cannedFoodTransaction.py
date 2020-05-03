from backend.config.dbconfig import pg_config
import psycopg2

class CannedFoodTransactionDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllCannedFoodTransactions(self):
        cursor = self.conn.cursor()
        query = "select cf_trans_id, cf_id as initial_post, person_id as fulfiller " \
                "from cannedFoodTransactions;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionById(self, tid):
        cursor = self.conn.cursor()
        query = "select cf_trans_id, cf_id as initial_post, person_id as fulfiller " \
                "from cannedFoodTransactions " \
                "where cf_trans_id = %s;"
        cursor.execute(query, tid)
        result = cursor.fetchone()
        return result

    def getTransactionByFulfillerID(self, pid):
        cursor = self.conn.cursor()
        query = "select cf_trans_id, cf_id as initial_post, tquantity as quantity, trans_total as total, date_completed " \
                "from cannedFoodTransactions " \
                "where person_id = %s;"
        cursor.execute(query, pid)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByFulfillerEmail(self, email):
        cursor = self.conn.cursor()
        query = "select cf_trans_id, cf_id as initial_post, tquantity as quantity, trans_total as total, date_completed " \
                "from cannedFoodTransactions inner join persons inner join account " \
                "where email = %s;"
        cursor.execute(query, email)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByFulfillerName(self, first, last):
        cursor = self.conn.cursor()
        query = "select cf_trans_id, cf_id as initial_post, tquantity as quantity, trans_total as total, date_completed " \
                "from cannedFoodTransactions inner join persons " \
                "where first_name = %s" \
                "or last_name = %s;"
        cursor.execute(query, first, last)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPost(self, wid):
        cursor = self.conn.cursor()
        query = "select cf_trans_id, person_id as fulfiller, tquantity as quantity, trans_total as total, date_completed " \
                "from cannedFoodTransactions " \
                "where cf_id = %s;"
        cursor.execute(query, wid)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPosterEmail(self, email):
        cursor = self.conn.cursor()
        query = "select cf_trans_id, person_id as fulfiller, tquantity as quantity, trans_total as total, date_completed " \
                "from cannedFoodTransactions as t inner join cannedFoods as w " \
                "where w.person_id = (" \
                "select person_id " \
                "from account inner join persons inner join cannedFoods " \
                "where email = %s);"
        cursor.execute(query, email)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPosterName(self, first, last):
        cursor = self.conn.cursor()
        query = "select cf_trans_id, person_id as fulfiller, tquantity as quantity, trans_total as total, date_completed " \
                "from cannedFoodTransactions as t inner join cannedFoods as w " \
                "where w.person_id = (" \
                "select person_id " \
                "from account inner join persons inner join cannedFoods " \
                "where first_name = %s " \
                "or last_name = %s);"
        cursor.execute(query, first, last)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByMaxCost(self, cost):
        cursor = self.conn.cursor()
        query = "select cf_trans_id, cf_id as initial_post, person_id as fulfiller, trans_total as total, date_completed " \
                "from cannedFoodTransactions " \
                "where trans_total <= %s;"
        cursor.execute(query, cost)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByMinCost(self, cost):
        cursor = self.conn.cursor()
        query = "select cf_trans_id, cf_id as initial_post, person_id as fulfiller, trans_total as total, date_completed " \
                "from cannedFoodTransactions " \
                "where trans_total >= %s;"
        cursor.execute(query, cost)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByMaxQuantity(self, quantity):
        cursor = self.conn.cursor()
        query = "select cf_trans_id, cf_id as initial_post, person_id as fulfiller, tquantity as quantity, date_completed " \
                "from cannedFoodTransactions " \
                "where tquantity <= %s;"
        cursor.execute(query, quantity)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByMinQuantity(self, quantity):
        cursor = self.conn.cursor()
        query = "select cf_trans_id, cf_id as initial_post, person_id as fulfiller, tquantity as quantity, date_completed " \
                "from cannedFoodTransactions " \
                "where tquantity >= %s;"
        cursor.execute(query, quantity)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, cf_id, person_id, tquantity, tunit_price, trans_total, date_completed):
        cursor = self.conn.cursor()
        query = "insert into cannedFoodTransactions(cf_id, person_id, tquantity, tunit_price, trans_total, date_completed) " \
                "values (%s, %s, %s, %s, %s, %s) " \
                "returning cf_trans_id;"
        cursor.execute(query, (cf_id, person_id, tquantity, tunit_price, trans_total, date_completed,))
        tid = cursor.fetchone()[0]
        self.conn.commit()
        return tid

    def delete(self, tid):
        cursor = self.conn.cursor()
        query = "delete from cannedFoodTransactions " \
                "where cf_trans_id = %s;"
        cursor.execute(query, (tid,))
        self.conn.commit()
        return tid

    def update(self, tid, cf_id, person_id, tquantity, tunit_price, trans_total):
        cursor = self.conn.cursor()
        query = "update cannedFoodTransactions " \
                "set cf_id = %s, person_id = %s, tquantity = %s, tunit_price = %s, trans_total = %s " \
                "where cf_trans_id = %s;"
        cursor.execute(query, (cf_id, person_id, tquantity, tunit_price, trans_total, tid,))
        self.conn.commit()
        return tid