from backend.config.dbconfig import pg_config
import psycopg2

class FuelTransactionDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllFuelTransactions(self):
        cursor = self.conn.cursor()
        query = "select fuel_trans_id, fuel_id as initial_post, person_id as fulfiller " \
                "from fuelTransactions;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionById(self, tid):
        cursor = self.conn.cursor()
        query = "select fuel_trans_id, fuel_id as initial_post, person_id as fulfiller " \
                "from fuelTransactions " \
                "where fuel_trans_id = %s;"
        cursor.execute(query, tid)
        result = cursor.fetchone()
        return result

    def getTransactionByFulfillerID(self, pid):
        cursor = self.conn.cursor()
        query = "select fuel_trans_id, fuel_id as initial_post, tquantity as quantity, trans_total as total, date_completed " \
                "from fuelTransactions " \
                "where person_id = %s;"
        cursor.execute(query, pid)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByFulfillerEmail(self, email):
        cursor = self.conn.cursor()
        query = "select fuel_trans_id, fuel_id as initial_post, tquantity as quantity, trans_total as total, date_completed " \
                "from fuelTransactions inner join persons inner join account " \
                "where email = %s;"
        cursor.execute(query, email)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByFulfillerName(self, first, last):
        cursor = self.conn.cursor()
        query = "select fuel_trans_id, fuel_id as initial_post, tquantity as quantity, trans_total as total, date_completed " \
                "from fuelTransactions inner join persons " \
                "where first_name = %s " \
                "or last_name = %s;"
        cursor.execute(query, first, last)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPost(self, wid):
        cursor = self.conn.cursor()
        query = "select fuel_trans_id, person_id as fulfiller, tquantity as quantity, trans_total as total, date_completed " \
                "from fuelTransactions " \
                "where fuel_id = %s;"
        cursor.execute(query, wid)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPosterEmail(self, email):
        cursor = self.conn.cursor()
        query = "select fuel_trans_id, person_id as fulfiller, tquantity as quantity, trans_total as total, date_completed " \
                "from fuelTransactions as t inner join fuel as w " \
                "where w.person_id = (" \
                "select person_id " \
                "from account inner join persons inner join fuel " \
                "where email = %s);"
        cursor.execute(query, email)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPosterName(self, first, last):
        cursor = self.conn.cursor()
        query = "select fuel_trans_id, person_id as fulfiller, tquantity as quantity, trans_total as total, date_completed " \
                "from fuelTransactions as t inner join fuel as w " \
                "where w.person_id = (" \
                "select person_id " \
                "from account inner join persons inner join fuel " \
                "where first_name = %s " \
                "or last_name = %s);"
        cursor.execute(query, first, last)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByMaxCost(self, cost):
        cursor = self.conn.cursor()
        query = "select fuel_trans_id, fuel_id as initial_post, person_id as fulfiller, trans_total as total, date_completed " \
                "from fuelTransactions " \
                "where trans_total <= %s;"
        cursor.execute(query, cost)
        result = cursor.fetchone()
        return result

    def getTransactionByMinCost(self, cost):
        cursor = self.conn.cursor()
        query = "select fuel_trans_id, fuel_id as initial_post, person_id as fulfiller, trans_total as total, date_completed " \
                "from fuelTransactions " \
                "where trans_total >= %s;"
        cursor.execute(query, cost)
        result = cursor.fetchone()
        return result

    def getTransactionByMaxQuantity(self, quantity):
        cursor = self.conn.cursor()
        query = "select fuel_trans_id, fuel_id as initial_post, person_id as fulfiller, tquantity as quantity, date_completed " \
                "from fuelTransactions " \
                "where tquantity <= %s;"
        cursor.execute(query, quantity)
        result = cursor.fetchone()
        return result

    def getTransactionByMinQuantity(self, quantity):
        cursor = self.conn.cursor()
        query = "select fuel_trans_id, fuel_id as initial_post, person_id as fulfiller, tquantity as quantity, date_completed " \
                "from fuelTransactions " \
                "where tquantity >= %s;"
        cursor.execute(query, quantity)
        result = cursor.fetchone()
        return result

    def insert(self, fuel_id, person_id, tquantity, tunit_price, trans_total, date_completed):
        cursor = self.conn.cursor()
        query = "insert into fuelTransactions(fuel_id, person_id, tquantity, tunit_price, trans_total, date_completed) " \
                "values (%s, %s, %s, %s, %s, %s) " \
                "returning fuel_trans_id;"
        cursor.execute(query, (fuel_id, person_id, tquantity, tunit_price, trans_total, date_completed,))
        tid = cursor.fetchone()[0]
        self.conn.commit()
        return tid

    def delete(self, tid):
        cursor = self.conn.cursor()
        query = "delete from fuelTransactions " \
                "where fuel_trans_id = %s;"
        cursor.execute(query, (tid,))
        self.conn.commit()
        return tid

    def update(self, tid, fuel_id, person_id, tquantity, tunit_price, trans_total):
        cursor = self.conn.cursor()
        query = "update fuelTransactions " \
                "set fuel_id = %s, person_id = %s, tquantity = %s, tunit_price = %s, trans_total = %s " \
                "where fuel_trans_id = %s;"
        cursor.execute(query, (fuel_id, person_id, tquantity, tunit_price, trans_total, tid,))
        self.conn.commit()
        return tid