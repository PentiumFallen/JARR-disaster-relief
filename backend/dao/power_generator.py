from backend.config.dbconfig import pg_config
import psycopg2

class PowerGeneratorsDAO:
    def __init__(self):

        connection_url = "dbWatts=%s user=%s password=%s" % (pg_config['dbWatts'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllPowerGenerators(self):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result


    def getAllPowerGeneratorsSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where is_supply = TRUE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllPowerGeneratorsRequests(self):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where is_supply = FALSE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailablePowerGeneratorsSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where is_supply = TRUE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUnfulfilledPowerGeneratorsRequests(self):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where is_supply = FALSE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPowerGeneratorsById(self, generator_id):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where generator_id = %s;"
        cursor.execute(query, (generator_id,))
        result = cursor.fetchone()
        return result

    def getPowerGeneratorsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorsSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where person_id = %s and is_supply = TRUE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorsRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where person_id = %s and is_supply = FALSE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorsByBrandAndWatts(self, brand):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where brand = %s an = %s;"
        cursor.execute(query, (brand))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorsByWatts(self, watts):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where watts = %s;"
        cursor.execute(query, (watts,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorsBy(self, watts):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where watts = %s;"
        cursor.execute(query, (watts,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorsSuppliesByBrandAndWattsAndMaxPrice(self, brand, max_price):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where brand = %s and unit_price <= %s and is_supply = TRUE;"
        cursor.execute(query, (brand, max_price))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorsSuppliesByBrandAndWatts(self, brand):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorsSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorsSuppliesByWatts(self, watts):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where is_supply = TRUE;"
        cursor.execute(query, (watts,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorsSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where is_supply = TRUE and unit_price <= %s;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorsRequestsByBrandAndWatts(self, brand):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorsRequestsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorsRequestsByWatts(self, watts):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where  = %s and is_supply = FALSE;"
        cursor.execute(query, (watts,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorsByWatts(self, watts):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerator where  = %s and is_supply = FALSE;"
        cursor.execute(query, (watts,))
        result = cursor.fetchall()
        return result

    def insert(self, person_id, brand, watts, description, quantity, unit_price, date_posted, curr_quantity,
               is_supply, fuel_used, address_id):
        cursor = self.conn.cursor()
        query = "insert into PowerGenerator(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity, " \
                "is_supply, fuel_used, address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning supply_id;"
        cursor.execute(query, (person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, fuel_used, address_id))
        generator_id = cursor.fetchone()[0]
        self.conn.commit()
        return generator_id

    def delete(self, generator_id):
        cursor = self.conn.cursor()
        query = "update PowerGenerator set curr_quantity = 0 where generator_id = %s;"
        cursor.execute(query, (generator_id,))
        self.conn.commit()
        return generator_id

    def update(self, generator_id, brand, description, unit_price, curr_quantity, fuel_used, address_id):
        cursor = self.conn.cursor()
        query = "update PowerGenerator set brand = %s = %s, description = %s, unit_price = %s, curr_quantity = %s, fuel_used = %s " \
                "address_id = %s where generator_id = %s;"
        cursor.execute(query, (brand, description, unit_price, curr_quantity, fuel_used, address_id, generator_id))
        self.conn.commit()
        return generator_id
