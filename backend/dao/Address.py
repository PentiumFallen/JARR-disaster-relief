from backend.config.dbconfig import pg_config
import psycopg2


class AddressDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAddressById(self, address_id):
        cursor = self.conn.cursor()
        query = "select * from Address where address_id = %s;"
        cursor.execute(query, (address_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # TODO wait for ER Review
    def getAddressByResourceId(self, resource_id):
        cursor = self.conn.cursor()
        query = "select * from Address natural inner join Location natural inner join Supplies where resource_id = %s;"
        cursor.execute(query, (resource_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # TODO wait for ER Review
    def getAddressByRequestId(self, request_id):
        cursor = self.conn.cursor()
        query = "select * from Address natural inner join Person natural inner join requests where resource_id = %s;"
        cursor.execute(query, (request_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result
