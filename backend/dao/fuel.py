from backend.config.dbconfig import pg_config
import psycopg2

class FuelDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllFuel(self):
        cursor = self.conn.cursor()
        query = "select * from Fuel;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllFuelSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Fuel where is_supply = TRUE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllFuelRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Fuel where is_supply = FALSE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableFuelSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Fuel where is_supply = TRUE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUnfulfilledFuelRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Fuel where is_supply = FALSE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getFuelById(self, fuel_id):
        cursor = self.conn.cursor()
        query = "select * from Fuel where fuel_id = %s;"
        cursor.execute(query, (fuel_id,))
        result = cursor.fetchone()
        return result

    def getFuelByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Fuel where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getFuelSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Fuel where person_id = %s and is_supply = TRUE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getFuelRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Fuel where person_id = %s and is_supply = FALSE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getFuelByBrandAndType(self, brand, fuel_type):
        cursor = self.conn.cursor()
        query = "select * from Fuel where brand = %s and fuel_id = (select fuel_id from FuelTypes where fuel_type = %s);"
        cursor.execute(query, (brand, fuel_type))
        result = cursor.fetchall()
        return result

    def getFuelByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Fuel where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getFuelByType(self, fuel_type):
        cursor = self.conn.cursor()
        query = "select * from Fuel where fuel_id = (select fuel_id from FuelTypes where fuel_type = %s);"
        cursor.execute(query, (fuel_type,))
        result = cursor.fetchall()
        return result

    def getFuelSuppliesByBrandAndTypeAndMaxPrice(self, brand, fuel_type, max_price):
        cursor = self.conn.cursor()
        query = "select * from Fuel where brand = %s and unit_price <= %s and is_supply = TRUE and fuel_id = " \
                "(select fuel_id from FuelTypes where fuel_type = %s);"
        cursor.execute(query, (brand, max_price, fuel_type))
        result = cursor.fetchall()
        return result

    def getFuelSuppliesByBrandAndType(self, brand, fuel_type):
        cursor = self.conn.cursor()
        query = "select * from Fuel where brand = %s and is_supply = TRUE and fuel_id = " \
                "(select fuel_id from FuelTypes where fuel_type = %s);"
        cursor.execute(query, (brand, fuel_type))
        result = cursor.fetchall()
        return result

    def getFuelSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Fuel where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getFuelSuppliesByType(self, fuel_type):
        cursor = self.conn.cursor()
        query = "select * from Fuel where is_supply = TRUE and fuel_id = " \
                "(select fuel_id from FuelTypes where fuel_type = %s);"
        cursor.execute(query, (fuel_type,))
        result = cursor.fetchall()
        return result

    def getFuelSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select * from Fuel where is_supply = TRUE and unit_price <= %s;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getFuelRequestsByBrandAndType(self, brand, fuel_type):
        cursor = self.conn.cursor()
        query = "select * from Fuel where brand = %s and is_supply = FALSE and fuel_id = " \
                "(select fuel_id from FuelTypes where fuel_type = %s);"
        cursor.execute(query, (brand, fuel_type))
        result = cursor.fetchall()
        return result

    def getFuelRequestsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Fuel where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getFuelRequestsByType(self, fuel_type):
        cursor = self.conn.cursor()
        query = "select * from Fuel where is_supply = FALSE and fuel_id = " \
                "(select fuel_id from FuelTypes where fuel_type = %s);"
        cursor.execute(query, (fuel_type,))
        result = cursor.fetchall()
        return result

    def getFuelTypeId(self, fuel_type):
        cursor = self.conn.cursor()
        query = "select fuel_id from FuelTypes natural where fuel_type = %s;"
        cursor.execute(query, (fuel_type,))
        result = cursor.fetchall()
        return result

    def insert(self, person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
               is_supply, type_id, address_id):
        cursor = self.conn.cursor()

        query = "insert into Fuel(person_id, brand, description, quantity, unit_price, date_posted, curr_quantity, " \
                "is_supply, type_id, address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning supply_id;"
        cursor.execute(query, (person_id, brand, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, type_id, address_id))

        fuel_id = cursor.fetchone()[0]

        self.conn.commit()
        return fuel_id

    def delete(self, fuel_id):
        cursor = self.conn.cursor()
        query = "update Fuel set curr_quantity = 0 where fuel_id = %s;"
        cursor.execute(query, (fuel_id,))
        self.conn.commit()
        return fuel_id

    def update(self, fuel_id, brand, description, unit_price, curr_quantity, type_id, address_id):
        cursor = self.conn.cursor()
        query = "update Fuel set brand = %s, description = %s, unit_price = %s, curr_quantity = %s, type_id = %s, " \
                "address_id = %s where fuel_id = %s;"
        cursor.execute(query, (brand, description, unit_price, curr_quantity, type_id, address_id, fuel_id))
        self.conn.commit()
        return fuel_id
