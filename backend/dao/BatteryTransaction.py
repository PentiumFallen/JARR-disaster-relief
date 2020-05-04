from backend.config.dbconfig import pg_config
import psycopg2


class BatteryTransactionDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllBatteryTransactions(self):
        cursor = self.conn.cursor()
        query = "select * from batterytransactions"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionById(self, tid):
        cursor = self.conn.cursor()
        query = "select * from batterytransactions where battery_trans_id = %s;"
        cursor.execute(query, tid)
        result = cursor.fetchone()
        return result

    def getTransactionByFulfillerID(self, pid):
        cursor = self.conn.cursor()
        query = "select * from batterytransactions where person_id = %s"
        cursor.execute(query, pid)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByFulfillerEmail(self, email):
        cursor = self.conn.cursor()
        query = "select * from batterytransactions inner join persons inner join account " \
                "where email = %s;"
        cursor.execute(query, email)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByFulfillerName(self, first, last):
        cursor = self.conn.cursor()
        query = "select * " \
                "from batterytransactions inner join persons " \
                "where first_name = %s" \
                "and last_name = %s;"
        cursor.execute(query, first, last)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPost(self, battery_id):
        cursor = self.conn.cursor()
        query = "select * " \
                "from batterytransactions " \
                "where battery_id = %s;"
        cursor.execute(query, battery_id)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPosterEmail(self, email):
        cursor = self.conn.cursor()
        query = "select * " \
                "from batterytransactions as t inner join battery as r " \
                "where r.person_id = (" \
                "select person_id " \
                "from account inner join persons inner join battery " \
                "where email = %s);"
        cursor.execute(query, email)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPosterName(self, first, last):
        cursor = self.conn.cursor()
        query = "select * " \
                "from batterytransactions as t inner join battery as r " \
                "where r.person_id = (" \
                "select person_id " \
                "from account inner join persons inner join battery " \
                "where first_name = %s " \
                "and last_name = %s);"
        cursor.execute(query, first, last)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, battery_id, person_id, tquantity, tunit_price, trans_total, date_completed):
        cursor = self.conn.cursor()
        query = "insert into batterytransactions(battery_id, person_id, tquantity, tunit_price, trans_total, date_completed) " \
                "values (%s, %s, %s, %s, %s, %s) " \
                "returning battery_trans_id;"
        cursor.execute(query, (battery_id, person_id, tquantity, tunit_price, trans_total, date_completed,))
        tid = cursor.fetchone()[0]
        self.conn.commit()
        return tid

    def delete(self, tid):
        cursor = self.conn.cursor()
        query = "delete from batterytransactions " \
                "where battery_trans_id = %s;"
        cursor.execute(query, (tid,))
        self.conn.commit()
        return tid
