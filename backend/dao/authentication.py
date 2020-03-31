from config.dbconfig import pg_config
import psycopg2

class AuthenticationDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllAuthentication(self):
        cursor = self.conn.cursor()
        query = "select * from account;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAuthenticationById(self, id):
        cursor = self.conn.cursor()
        query = "select account_id, email, password, is_admin from requests where account_id = %s;"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        return result

    def getAuthenticationByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select account_id, email, password, is_admin from person where account_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchone()
        return result

    def getAuthenticationByRequestId(self, request_id):
        cursor = self.conn.cursor()
        query = "select account_id, email, password, is_admin from person where account_id = %s;"
        cursor.execute(query, (request_id,))
        result = cursor.fetchone()
        return result

    def getAuthenticationBySupplyId(self, supply_id):
        cursor = self.conn.cursor()
        query = "select account_id, email, password, is_admin from person where account_id = %s;"
        cursor.execute(query, (supply_id,))
        result = cursor.fetchone()
        return result

    def insertAccount(self, email, password, is_admin):
        cursor = self.conn.cursor()
        query = "insert into account(email, password, is_admin) values (%s, %s, %s) returning account_id;"
        cursor.execute(query, (email, password, is_admin,))
        account_id = cursor.fetchone()[0]
        self.conn.commit()
        return account_id

    def deleteAccount(self, account_id):
        cursor = self.conn.cursor()
        query = "delete from account where account_id = %s;"
        cursor.execute(query, (account_id,))
        self.conn.commit()
        return account_id

    def updateAccount(self, email, password, is_admin, account_id):
        cursor = self.conn.cursor()
        query = "update account set email = %s, password = %s, is_admin = %s;"
        cursor.execute(query, (email, password, is_admin, account_id,))
        self.conn.commit()
        return account_id