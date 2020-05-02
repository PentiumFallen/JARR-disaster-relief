from backend.config.dbconfig import pg_config
import psycopg2

class WaterDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllWater(self):
        cursor = self.conn.cursor()
        query = "select * from Water;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllWaterSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Water where is_supply = TRUE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllWaterRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Water where is_supply = FALSE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableWaterSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Water where is_supply = TRUE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUnfulfilledWaterRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Water where is_supply = FALSE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getWaterById(self, water_id):
        cursor = self.conn.cursor()
        query = "select * from Water where water_id = %s;"
        cursor.execute(query, (water_id,))
        result = cursor.fetchone()
        return result

    def getWaterByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Water where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getWaterSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Water where person_id = %s and is_supply = TRUE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getWaterRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Water where person_id = %s and is_supply = FALSE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getWaterByBrandAndType(self, brand, water_type):
        cursor = self.conn.cursor()
        query = "select * from Water where brand = %s and water_id = (select water_id from Water_Type where water_type = %s);"
        cursor.execute(query, (brand, water_type))
        result = cursor.fetchall()
        return result

    def getWaterByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Water where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getWaterByType(self, water_type):
        cursor = self.conn.cursor()
        query = "select * from Water where water_id = (select water_id from Water_Type where water_type = %s);"
        cursor.execute(query, (water_type,))
        result = cursor.fetchall()
        return result

    def getWaterSuppliesByBrandAndTypeAndMaxPrice(self, brand, water_type, max_price):
        cursor = self.conn.cursor()
        query = "select * from Water where brand = %s and unit_price <= %s and is_supply = TRUE and water_id = " \
                "(select water_id from Water_Type where water_type = %s);"
        cursor.execute(query, (brand, max_price, water_type))
        result = cursor.fetchall()
        return result

    def getWaterSuppliesByBrandAndType(self, brand, water_type):
        cursor = self.conn.cursor()
        query = "select * from Water where brand = %s and is_supply = TRUE and water_id = " \
                "(select water_id from Water_Type where water_type = %s);"
        cursor.execute(query, (brand, water_type))
        result = cursor.fetchall()
        return result

    def getWaterSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Water where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getWaterSuppliesByType(self, water_type):
        cursor = self.conn.cursor()
        query = "select * from Water where is_supply = TRUE and water_id = " \
                "(select water_id from Water_Type where water_type = %s);"
        cursor.execute(query, (water_type,))
        result = cursor.fetchall()
        return result

    def getWaterSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select * from Water where is_supply = TRUE and unit_price <= %s;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getWaterRequestsByBrandAndType(self, brand, water_type):
        cursor = self.conn.cursor()
        query = "select * from Water where brand = %s and is_supply = FALSE and water_id = " \
                "(select water_id from Water_Type where water_type = %s);"
        cursor.execute(query, (brand, water_type))
        result = cursor.fetchall()
        return result

    def getWaterRequestsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Water where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getWaterRequestsByType(self, water_type):
        cursor = self.conn.cursor()
        query = "select * from Water where is_supply = FALSE and water_id = " \
                "(select water_id from Water_Type where water_type = %s);"
        cursor.execute(query, (water_type,))
        result = cursor.fetchall()
        return result

    def getWaterTypeId(self, water_type):
        cursor = self.conn.cursor()
        query = "select water_id from Water_Type natural where water_type = %s;"
        cursor.execute(query, (water_type,))
        result = cursor.fetchall()
        return result

    def insert(self, person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
               is_supply, type_id, address_id):
        cursor = self.conn.cursor()

        query = "insert into Water(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity, " \
                "is_supply, type_id, address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning supply_id;"
        cursor.execute(query, (person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, type_id, address_id))

        water_id = cursor.fetchone()[0]

        self.conn.commit()
        return water_id

    def delete(self, water_id):
        cursor = self.conn.cursor()
        query = "update Water set curr_quantity = 0 where water_id = %s;"
        cursor.execute(query, (water_id,))
        self.conn.commit()
        return water_id

    def update(self, water_id, brand, description, unit_price, curr_quantity, type_id, address_id):
        cursor = self.conn.cursor()
        query = "update Water set brand = %s, description = %s, unit_price = %s, curr_quantity = %s, type_id = %s, " \
                "address_id = %s where water_id = %s;"
        cursor.execute(query, (brand, description, unit_price, curr_quantity, type_id, address_id, water_id))
        self.conn.commit()
        return water_id
