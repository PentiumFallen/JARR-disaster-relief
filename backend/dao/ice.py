from backend.config.dbconfig import pg_config
import psycopg2


class IceDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllIce(self):
        cursor = self.conn.cursor()
        query = "select * from Ice;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllIceSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Ice where is_supply = TRUE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllIceRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Ice where is_supply = FALSE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableIceSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Ice where is_supply = TRUE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUnfulfilledIceRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Ice where is_supply = FALSE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getIceById(self, ice_id):
        cursor = self.conn.cursor()
        query = "select * from Ice where ice_id = %s;"
        cursor.execute(query, (ice_id,))
        result = cursor.fetchone()
        return result

    def getIceByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Ice where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getIceSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Ice where person_id = %s and is_supply = TRUE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getIceRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Ice where person_id = %s and is_supply = FALSE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getIceByBrandAndFoodType(self, brand, weight):
        cursor = self.conn.cursor()
        query = "select * from Ice where brand = %s and weight = %s;"
        cursor.execute(query, (brand, weight))
        result = cursor.fetchall()
        return result

    def getIceByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Ice where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getIceByFoodType(self, weight):
        cursor = self.conn.cursor()
        query = "select * from Ice where weight = %s;"
        cursor.execute(query, (weight,))
        result = cursor.fetchall()
        return result

    def getIceSuppliesByBrandAndFoodTypeAndMaxPrice(self, brand, weight, max_price):
        cursor = self.conn.cursor()
        query = "select * from Ice where brand = %s and unit_price <= %s and is_supply = TRUE and food_" \
                "type =  %s;"
        cursor.execute(query, (brand, max_price, weight))
        result = cursor.fetchall()
        return result

    def getIceSuppliesByBrandAndFoodType(self, brand, weight):
        cursor = self.conn.cursor()
        query = "select * from Ice where brand = %s and is_supply = TRUE and weight = %s;"
        cursor.execute(query, (brand, weight))
        result = cursor.fetchall()
        return result

    def getIceSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Ice where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getIceSuppliesByFoodType(self, weight):
        cursor = self.conn.cursor()
        query = "select * from Ice where is_supply = TRUE and weight = %s;"
        cursor.execute(query, (weight,))
        result = cursor.fetchall()
        return result

    def getIceSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select * from Ice where is_supply = TRUE and unit_price <= %s;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getIceRequestsByBrandAndFoodType(self, brand, weight):
        cursor = self.conn.cursor()
        query = "select * from Ice where brand = %s and is_supply = FALSE and weight = %s"
        cursor.execute(query, (brand, weight))
        result = cursor.fetchall()
        return result

    def getIceRequestsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Ice where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getIceRequestsByFoodType(self, weight):
        cursor = self.conn.cursor()
        query = "select * from Ice where is_supply = FALSE and weight = %s"
        cursor.execute(query, (weight,))
        result = cursor.fetchall()
        return result

    def getIceByFoodType(self, weight):
        cursor = self.conn.cursor()
        query = "select ice_id from Ice where weight = %s;"
        cursor.execute(query, (weight,))
        result = cursor.fetchall()
        return result

    def insert(self, person_id, brand, weight, description, quantity, unit_price, date_posted, curr_quantity,
               is_supply, address_id):
        cursor = self.conn.cursor()

        query = "insert into Ice(person_id, brand, weight, description, quantity, unit_price, date_posted, " \
                "curr_quantity, is_supply, address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " \
                "returning supply_id;"
        cursor.execute(query, (person_id, brand, weight, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, address_id))

        ice_id = cursor.fetchone()[0]

        self.conn.commit()
        return ice_id

    def delete(self, ice_id):
        cursor = self.conn.cursor()
        query = "update Ice set curr_quantity = 0 where ice_id = %s;"
        cursor.execute(query, (ice_id,))
        self.conn.commit()
        return ice_id

    def update(self, ice_id, brand, weight, description, unit_price, curr_quantity, address_id):
        cursor = self.conn.cursor()
        query = "update Ice set brand = %s, weight = %s, description = %s, unit_price = %s, curr_quantity = %s, " \
                "address_id = %s where ice_id = %s;"
        cursor.execute(query, (brand, weight, description, unit_price, curr_quantity, address_id, ice_id))
        self.conn.commit()
        return ice_id
