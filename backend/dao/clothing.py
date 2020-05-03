from backend.config.dbconfig import pg_config
import psycopg2

class ClothingDAO:
    def __init__(self):

        connection_url = "dbType=%s user=%s password=%s" % (pg_config['dbType'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllClothing(self):
        cursor = self.conn.cursor()
        query = "select * from Clothing;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllClothingSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Clothing where is_supply = TRUE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllClothingRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Clothing where is_supply = FALSE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableClothingSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Clothing where is_supply = TRUE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUnfulfilledClothingRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Clothing where is_supply = FALSE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getClothingById(self, clothing_id):
        cursor = self.conn.cursor()
        query = "select * from Clothing where clothing_id = %s;"
        cursor.execute(query, (clothing_id,))
        result = cursor.fetchone()
        return result

    def getClothingByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Clothing where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getClothingSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Clothing where person_id = %s and is_supply = TRUE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getClothingRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Clothing where person_id = %s and is_supply = FALSE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getClothingByBrandAndType(self, brand, clothing_type):
        cursor = self.conn.cursor()
        query = "select * from Clothing where brand = %s and clothing_type = %s;"
        cursor.execute(query, (brand, clothing_type))
        result = cursor.fetchall()
        return result

    def getClothingByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Clothing where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getClothingByType(self, clothing_type):
        cursor = self.conn.cursor()
        query = "select * from Clothing where clothing_type = %s;"
        cursor.execute(query, (clothing_type,))
        result = cursor.fetchall()
        return result

    def getClothingSuppliesByBrandAndTypeAndMaxPrice(self, brand, clothing_type, max_price):
        cursor = self.conn.cursor()
        query = "select * from Clothing where brand = %s and unit_price <= %s and is_supply = TRUE and clothing_type = %s;"
        cursor.execute(query, (brand, max_price, clothing_type))
        result = cursor.fetchall()
        return result

    def getClothingSuppliesByBrandAndType(self, brand, clothing_type):
        cursor = self.conn.cursor()
        query = "select * from Clothing where brand = %s and is_supply = TRUE and clothing_type = %s;"
        cursor.execute(query, (brand, clothing_type))
        result = cursor.fetchall()
        return result

    def getClothingSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Clothing where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getClothingSuppliesByType(self, clothing_type):
        cursor = self.conn.cursor()
        query = "select * from Clothing where is_supply = TRUE and clothing_type = %s;"
        cursor.execute(query, (clothing_type,))
        result = cursor.fetchall()
        return result

    def getClothingSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select * from Clothing where is_supply = TRUE and unit_price <= %s;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getClothingRequestsByBrandAndType(self, brand, clothing_type):
        cursor = self.conn.cursor()
        query = "select * from Clothing where brand = %s and clothing_type = %s and is_supply = FALSE;"
        cursor.execute(query, (brand, clothing_type))
        result = cursor.fetchall()
        return result

    def getClothingRequestsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Clothing where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getClothingRequestsByType(self, clothing_type):
        cursor = self.conn.cursor()
        query = "select * from Clothing where clothing_type = %s and is_supply = FALSE;"
        cursor.execute(query, (clothing_type,))
        result = cursor.fetchall()
        return result

    def insert(self, person_id, brand, clothing_type, description, quantity, unit_price, date_posted, curr_quantity,
               is_supply, address_id):
        cursor = self.conn.cursor()
        query = "insert into Clothing(person_id, brand, clothing_type, description, quantity, unit_price, date_posted, curr_quantity, " \
                "is_supply, address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning supply_id;"
        cursor.execute(query, (person_id, brand, clothing_type, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, address_id))
        clothing_id = cursor.fetchone()[0]
        self.conn.commit()
        return clothing_id

    def delete(self, clothing_id):
        cursor = self.conn.cursor()
        query = "update Clothing set curr_quantity = 0 where clothing_id = %s;"
        cursor.execute(query, (clothing_id,))
        self.conn.commit()
        return clothing_id

    def update(self, clothing_id, brand, clothing_type, description, unit_price, curr_quantity, address_id):
        cursor = self.conn.cursor()
        query = "update Clothing set brand = %s, clothing_type = %s, description = %s, unit_price = %s, curr_quantity = %s, " \
                "address_id = %s where clothing_id = %s;"
        cursor.execute(query, (brand, clothing_type, description, unit_price, curr_quantity, address_id, clothing_id))
        self.conn.commit()
        return clothing_id
