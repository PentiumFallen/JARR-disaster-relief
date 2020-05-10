from backend.config.dbconfig import pg_config
import psycopg2

class AccountDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllAccountById(self):
        cursor = self.conn.cursor()
        query = "select account_id, email, password, registered_date, is_admin, balance, person_id " \
                "bank_account_number, routing_number from Accounts where account_id = %s;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAdminAccount(self, is_admin):
        cursor = self.conn.cursor()
        query = "select account_id, email, password, registered_date, is_admin, balance, person_id " \
                "bank_account_number, routing_number from Accounts where is_admin = TRUE;"
        cursor.execute(query, (is_admin,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAccountByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select account_id, email, password, registered_date, is_admin, balance, person_id " \
                "bank_account_number, routing_number from Accounts where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getAccountByEmail(self, email):
        cursor = self.conn.cursor()
        query = "select account_id, email, password, registered_date, is_admin, balance, person_id " \
                "bank_account_number, routing_number from Accounts where email = %s;"
        cursor.execute(query, (email,))
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getAccountData(self, email, password):
        cursor = self.conn.cursor()
        query = "select email, password, registered_date, is_admin, balance " \
                "bank_account_number, routing_number from Accounts where email = %s and password = %s;"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        return result
    
    def getAccountType(self, account_id):
        cursor = self.conn.cursor()
        query = "select is_admin from Accounts where account_id = %s;"
        cursor.execute(query, (account_id,))
        result = cursor.fetchone()
        return result

    def insertAccount(self, person_id, email, password, registered_date, is_admin, balance, bank_account_number, routing_number):
        cursor = self.conn.cursor()
        query = "insert into Accounts(person_id, email, password, is_admin, registered_date, is_admin, balance, bank_account_number, routing_number) " \
                    "values (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning account_id;"
        cursor.execute(query, (person_id, email, password, registered_date, is_admin, balance, bank_account_number, routing_number,))
        self.conn.commit()
        result = cursor.fetchone()
        return result
    
    def deleteAccount(self, account_id):
        cursor = self.conn.cursor()
        query = "delete from Accounts where account_id = %s;"
        cursor.execute(query, (account_id,))
        self.conn.commit()
        return account_id

    def accountChangePassword(self, email, password):
        cursor = self.conn.cursor()
        query = "update Accounts set password = %s  where email = %s;"
        cursor.execute(query, (password, email))
        self.conn.commit()
        return'Password has been changed'
    
    def accountLogin(self, email,password):
        cursor = self.conn.cursor()
        query = "select * from Account where email = %s and password = %s;"
        cursor.execute(query, (email,password))
        result = []
        for row in cursor:
            result.append(row)
        return result


    
    
    