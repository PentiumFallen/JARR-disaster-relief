from backend.config.dbconfig import pg_config
import psycopg2


class BabyFoodDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllBabyFood(self):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllBabyFoodSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where is_supply = TRUE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllBabyFoodRequests(self):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where is_supply = FALSE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableBabyFoodSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where is_supply = TRUE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUnfulfilledBabyFoodRequests(self):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where is_supply = FALSE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBabyFoodById(self, bf_id):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where bf_id = %s;"
        cursor.execute(query, (bf_id,))
        result = cursor.fetchone()
        return result

    def getBabyFoodByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getBabyFoodSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where person_id = %s and is_supply = TRUE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getBabyFoodRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where person_id = %s and is_supply = FALSE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getBabyFoodByBrandAndFlavor(self, brand, flavor):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where brand = %s and flavor = %s;"
        cursor.execute(query, (brand, flavor))
        result = cursor.fetchall()
        return result

    def getBabyFoodByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getBabyFoodByFlavor(self, flavor):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where flavor = %s;"
        cursor.execute(query, (flavor,))
        result = cursor.fetchall()
        return result

    def getBabyFoodSuppliesByBrandAndFlavorAndMaxPrice(self, brand, flavor, max_price):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where brand = %s and unit_price <= %s and is_supply = TRUE and flavor =  %s;"
        cursor.execute(query, (brand, max_price, flavor))
        result = cursor.fetchall()
        return result

    def getBabyFoodSuppliesByBrandAndFlavor(self, brand, flavor):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where brand = %s and is_supply = TRUE and flavor = %s;"
        cursor.execute(query, (brand, flavor))
        result = cursor.fetchall()
        return result

    def getBabyFoodSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getBabyFoodSuppliesByFlavor(self, flavor):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where is_supply = TRUE and flavor = %s;"
        cursor.execute(query, (flavor,))
        result = cursor.fetchall()
        return result

    def getBabyFoodSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where is_supply = TRUE and unit_price <= %s;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getBabyFoodRequestsByBrandAndFlavor(self, brand, flavor):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where brand = %s and is_supply = FALSE and flavor = %s"
        cursor.execute(query, (brand, flavor))
        result = cursor.fetchall()
        return result

    def getBabyFoodRequestsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getBabyFoodRequestsByFlavor(self, flavor):
        cursor = self.conn.cursor()
        query = "select * from BabyFoods where is_supply = FALSE and flavor = %s"
        cursor.execute(query, (flavor,))
        result = cursor.fetchall()
        return result

    def getBabyFoodByFlavor(self, flavor):
        cursor = self.conn.cursor()
        query = "select bf_id from BabyFoods where flavor = %s;"
        cursor.execute(query, (flavor,))
        result = cursor.fetchall()
        return result

    def insert(self, person_id, brand, flavor, description, quantity, unit_price, date_posted, curr_quantity,
               is_supply, address_id):
        cursor = self.conn.cursor()

        query = "insert into BabyFoods(person_id, brand, flavor, description, quantity, unit_price, date_posted, curr_quantity, " \
                "is_supply, address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning supply_id;"
        cursor.execute(query, (person_id, brand, flavor, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, address_id))

        bf_id = cursor.fetchone()[0]

        self.conn.commit()
        return bf_id

    def delete(self, bf_id):
        cursor = self.conn.cursor()
        query = "update BabyFoods set curr_quantity = 0 where bf_id = %s;"
        cursor.execute(query, (bf_id,))
        self.conn.commit()
        return bf_id

    def update(self, bf_id, brand, flavor, description, unit_price, curr_quantity, address_id):
        cursor = self.conn.cursor()
        query = "update BabyFoods set brand = %s, flavor = %s, description = %s, unit_price = %s, curr_quantity = %s, " \
                "address_id = %s where bf_id = %s;"
        cursor.execute(query, (brand, flavor, description, unit_price, curr_quantity, address_id, bf_id))
        self.conn.commit()
        return bf_id
