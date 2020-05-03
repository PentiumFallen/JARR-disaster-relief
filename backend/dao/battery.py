from backend.config.dbconfig import pg_config
import psycopg2

class BatteryDAO:
    def __init__(self):

        connection_url = "dbType=%s user=%s password=%s" % (pg_config['dbType'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllBatteries(self):
        cursor = self.conn.cursor()
        query = "select * from Battery;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllBatteriesSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Battery where is_supply = TRUE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllBatteriesRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Battery where is_supply = FALSE;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllAvailableBatteriesSupplies(self):
        cursor = self.conn.cursor()
        query = "select * from Battery where is_supply = TRUE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUnfulfilledBatteriesRequests(self):
        cursor = self.conn.cursor()
        query = "select * from Battery where is_supply = FALSE and curr_quantity > 0;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBatteriesById(self, battery_id):
        cursor = self.conn.cursor()
        query = "select * from Battery where battery_id = %s;"
        cursor.execute(query, (battery_id,))
        result = cursor.fetchone()
        return result

    def getBatteriesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Battery where person_id = %s;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getBatteriesSuppliesByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Battery where person_id = %s and is_supply = TRUE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getBatteriesRequestsByPersonId(self, person_id):
        cursor = self.conn.cursor()
        query = "select * from Battery where person_id = %s and is_supply = FALSE;"
        cursor.execute(query, (person_id,))
        result = cursor.fetchall()
        return result

    def getBatteriesByBrandAndType(self, brand, battery_type):
        cursor = self.conn.cursor()
        query = "select * from Battery where brand = %s and battery_type = %s;"
        cursor.execute(query, (brand, battery_type))
        result = cursor.fetchall()
        return result

    def getBatteriesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Battery where brand = %s;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getBatteriesByType(self, battery_type):
        cursor = self.conn.cursor()
        query = "select * from Battery where battery_type = %s;"
        cursor.execute(query, (battery_type,))
        result = cursor.fetchall()
        return result

    def getBatteriesSuppliesByBrandAndTypeAndMaxPrice(self, brand, battery_type, max_price):
        cursor = self.conn.cursor()
        query = "select * from Battery where brand = %s and unit_price <= %s and is_supply = TRUE and battery_type = %s;"
        cursor.execute(query, (brand, max_price, battery_type))
        result = cursor.fetchall()
        return result

    def getBatteriesSuppliesByBrandAndType(self, brand, battery_type):
        cursor = self.conn.cursor()
        query = "select * from Battery where brand = %s and is_supply = TRUE and battery_type = %s;"
        cursor.execute(query, (brand, battery_type))
        result = cursor.fetchall()
        return result

    def getBatteriesSuppliesByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Battery where brand = %s and is_supply = TRUE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getBatteriesSuppliesByType(self, battery_type):
        cursor = self.conn.cursor()
        query = "select * from Battery where is_supply = TRUE and battery_type = %s;"
        cursor.execute(query, (battery_type,))
        result = cursor.fetchall()
        return result

    def getBatteriesSuppliesByMaxPrice(self, max_price):
        cursor = self.conn.cursor()
        query = "select * from Battery where is_supply = TRUE and unit_price <= %s;"
        cursor.execute(query, (max_price,))
        result = cursor.fetchall()
        return result

    def getBatteriesRequestsByBrandAndType(self, brand, battery_type):
        cursor = self.conn.cursor()
        query = "select * from Battery where brand = %s and battery_type = %s and is_supply = FALSE;"
        cursor.execute(query, (brand, battery_type))
        result = cursor.fetchall()
        return result

    def getBatteriesRequestsByBrand(self, brand):
        cursor = self.conn.cursor()
        query = "select * from Battery where brand = %s and is_supply = FALSE;"
        cursor.execute(query, (brand,))
        result = cursor.fetchall()
        return result

    def getBatteriesRequestsByType(self, battery_type):
        cursor = self.conn.cursor()
        query = "select * from Battery where battery_type = %s and is_supply = FALSE;"
        cursor.execute(query, (battery_type,))
        result = cursor.fetchall()
        return result

    def insert(self, person_id, brand, battery_type, description, quantity, unit_price, date_posted, curr_quantity,
               is_supply, address_id):
        cursor = self.conn.cursor()
        query = "insert into Battery(person_id, brand, battery_type, description, quantity, unit_price, date_posted, curr_quantity, " \
                "is_supply, address_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning supply_id;"
        cursor.execute(query, (person_id, brand, battery_type, description, quantity, unit_price, date_posted, curr_quantity,
                               is_supply, address_id))
        battery_id = cursor.fetchone()[0]
        self.conn.commit()
        return battery_id

    def delete(self, battery_id):
        cursor = self.conn.cursor()
        query = "update Battery set curr_quantity = 0 where battery_id = %s;"
        cursor.execute(query, (battery_id,))
        self.conn.commit()
        return battery_id

    def update(self, battery_id, brand, battery_type, description, unit_price, curr_quantity, address_id):
        cursor = self.conn.cursor()
        query = "update Battery set brand = %s, battery_type = %s, description = %s, unit_price = %s, curr_quantity = %s, " \
                "address_id = %s where battery_id = %s;"
        cursor.execute(query, (brand, battery_type, description, unit_price, curr_quantity, address_id, battery_id))
        self.conn.commit()
        return battery_id
