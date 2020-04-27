from backend.config.dbconfig import pg_config
import psycopg2


class SupplyDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Supply;"
        cursor.execute(query)
        result = cursor.fetchall()
        # for row in cursor:
        #     result.append(row)
        return result

    def getSupplyById(self, sid):
        cursor = self.conn.cursor()
        query = "select * from Supply where supply_id = %s;"
        cursor.execute(query, (sid,))
        result = cursor.fetchone()
        return result

    def getSuppliesByCategory(self, category):
        cursor = self.conn.cursor()
        query = "select * from Supply where scategory = %s;"
        cursor.execute(query, (category,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSuppliesByAddress(self, address):
        cursor = self.conn.cursor()
        query = "select * from Supply where saddress = %s;"
        cursor.execute(query, (address,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSuppliesByCategoryAndAddress(self, category, address):
        cursor = self.conn.cursor()
        query = "select * from Supply where scategory = %s and saddress = %s;"
        cursor.execute(query, (category, address))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSuppliesByCategoryAndMaxPrice(self, category, max_price):
        cursor = self.conn.cursor()
        query = "select * from Supply where scategory = %s and sprice <= %s;"
        cursor.execute(query, (category, max_price))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSuppliesByCategoryAddressAndMaxPrice(self, category, address, max_price):
        cursor = self.conn.cursor()
        query = "select * from Supply where scategory = %s and saddress = %s and sprice <= %s;"
        cursor.execute(query, (category, address, max_price))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Supply natural inner join supplies where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, scategory, sdescription, saddress, sprice, date_offered, squantity, person_id):
        cursor = self.conn.cursor()

        query = "insert into Supply(scategory, sdescription, saddress, sprice) values (%s, %s, %s, %s) returning supply_id;"
        cursor.execute(query, (scategory, sdescription, saddress, sprice,))

        supply_id = cursor.fetchone()[0]

        query2 = "insert into Supply(date_offered, squantity, person_id, supply_id) values (%s, %s, %s, %s)"
        cursor.execute(query2, (date_offered, squantity, person_id, supply_id,))

        self.conn.commit()
        return supply_id

    # Shouldn't use!
    def delete(self, supply_id):
        cursor = self.conn.cursor()
        query = "delete from Supply where supply_id = %s;"
        cursor.execute(query, (supply_id,))
        self.conn.commit()
        return supply_id

    def update(self, supply_id, scategory, sdescription, saddress, sprice):
        cursor = self.conn.cursor()
        query = "update Supply set scategory = %s, sdescription = %s, saddress = %s, sprice = %s where supply_id = %s;"
        cursor.execute(query, (scategory, sdescription, saddress, sprice, supply_id,))
        self.conn.commit()
        return supply_id

    def getCountBySupplyCategory(self):
        cursor = self.conn.cursor()
        query = "select scategory, sum(squantity) from Supply natural inner join Supplies group by scategory, scategory order by scategory;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
