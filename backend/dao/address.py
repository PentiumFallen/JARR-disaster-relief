from backend.config.dbconfig import pg_config
from backend.utility import senate_district
import psycopg2


class AddressDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['passwd'],
                                                                    pg_config['host'])
        self.conn = psycopg2._connect(connection_url)

    def getAddressById(self, address_id):
        cursor = self.conn.cursor()
        query = "select * from \"Addresses\" where address_id = %s;"
        cursor.execute(query, (address_id,))
        result = cursor.fetchone()
        return result

    def getAddressIdFromAddressAndCityAndZipCode(self, address, city, zip_code):
        cursor = self.conn.cursor()
        query = "select address_id from \"Addresses\" where address = %s, city = %s, zip_code = %s;"
        cursor.execute(query, (address, city, zip_code))
        result = cursor.fetchone()[0]
        for row in cursor:
            result.append(row)
        return result

    # TODO wait for ER Review
    def getAddressBySupplyId(self, supply_id):
        cursor = self.conn.cursor()
        query = "select * from \"Addresses\" natural inner join \"Supplies\" where supply_id = %s;"
        cursor.execute(query, (supply_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # TODO wait for ER Review
    def getAddressByRequestId(self, request_id):
        cursor = self.conn.cursor()
        query = "select * from \"Addresses\" natural inner join \"Requests\" where request_id = %s;"
        cursor.execute(query, (request_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAddressIdByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select address_id from \"Persons\" natural inner join \"Addresses\" where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchone()[0]
        return result

    def insert(self, address, city, zip_code):
        cursor = self.conn.cursor()
        query = "insert into \"Addresses\"(address, city, district, zip_code) " \
                "values(%s,%s,%s,%s) returning address_id;"
        cursor.execute(query, (address, city, senate_district[city.lower()], zip_code))
        address_id = cursor.fetchone()[0]
        self.conn.commit()
        return address_id

    def update(self, address_id, address, city, zip_code):
        cursor = self.conn.cursor()
        query = "update \"Addresses\" set address = %s, city = %s, district = %s, zip_code = %s where address_id = %s;"
        cursor.execute(query, (address, city, senate_district[city.lower()], zip_code, address_id))
        self.conn.commit()
        return address_id
