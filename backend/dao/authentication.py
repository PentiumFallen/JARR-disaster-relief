from backend.config.dbconfig import pg_config
import psycopg2

class AuthenticationDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllAuthenticationByEmail(self):
        cursor = self.conn.cursor()
        query = "select * from accounts where email = %s;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getAccountData(self, email, password):
        cursor = self.conn.cursor()
        query = "select * from accounts where email = %s and password = %s;"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        return result
    
    def getAccountType(self, account_id):
        cursor = self.conn.cursor()
        query = "select is_admin from accounts where account_id = %s;"
        cursor.execute(query, account_id)
        result = cursor.fetchone()
        return result

    def insertAccount(self, json):
        email = json['email']
        password = json['password']
        is_admin = json['is_admin']
        cursor = self.conn.cursor()
        query = "insert into accounts(email, password, is_admin) values (%s, %s, %s) returning account_id;"
        cursor.execute(query, (email, password, is_admin,))
        self.conn.commit()
        result = cursor.fetchone()
        return result
    
    def deleteAccount(self, account_id):
        cursor = self.conn.cursor()
        query = "delete from account where account_id = %s;"
        cursor.execute(query, (account_id,))
        self.conn.commit()
        return account_id

    def accountChangePassword(self, email,password):
        cursor = self.conn.cursor()
        query = "update accounts set password =%s  where email = %s;"
        cursor.execute(query, (password,email))
        self.conn.commit()
        return'Password as been change'
    
    def accountLogin(self, email,password):
        cursor = self.conn.cursor()
        query = "select * from accounts where email = %s and password = %s;"
        cursor.execute(query, (email,password,))
        result = []
        for row in cursor:
            result.append(row)
        return result


    
    
    
