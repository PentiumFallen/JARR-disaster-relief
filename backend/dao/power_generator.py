from backend.config.dbconfig import pg_config
import psycopg2

class PowerGeneratorDAO:
    def __init__(self):

        connection_url = "dbWatts=%s user=%s password=%s" % (pg_config['dbWatts'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllPowerGenerator(self):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result


    def getAllPowerGeneratorSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where is_supply = TRUE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllPowerGeneratorRequests(self):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where is_supply = FALSE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailablePowerGeneratorSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where is_supply = TRUE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUnfulfilledPowerGeneratorRequests(self):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where is_supply = FALSE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPowerGeneratorById(self, generator_id):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where generator_id = %s;"
        cursor.execute(query, (generator_id,))
        result = cursor.fetchone()
        return result

    def getPowerGeneratorByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where person_id = %s and is_supply = TRUE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where person_id = %s and is_supply = FALSE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorByBrandAndWatts(self, brand):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where brand = %s an = %s;"
        cursor.execute(query, (brand))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorByWatts(self, watts):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where watts = %s;"
        cursor.execute(query, (watts,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorBy(self, watts):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where watts = %s;"
        cursor.execute(query, (watts,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorSuppliesByBrandAndWattsAndMaxPrice(self, brand, watts, max_price):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where brand = %s and watts = %s and unit_price <= %s and is_supply = TRUE;"
        cursor.execute(query, (brand,watts, max_price))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorSuppliesByBrandAndWatts(self, brand, watts):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where brand = %s and is_supply = TRUE and watts = %s;"
        cursor.execute(query, (brand, watts))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorSuppliesByWatts(self, watts):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where is_supply = TRUE and watts = %s;"
        cursor.execute(query, (watts,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where is_supply = TRUE and unit_price <= %s;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorRequestsByBrandAndWatts(self, brand):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where brand = %s and is_supply = FALSE and watts = %s;"
        cursor.execute(query, (brand))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorRequestsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorRequestsByWatts(self, watts):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where  watts = %s and is_supply = FALSE;"
        cursor.execute(query, (watts,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorByWatts(self, watts):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where watts = %s and is_supply = FALSE;"
        cursor.execute(query, (watts,))
        result = cursor.fetchall()
        return result

    def getPowerGeneratorByFuelUsed(self, fuel_used):
        cursor = self.conn.cursor()
        query = "select * from PowerGenerators where fuel_used = TRUE and is_supply = FALSE;"
        cursor.execute(query, (fuel_used,))
        result = cursor.fetchall()
        return result

    def insert(self, person_id, brand, watts, description, quantity, unit_price, date_posted, curr_quantity,
               is_supply, fuel_used, address_id):
        cursor = self.conn.cursor()
        query = "insert into PowerGenerators(person_id, brand, watts, description, quantity, unit_price, date_posted, curr_quantity, " \
                "is_supply, fuel_used, address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning supply_id;"
        cursor.execute(query, (person_id, brand, watts, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, fuel_used, address_id))
        generator_id = cursor.fetchone()[0]
        self.conn.commit()
        return generator_id

    def delete(self, generator_id):
        cursor = self.conn.cursor()
        query = "update PowerGenerators set curr_quantity = 0 where generator_id = %s;"
        cursor.execute(query, (generator_id,))
        self.conn.commit()
        return generator_id

    def update(self, generator_id, brand, watts, description, unit_price, curr_quantity, fuel_used, address_id):
        cursor = self.conn.cursor()
        query = "update PowerGenerators set brand = %s, watts = %s, description = %s, unit_price = %s, curr_quantity = %s, fuel_used = %s " \
                "address_id = %s where generator_id = %s;"
        cursor.execute(query, (brand, watts, description, unit_price, curr_quantity, fuel_used, address_id, generator_id))
        self.conn.commit()
        return generator_id
