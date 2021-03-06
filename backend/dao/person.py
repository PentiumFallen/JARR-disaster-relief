from backend.config.dbconfig import pg_config
import psycopg2


class PersonDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['passwd'],
                                                                    pg_config['host'])
        self.conn = psycopg2._connect(connection_url)

    def getAllPersons(self):
        cursor = self.conn.cursor()
        query = "select * from \"Persons\";"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPersonById(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from \"Persons\" where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchone()
        return result

    def getPersonBySupplyId(self, supply_id):
        cursor = self.conn.cursor()
        query = "select * from \"Persons\" natural inner join supplies where supply_id = %s;"
        cursor.execute(query, (supply_id,))
        result = cursor.fetchone()
        return result

    def getPersonByRequestId(self, supply_id):
        cursor = self.conn.cursor()
        query = "select * from \"Persons\" natural inner join requests where request_id = %s;"
        cursor.execute(query, (supply_id,))
        result = cursor.fetchone()
        return result

    def insertPerson(self, first_name, last_name, address_id):
        cursor = self.conn.cursor()
        query = "insert into \"Persons\"(first_name, last_name, address_id) values (%s, %s, %s) returning person_id;"
        cursor.execute(query, (first_name, last_name, address_id,))
        person_id = cursor.fetchone()[0]
        self.conn.commit()
        return person_id

    def deletePerson(self, person_id):
        cursor = self.conn.cursor()
        query = "delete from \"Persons\" where person_id = %s;"
        cursor.execute(query, (person_id,))
        self.conn.commit()
        return person_id

    def updatePerson(self, first_name, last_name, phone_number, person_id):
        cursor = self.conn.cursor()
        query = "update \"Persons\" set first_name = %s, last_name = %s, phone_number = %s where person_id = %s;"
        cursor.execute(query, (first_name, last_name, phone_number, person_id,))
        self.conn.commit()
        return person_id
