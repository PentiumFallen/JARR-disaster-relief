from config.dbconfig import pg_config
import psycopg2

class PersonDao:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllPersons(self):
        cursor = self.conn.cursor()
        query = "select * from person;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPersonById(self, pid):
        cursor = self.conn.cursor()
        query = "select first_name, last_name, address, senate_district, phone_number, current_location from person where person_id = %s;"
        cursor.execute(query, (pid,))
        result = cursor.fetchone()
        return result

    def insertPerson(self, first_name, last_name, address, senate_district, phone_number, current_location):
        cursor = self.conn.cursor()
        "select first_name, last_name, address, senate_district, phone_number, current_location from person where person_id = %s;"
        query = "insert into person(first_name, last_name, address, senate_district, phone_number, current_location) values (%s, %s, %s, %s, %s, %s, %s) returning person_id;"
        cursor.execute(query, (first_name, last_name, address, senate_district, phone_number, current_location,))
        person_id = cursor.fetchone()[0]
        self.conn.commit()
        return person_id

    def deletePerson(self, person_id):
        cursor = self.conn.cursor()
        query = "delete from person where person_id = %s;"
        cursor.execute(query, (person_id,))
        self.conn.commit()
        return person_id

    def updatePersonLocation(self, new_location, person_id):
        cursor = self.conn.cursor()
        query = "update person set current_location = %s where person_id = %s;"
        cursor.execute(query, (new_location, person_id))
        self.conn.commit()
        return person_id

    def updatePerson(self, first_name, last_name, address, senate_district, phone_number, current_location, person_id):
        cursor = self.conn.cursor()
        query = "update person set first_name = %s, last_name = %s, address = %s, senate_district = %s, phone_number = %s, current_location = %s, phone_number = %s where person_id = %s;"
        cursor.execute(query, (first_name, last_name, municipality, zip_code, address, senate_district, phone_number, person_id,))
        self.conn.commit()
        return person_id

