from backend.config.dbconfig import pg_config
import psycopg2

class BatteryDAO:
    def __init__(self):

        connection_url = "dbType=%s user=%s password=%s" % (pg_config['dbType'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllBattery(self):
        cursor = self.conn.cursor()
        query = "select * from Batteries;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllBatterySupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Batteries where is_supply = TRUE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllBatteryRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Batteries where is_supply = FALSE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableBatterySupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Batteries where is_supply = TRUE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUnfulfilledBatteryRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Batteries where is_supply = FALSE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBatteryById(self, battery_id):
        cursor = self.conn.cursor()
        query = "select * from Batteries where battery_id = %s;"
        cursor.execute(query, (battery_id,))
        result = cursor.fetchone()
        return result

    def getBatteryByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Batteries where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getBatterySuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Batteries where person_id = %s and is_supply = TRUE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getBatteryRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Batteries where person_id = %s and is_supply = FALSE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getBatteryByBrandAndType(self, brand, battery_type):
        cursor = self.conn.cursor()
        query = "select * from Batteries where brand = %s and battery_type = %s;"
        cursor.execute(query, (brand, battery_type))
        result = cursor.fetchall()
        return result

    def getBatteryByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Batteries where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getBatteryByType(self, battery_type):
        cursor = self.conn.cursor()
        query = "select * from Batteries where battery_type = %s;"
        cursor.execute(query, (battery_type,))
        result = cursor.fetchall()
        return result

    def getBatterySuppliesByBrandAndTypeAndMaxPrice(self, brand, battery_type, max_price):
        cursor = self.conn.cursor()
        query = "select * from Batteries where brand = %s and unit_price <= %s and is_supply = TRUE and battery_type = %s;"
        cursor.execute(query, (brand, max_price, battery_type))
        result = cursor.fetchall()
        return result

    def getBatterySuppliesByBrandAndType(self, brand, battery_type):
        cursor = self.conn.cursor()
        query = "select * from Batteries where brand = %s and is_supply = TRUE and battery_type = %s;"
        cursor.execute(query, (brand, battery_type))
        result = cursor.fetchall()
        return result

    def getBatterySuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Batteries where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getBatterySuppliesByType(self, battery_type):
        cursor = self.conn.cursor()
        query = "select * from Batteries where is_supply = TRUE and battery_type = %s;"
        cursor.execute(query, (battery_type,))
        result = cursor.fetchall()
        return result

    def getBatterySuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select * from Batteries where is_supply = TRUE and unit_price <= %s;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getBatteryRequestsByBrandAndType(self, brand, battery_type):
        cursor = self.conn.cursor()
        query = "select * from Batteries where brand = %s and battery_type = %s and is_supply = FALSE;"
        cursor.execute(query, (brand, battery_type))
        result = cursor.fetchall()
        return result

    def getBatteryRequestsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Batteries where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getBatteryRequestsByType(self, battery_type):
        cursor = self.conn.cursor()
        query = "select * from Batteries where battery_type = %s and is_supply = FALSE;"
        cursor.execute(query, (battery_type,))
        result = cursor.fetchall()
        return result

    def insert(self, person_id, brand, battery_type, description, quantity, unit_price, date_posted, curr_quantity,
               is_supply, address_id):
        cursor = self.conn.cursor()
        query = "insert into Batteries(person_id, brand, battery_type, description, quantity, unit_price, date_posted, curr_quantity, " \
                "is_supply, address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning supply_id;"
        cursor.execute(query, (person_id, brand, battery_type, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, address_id))
        battery_id = cursor.fetchone()[0]
        self.conn.commit()
        return battery_id

    def delete(self, battery_id):
        cursor = self.conn.cursor()
        query = "update Batteries set curr_quantity = 0 where battery_id = %s;"
        cursor.execute(query, (battery_id,))
        self.conn.commit()
        return battery_id

    def update(self, battery_id, brand, battery_type, description, unit_price, curr_quantity, address_id):
        cursor = self.conn.cursor()
        query = "update Batteries set brand = %s, battery_type = %s, description = %s, unit_price = %s, curr_quantity = %s, " \
                "address_id = %s where battery_id = %s;"
        cursor.execute(query, (brand, battery_type, description, unit_price, curr_quantity, address_id, battery_id))
        self.conn.commit()
        return battery_id
