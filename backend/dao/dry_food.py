from backend.config.dbconfig import pg_config
import psycopg2


class DryFoodDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllDryFood(self):
        cursor = self.conn.cursor()
        query = "select * from DryFoods;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllDryFoodSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where is_supply = TRUE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllDryFoodRequests(self):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where is_supply = FALSE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableDryFoodSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where is_supply = TRUE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUnfulfilledDryFoodRequests(self):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where is_supply = FALSE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getDryFoodById(self, df_id):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where df_id = %s;"
        cursor.execute(query, (df_id,))
        result = cursor.fetchone()
        return result

    def getDryFoodByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getDryFoodSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where person_id = %s and is_supply = TRUE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getDryFoodRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where person_id = %s and is_supply = FALSE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getDryFoodByBrandAndFoodType(self, brand, food_type):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where brand = %s and food_type = %s;"
        cursor.execute(query, (brand, food_type))
        result = cursor.fetchall()
        return result

    def getDryFoodByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getDryFoodByFoodType(self, food_type):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where food_type = %s;"
        cursor.execute(query, (food_type,))
        result = cursor.fetchall()
        return result

    def getDryFoodSuppliesByBrandAndFoodTypeAndMaxPrice(self, brand, food_type, max_price):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where brand = %s and unit_price <= %s and is_supply = TRUE and food_" \
                "type =  %s;"
        cursor.execute(query, (brand, max_price, food_type))
        result = cursor.fetchall()
        return result

    def getDryFoodSuppliesByBrandAndFoodType(self, brand, food_type):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where brand = %s and is_supply = TRUE and food_type = %s;"
        cursor.execute(query, (brand, food_type))
        result = cursor.fetchall()
        return result

    def getDryFoodSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getDryFoodSuppliesByFoodType(self, food_type):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where is_supply = TRUE and food_type = %s;"
        cursor.execute(query, (food_type,))
        result = cursor.fetchall()
        return result

    def getDryFoodSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where is_supply = TRUE and unit_price <= %s;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getDryFoodRequestsByBrandAndFoodType(self, brand, food_type):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where brand = %s and is_supply = FALSE and food_type = %s"
        cursor.execute(query, (brand, food_type))
        result = cursor.fetchall()
        return result

    def getDryFoodRequestsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getDryFoodRequestsByFoodType(self, food_type):
        cursor = self.conn.cursor()
        query = "select * from DryFoods where is_supply = FALSE and food_type = %s"
        cursor.execute(query, (food_type,))
        result = cursor.fetchall()
        return result

    def getDryFoodByFoodType(self, food_type):
        cursor = self.conn.cursor()
        query = "select df_id from DryFoods where food_type = %s;"
        cursor.execute(query, (food_type,))
        result = cursor.fetchall()
        return result

    def insert(self, person_id, brand, food_type, description, quantity, unit_price, date_posted, curr_quantity,
               is_supply, address_id):
        cursor = self.conn.cursor()

        query = "insert into DryFoods(person_id, brand, food_type, description, quantity, unit_price, date_posted, curr_quantity, " \
                "is_supply, address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning supply_id;"
        cursor.execute(query, (person_id, brand, food_type, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, address_id))

        df_id = cursor.fetchone()[0]

        self.conn.commit()
        return df_id

    def delete(self, df_id):
        cursor = self.conn.cursor()
        query = "update DryFoods set curr_quantity = 0 where df_id = %s;"
        cursor.execute(query, (df_id,))
        self.conn.commit()
        return df_id

    def update(self, df_id, brand, food_type, description, unit_price, curr_quantity, address_id):
        cursor = self.conn.cursor()
        query = "update DryFoods set brand = %s, food_type = %s, description = %s, unit_price = %s, curr_quantity = %s, " \
                "address_id = %s where df_id = %s;"
        cursor.execute(query, (brand, food_type, description, unit_price, curr_quantity, address_id, df_id))
        self.conn.commit()
        return df_id
