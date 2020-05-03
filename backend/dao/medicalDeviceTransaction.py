from backend.config.dbconfig import pg_config
import psycopg2

class MedicalDeviceTransactionDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllMedicalDeviceTransactions(self):
        cursor = self.conn.cursor()
        query = "select * from medicaldevicetransaction"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionById(self, tid):
        cursor = self.conn.cursor()
        query = "select * from medicaldevicetransaction where med_dev_trans_id = %s;"
        cursor.execute(query, tid)
        result = cursor.fetchone()
        return result

    def getTransactionByFulfillerID(self, pid):
        cursor = self.conn.cursor()
        query = "select * from medicaldevicetransaction where person_id = %s"
        cursor.execute(query, pid)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByFulfillerEmail(self, email):
        cursor = self.conn.cursor()
        query = "select * from medicaldevicetransaction inner join persons inner join account " \
                "where email = %s;"
        cursor.execute(query, email)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByFulfillerName(self, first, last):
        cursor = self.conn.cursor()
        query = "select * " \
                "from medicaldevicetransaction inner join persons " \
                "where first_name = %s" \
                "and last_name = %s;"
        cursor.execute(query, first, last)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPost(self, wid):
        cursor = self.conn.cursor()
        query = "select * " \
                "from medicaldevicetransaction " \
                "where cf_id = %s;"
        cursor.execute(query, wid)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPosterEmail(self, email):
        cursor = self.conn.cursor()
        query = "select * " \
                "from medicaldevicetransaction as t inner join medicaldevice as w " \
                "where w.person_id = (" \
                "select person_id " \
                "from account inner join persons inner join medicaldevice " \
                "where email = %s);"
        cursor.execute(query, email)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTransactionByInitialPosterName(self, first, last):
        cursor = self.conn.cursor()
        query = "select * " \
                "from medicaldevicetransaction as t inner join medicaldevice as w " \
                "where w.person_id = (" \
                "select person_id " \
                "from account inner join persons inner join medicaldevice " \
                "where first_name = %s " \
                "and last_name = %s);"
        cursor.execute(query, first, last)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, medical_dev_id, person_id, tquantity, tunit_price, trans_total, date_completed):
        cursor = self.conn.cursor()
        query = "insert into medicaldevicetransaction(medical_dev_id, person_id, tquantity, tunit_price, trans_total, date_completed) " \
                "values (%s, %s, %s, %s, %s, %s) " \
                "returning med_dev_trans_id;"
        cursor.execute(query, (medical_dev_id, person_id, tquantity, tunit_price, trans_total, date_completed,))
        tid = cursor.fetchone()[0]
        self.conn.commit()
        return tid

    def delete(self, tid):
        cursor = self.conn.cursor()
        query = "delete from medicaldevicetransaction " \
                "where med_dev_trans_id = %s;"
        cursor.execute(query, (tid,))
        self.conn.commit()
        return tid

    # def update(self, cf_id, person_id, tquantity, tunit_price, trans_total, tid):
    #     cursor = self.conn.cursor()
    #     query = "update medicaldevicetransaction " \
    #             "set person_id = %s, tquantity = %s, tunit_price = %s, trans_total = %s " \
    #             "where med_dev_trans_id = %s;"
    #     cursor.execute(query, (cf_id, person_id, tquantity, tunit_price, trans_total, tid,))
    #     self.conn.commit()
    #     return tid