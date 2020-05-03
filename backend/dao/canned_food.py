from backend.config.dbconfig import pg_config
import psycopg2

class CannedFoodDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllCannedFood(self):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllCannedFoodSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where is_supply = TRUE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllCannedFoodRequests(self):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where is_supply = FALSE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableCannedFoodSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where is_supply = TRUE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUnfulfilledCannedFoodRequests(self):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where is_supply = FALSE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getCannedFoodById(self, cf_id):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where cf_id = %s;"
        cursor.execute(query, (cf_id,))
        result = cursor.fetchone()
        return result

    def getCannedFoodByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getCannedFoodSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where person_id = %s and is_supply = TRUE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getCannedFoodRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where person_id = %s and is_supply = FALSE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getCannedFoodByBrandAndFoodType(self, brand, food_type):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where brand = %s and food_type = %s;"
        cursor.execute(query, (brand, food_type))
        result = cursor.fetchall()
        return result

    def getCannedFoodByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getCannedFoodByFoodType(self, food_type):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where food_type = %s;"
        cursor.execute(query, (food_type,))
        result = cursor.fetchall()
        return result

    def getCannedFoodSuppliesByBrandAndFoodTypeAndMaxPrice(self, brand, food_type, max_price):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where brand = %s and unit_price <= %s and is_supply = TRUE and food_" \
                "type =  %s;"
        cursor.execute(query, (brand, max_price, food_type))
        result = cursor.fetchall()
        return result

    def getCannedFoodSuppliesByBrandAndFoodType(self, brand, food_type):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where brand = %s and is_supply = TRUE and food_type = %s;"
        cursor.execute(query, (brand, food_type))
        result = cursor.fetchall()
        return result

    def getCannedFoodSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getCannedFoodSuppliesByFoodType(self, food_type):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where is_supply = TRUE and food_type = %s;"
        cursor.execute(query, (food_type,))
        result = cursor.fetchall()
        return result

    def getCannedFoodSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where is_supply = TRUE and unit_price <= %s;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getCannedFoodRequestsByBrandAndFoodType(self, brand, food_type):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where brand = %s and is_supply = FALSE and food_type = %s"
        cursor.execute(query, (brand, food_type))
        result = cursor.fetchall()
        return result

    def getCannedFoodRequestsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getCannedFoodRequestsByFoodType(self, food_type):
        cursor = self.conn.cursor()
        query = "select * from CannedFoods where is_supply = FALSE and food_type = %s"
        cursor.execute(query, (food_type,))
        result = cursor.fetchall()
        return result

    def getCannedFoodByFoodType(self, food_type):
        cursor = self.conn.cursor()
        query = "select cf_id from CannedFoods where food_type = %s;"
        cursor.execute(query, (food_type,))
        result = cursor.fetchall()
        return result

    def insert(self, person_id, brand, food_type, description, quantity, unit_price, date_posted, curr_quantity,
               is_supply, address_id):
        cursor = self.conn.cursor()

        query = "insert into CannedFoods(person_id, brand, food_type, description, quantity, unit_price, date_posted, curr_quantity, " \
                "is_supply, address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning supply_id;"
        cursor.execute(query, (person_id, brand, food_type, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, address_id))

        cf_id = cursor.fetchone()[0]

        self.conn.commit()
        return cf_id

    def delete(self, cf_id):
        cursor = self.conn.cursor()
        query = "update CannedFoods set curr_quantity = 0 where cf_id = %s;"
        cursor.execute(query, (cf_id,))
        self.conn.commit()
        return cf_id

    def update(self, cf_id, brand, food_type, description, unit_price, curr_quantity, address_id):
        cursor = self.conn.cursor()
        query = "update CannedFoods set brand = %s, food_type = %s, description = %s, unit_price = %s, curr_quantity = %s, " \
                "address_id = %s where cf_id = %s;"
        cursor.execute(query, (brand, food_type, description, unit_price, curr_quantity, address_id, cf_id))
        self.conn.commit()
        return cf_id
